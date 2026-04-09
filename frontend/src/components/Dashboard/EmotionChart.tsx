import { useMemo } from 'react';
import { BarChart, Bar, Cell, Tooltip, ResponsiveContainer, XAxis, YAxis } from 'recharts';
interface CommentResult {
  text: string;
  sentiment: string;
  emotion: string;
  sarcastic: boolean;
  confidence: number;
}

interface EmotionChartProps {
  distribution: Record<string, number>;
  rawResults: CommentResult[];
}

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7f50', '#8dd1e1', '#a4de6c', '#d0ed57'];

const CustomTooltip = ({ active, payload, rawResults }: any) => {
  if (active && payload && payload.length) {
    const dataPoint = (payload as any[])[0].payload;
    const emotionName = dataPoint.name;
    const count = dataPoint.value;
    
    // Find a random sample review that matches the emotion
    const matchingReviews = rawResults.filter((r: any) => r.emotion === emotionName);
    const sampleText = matchingReviews.length > 0 
      ? matchingReviews[Math.floor(Math.random() * matchingReviews.length)].text 
      : "No review text available.";

    return (
      <div className="custom-tooltip" style={{ backgroundColor: '#2a2a2a', border: '1px solid #555', padding: '12px', borderRadius: '8px', maxWidth: '300px', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}>
        <p className="label" style={{ fontWeight: 'bold', margin: '0 0 8px 0', color: '#fff' }}>{`${emotionName} : ${count}`}</p>
        <p className="intro" style={{ fontSize: '0.85rem', fontStyle: 'italic', margin: 0, color: '#ddd' }}>"{sampleText}"</p>
      </div>
    );
  }
  return null;
};

export const EmotionChart: React.FC<EmotionChartProps> = ({ distribution, rawResults }) => {
  const chartData = useMemo(() => {
    return Object.entries(distribution || {}).map(([name, value]) => ({ name, value }));
  }, [distribution]);

  if (chartData.length === 0) return <p style={{ opacity: 0.5, textAlign: 'center' }}>No emotion data available</p>;

  return (
    <div style={{ width: '100%', height: 350 }}>
      <ResponsiveContainer>
        <BarChart data={chartData} margin={{ top: 20, right: 20, bottom: 40, left: 0 }}>
          <XAxis 
            dataKey="name" 
            stroke="#888" 
            tick={{ fill: '#ccc' }} 
            angle={-35} 
            textAnchor="end"
            height={60}
          />
          <YAxis stroke="#888" tick={{ fill: '#ccc' }} />
          <Tooltip 
            content={<CustomTooltip rawResults={rawResults} />} 
            cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }}
          />
          <Bar dataKey="value" isAnimationActive={true} animationDuration={1200} animationEasing="ease-out" radius={[4, 4, 0, 0]}>
            {chartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
