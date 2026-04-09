import axios from 'axios';
import type { AnalysisData } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export const analyzeUrl = async (url: string): Promise<AnalysisData> => {
  const response = await axios.post(`${API_BASE_URL}/analyze`, { url });
  return response.data;
};
