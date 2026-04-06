from transformers import pipeline
import torch
from typing import List, Dict

class AnalyzerService:
    def __init__(self):
        # Using BERT-based models from Hugging Face
        # We use try/except for each model to ensure the app starts even if a download fails
        
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
            print("Loading Sarcasm BERT...")
            # Using a reliable, existing model
            self.sarcasm_analyzer = pipeline("text-classification", 
                                            model="jkandut/sarcasm-detection-bert")
        except Exception as e:
            print(f"Warning: Could not load sarcasm model: {e}")
        
        try:
            print("Loading Sentiment Engine...")
            self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                              model="distilbert-base-uncased-finetuned-sst-2-english")
        except Exception as e:
            print(f"Warning: Could not load sentiment model: {e}")

    def analyze(self, texts: List[str]) -> List[Dict]:
        results = []
        for text in texts:
            if not text.strip(): continue
            truncated_text = text[:512]
            
            try:
                # Default values in case models aren't loaded
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
                    # jkandut model: label_1 is sarcastic, label_0 is non-sarcastic
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
