import os
import asyncio
from transformers import pipeline
import torch
from typing import List, Dict
from google import genai
from dotenv import load_dotenv

load_dotenv()

class AnalyzerService:
    def __init__(self):
        # Using BERT-based models from Hugging Face
        self.emotion_analyzer = None
        self.sarcasm_analyzer = None
        self.sentiment_analyzer = None

        try:
            print("Loading Emotion BERT...")
            self.emotion_analyzer = pipeline("text-classification", 
                                            model="bhadresh-savani/bert-base-uncased-emotion", 
                                            return_all_scores=False)
        except Exception as e:
            print(f"Warning: Could not load emotion model: {e}")
        try:
            print("Loading Sarcasm Detection...")
            self.sarcasm_analyzer = pipeline("text-classification", 
                                            model="helinwang/sarcasm-detection")
        except Exception as e:
            print(f"Warning: Could not load sarcasm model: {e}")
        
        try:
            print("Loading Sentiment Engine...")
            self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                              model="distilbert-base-uncased-finetuned-sst-2-english")
        except Exception as e:
            print(f"Warning: Could not load sentiment model: {e}")

        # Configure Gemini using new SDK with v1 for current active models
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            try:
                # Switching to v1 as recommended for active models like 2.5/3.1
                self.client = genai.Client(
                    api_key=self.gemini_api_key,
                    http_options={'api_version': 'v1'}
                )
                self.available_model = None
            except Exception as e:
                print(f"Error initializing Gemini client: {e}")
                self.client = None
        else:
            self.client = None

    def analyze(self, texts: List[str]) -> List[Dict]:
        results = []
        for text in texts:
            if not text.strip(): continue
            truncated_text = text[:512]
            
            try:
                sentiment = "NEUTRAL"
                emotion = "neutral"
                is_sarcastic = False
                score = 0.5

                if self.sentiment_analyzer:
                    res = self.sentiment_analyzer(truncated_text)[0]
                    sentiment = res['label']
                    score = res['score']
                
                if self.emotion_analyzer:
                    emotion = self.emotion_analyzer(truncated_text)[0]['label']
                
                if self.sarcasm_analyzer:
                    s_res = self.sarcasm_analyzer(truncated_text)[0]
                    is_sarcastic = s_res['label'].upper() == 'LABEL_1'

                results.append({
                    "text": text,
                    "sentiment": sentiment,
                    "emotion": emotion,
                    "sarcastic": is_sarcastic,
                    "confidence": score
                })
            except Exception as e:
                print(f"Error analyzing text: {e}")
                
        return results

    def get_summary(self, results: List[Dict]) -> Dict:
        if not results: return {}
        
        total = len(results)
        sentiments = {}
        emotions = {}
        sarcastic_count = 0
        
        for r in results:
            sent = r['sentiment'].upper()
            sentiments[sent] = sentiments.get(sent, 0) + 1
            
            emo = r['emotion']
            emotions[emo] = emotions.get(emo, 0) + 1
            
            if r['sarcastic']:
                sarcastic_count += 1
                
        return {
            "sentiment_distribution": sentiments,
            "emotion_distribution": emotions,
            "sarcasm_percentage": (sarcastic_count / total) * 100 if total > 0 else 0
        }

    async def _get_best_model(self):
        if hasattr(self, 'available_model') and self.available_model:
            return self.available_model
        
        try:
            # Discover available models
            models_iter = await asyncio.to_thread(lambda: list(self.client.models.list()))
            models = [m.name for m in models_iter]
            
            # Priority list updated for 2026 guidelines
            priority = [
                'models/gemini-2.5-flash', 
                'models/gemini-3.1-pro-preview',
                'models/gemini-3-flash-preview',
                'models/gemini-2.5-pro'
            ]
            
            for p in priority:
                if p in models:
                    self.available_model = p
                    return p
            
            # If priority ones aren't there, take the first one containing 'flash' or 'pro'
            for m in models:
                if 'flash' in m or 'pro' in m:
                    self.available_model = m
                    return m
                    
            if models:
                self.available_model = models[0]
                return models[0]
        except:
            pass
        
        # Absolute fallback to a 2026 active model
        return 'gemini-2.5-flash'

    async def get_ai_summary(self, results: List[Dict], summary_stats: Dict) -> str:
        if not self.client:
            return "AI summary is unavailable because GEMINI_API_KEY is not configured."

        review_samples = [r['text'] for r in results[:15]]
        
        prompt = f"""
        You are an expert product analyst. Based on the following sentiment and emotion analysis of customer reviews, 
        provide a concise, professional, and insightful summary of the product.
        
        Stats:
        - Sentiment Distribution: {summary_stats['sentiment_distribution']}
        - Emotion Distribution: {summary_stats['emotion_distribution']}
        - Sarcasm Level: {summary_stats['sarcasm_percentage']:.1f}%
        
        Sample Reviews:
        {chr(10).join(['- ' + r for r in review_samples])}
        
        Your summary should highlight:
        1. The overall consensus (positive, negative, or mixed).
        2. Key strengths mentioned by customers.
        3. Common complaints or issues.
        4. Whether it's recommended based on the data.
        
        Keep it to 2-3 short paragraphs.
        """

        model_name = await self._get_best_model()
        
        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating AI summary with {model_name}: {e}")
            # If it fails, try a direct string name as fallback in case 'models/' prefix is causing the 404
            try:
                fallback_name = model_name.replace('models/', '')
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=fallback_name,
                    contents=prompt
                )
                return response.text
            except:
                return f"Failed to generate AI summary. Error: {str(e)[:100]}"
