import React, { useMemo } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

interface CommentResult {
  text: string;
  sentiment: string;
  emotion: string;
  sarcastic: boolean;
  confidence: number;
}

interface SentimentGaugeProps {
  distribution: Record<string, number>;
}

interface SentimentTimelineProps {
  rawResults: CommentResult[];
}

const GAUGE_COLORS = ['#ff4d4d', '#8884d8', '#4caf50']; // Negative, Neutral, Positive

export const SentimentGauge: React.FC<SentimentGaugeProps> = ({ distribution }) => {
  const data = useMemo(() => {
    return [
      { name: 'Negative', value: distribution['Negative'] || 0 },
      { name: 'Neutral', value: distribution['Neutral'] || 0 },
      { name: 'Positive', value: distribution['Positive'] || 0 },
    ].filter(d => d.value > 0);
  }, [distribution]);

  if (data.length === 0) return <p style={{ opacity: 0.5, textAlign: 'center' }}>No gauge data available</p>;

  return (
    <div style={{ width: '100%', height: 260, position: 'relative' }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="100%"
            startAngle={180}
            endAngle={0}
            innerRadius={70}
            outerRadius={120}
            paddingAngle={3}
            dataKey="value"
            isAnimationActive={true}
            animationDuration={1500}
            animationEasing="ease-out"
          >
            {data.map((entry, index) => {
              const colorMap: any = { 'Negative': GAUGE_COLORS[0], 'Neutral': GAUGE_COLORS[1], 'Positive': GAUGE_COLORS[2] };
              return <Cell key={`cell-${index}`} fill={colorMap[entry.name] || '#888'} />;
            })}
          </Pie>
          <Tooltip 
            contentStyle={{ backgroundColor: '#2a2a2a', border: '1px solid #555', borderRadius: '8px', color: '#fff' }}
            itemStyle={{ color: '#fff' }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export const SentimentTimeline: React.FC<SentimentTimelineProps> = ({ rawResults }) => {
  const data = useMemo(() => {
    return rawResults.map((r, i) => {
      let score = 0;
      if (r.sentiment === 'Positive') score = 1;
      else if (r.sentiment === 'Negative') score = -1;
      
      return {
        index: `Rev ${i+1}`,
        score,
        text: r.text,
        fullSentiment: r.sentiment
      };
    });
  }, [rawResults]);

  const CustomTimelineTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const p = payload[0].payload;
      return (
        <div style={{ backgroundColor: '#2a2a2a', border: '1px solid #555', padding: '12px', borderRadius: '8px', maxWidth: '280px', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}>
          <p style={{ fontWeight: 'bold', margin: '0 0 5px 0', color: '#fff' }}>{p.index} <span style={{opacity: 0.7, fontWeight: 'normal'}}>({p.fullSentiment})</span></p>
          <p style={{ fontSize: '0.85rem', fontStyle: 'italic', margin: 0, color: '#ddd' }}>"{p.text}"</p>
        </div>
      );
    }
    return null;
  };

  if (data.length === 0) return <p style={{ opacity: 0.5, textAlign: 'center' }}>No timeline data available</p>;

  return (
    <div style={{ width: '100%', height: 260 }}>
      <ResponsiveContainer>
        <AreaChart data={data} margin={{ top: 20, right: 20, bottom: 0, left: -20 }}>
          <defs>
            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#4caf50" stopOpacity={0.5}/>
              <stop offset="95%" stopColor="#ff4d4d" stopOpacity={0.1}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" opacity={0.1} vertical={false} />
          <XAxis dataKey="index" hide />
          <YAxis domain={[-1.2, 1.2]} ticks={[-1, 0, 1]} tickFormatter={(v) => v === 1 ? 'Pos' : v === -1 ? 'Neg' : 'Neu'} stroke="#888" tick={{fontSize: 12}} />
          <Tooltip content={<CustomTimelineTooltip />} />
          <Area 
            type="monotoneX" 
            dataKey="score" 
            stroke="#8884d8" 
            strokeWidth={2}
            fillOpacity={1} 
            fill="url(#colorScore)" 
            isAnimationActive={true} 
            animationDuration={1500} 
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
