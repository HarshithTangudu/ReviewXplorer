export interface CommentResult {
  text: string;
  sentiment: string;
  emotion: string;
  sarcastic: boolean;
  confidence: number;
}

export interface SummaryData {
  sentiment_distribution: Record<string, number>;
  emotion_distribution: Record<string, number>;
  sarcasm_percentage: number;
}

export interface AnalysisData {
  platform: string;
  total_comments: number;
  results: CommentResult[];
  summary: SummaryData;
  ai_summary?: string;
}
