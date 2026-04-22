import React, { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface WordCloudProps {
  texts: string[];
}

const STOP_WORDS = new Set([
  'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'to', 'for', 'in', 'at', 'by', 'of', 'with', 'from', 'it', 'its', 'that', 'this', 'on', 'as', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'my', 'your', 'his', 'her', 'their', 'we', 'us', 'i', 'you', 'he', 'she', 'it', 'they', 'me', 'him', 'them', 'if', 'then', 'else', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now', 'very', 're', 've', 'll', 'd', 'm', 'o', 't', 'y', 'amazon', 'flipkart', 'product', 'review', 'buy', 'bought', 'get', 'got'
]);

const COLORS = ['#6366f1', '#3b82f6', '#0ea5e9', '#06b6d4', '#14b8a6', '#10b981', '#8b5cf6'];

export const WordCloud: React.FC<WordCloudProps> = ({ texts }) => {
  const wordData = useMemo(() => {
    const counts: Record<string, number> = {};
    
    texts.forEach(text => {
      const words = text.toLowerCase()
        .replace(/[^\w\s]/g, '')
        .split(/\s+/)
        .filter(w => w.length > 3 && !STOP_WORDS.has(w));
      
      words.forEach(word => {
        counts[word] = (counts[word] || 0) + 1;
      });
    });

    return Object.entries(counts)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 12);
  }, [texts]);

  if (wordData.length === 0) return null;

  return (
    <div style={{ width: '100%', height: 350 }}>
      <ResponsiveContainer>
        <BarChart
          layout="vertical"
          data={wordData}
          margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
        >
          <XAxis type="number" hide />
          <YAxis 
            type="category" 
            dataKey="name" 
            stroke="#a1a1aa" 
            fontSize={12} 
            width={80}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '8px', color: '#fafafa' }}
            itemStyle={{ color: '#fafafa' }}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {wordData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
