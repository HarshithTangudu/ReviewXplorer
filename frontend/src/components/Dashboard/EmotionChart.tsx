import { useMemo } from 'react';
import { 
  BarChart, Bar, Cell, Tooltip, ResponsiveContainer, XAxis, YAxis,
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis 
} from 'recharts';
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

const COLORS = ['#6366f1', '#3b82f6', '#0ea5e9', '#06b6d4', '#14b8a6', '#10b981', '#8b5cf6'];

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
      <div className="custom-tooltip" style={{ backgroundColor: '#18181b', border: '1px solid #27272a', padding: '12px', borderRadius: '8px', maxWidth: '300px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)' }}>
        <p className="label" style={{ fontWeight: '600', margin: '0 0 8px 0', color: '#fafafa', textTransform: 'capitalize' }}>{`${emotionName} : ${count}`}</p>
        <p className="intro" style={{ fontSize: '0.875rem', fontStyle: 'italic', margin: 0, color: '#a1a1aa', lineHeight: 1.5 }}>"{sampleText}"</p>
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

export const EmotionRadar: React.FC<EmotionChartProps> = ({ distribution, rawResults }) => {
  const chartData = useMemo(() => {
    return Object.entries(distribution || {}).map(([name, value]) => ({ 
      name: name.charAt(0).toUpperCase() + name.slice(1), 
      value 
    }));
  }, [distribution]);

  if (chartData.length === 0) return null;

  return (
    <div style={{ width: '100%', height: 350 }}>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
          <PolarGrid stroke="#444" />
          <PolarAngleAxis dataKey="name" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
          <PolarRadiusAxis hide />
          <Radar
            name="Emotions"
            dataKey="value"
            stroke="#6366f1"
            fill="#6366f1"
            fillOpacity={0.6}
            isAnimationActive={true}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '8px', color: '#fafafa' }}
            itemStyle={{ color: '#fafafa' }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
