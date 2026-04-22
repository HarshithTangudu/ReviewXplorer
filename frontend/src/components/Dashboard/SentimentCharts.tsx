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

const GAUGE_COLORS = ['#ef4444', '#a1a1aa', '#22c55e']; // Negative, Neutral, Positive

export const SentimentGauge: React.FC<SentimentGaugeProps> = ({ distribution }) => {
  const data = useMemo(() => {
    // Normalize keys to support various casing from backend
    const normalized: Record<string, number> = {};
    Object.entries(distribution || {}).forEach(([key, val]) => {
      normalized[key.toUpperCase()] = val;
    });

    return [
      { name: 'Negative', value: normalized['NEGATIVE'] || 0 },
      { name: 'Neutral', value: normalized['NEUTRAL'] || 0 },
      { name: 'Positive', value: normalized['POSITIVE'] || 0 },
    ];
  }, [distribution]);

  const total = data.reduce((acc, curr) => acc + curr.value, 0);
  if (total === 0) return <p style={{ opacity: 0.5, textAlign: 'center' }}>No sentiment data available</p>;

  const positiveValue = data.find(d => d.name === 'Positive')?.value || 0;

  return (
    <div style={{ width: '100%', height: 260, position: 'relative' }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="85%"
            startAngle={180}
            endAngle={0}
            innerRadius={80}
            outerRadius={120}
            paddingAngle={2}
            dataKey="value"
            isAnimationActive={true}
            animationDuration={1000}
          >
            {data.map((entry, index) => {
              const colorMap: any = { 'Negative': GAUGE_COLORS[0], 'Neutral': GAUGE_COLORS[1], 'Positive': GAUGE_COLORS[2] };
              return <Cell key={`cell-${index}`} fill={colorMap[entry.name]} />;
            })}
          </Pie>
          <Tooltip 
            contentStyle={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '8px', color: '#fafafa' }}
            itemStyle={{ color: '#fafafa' }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ 
        position: 'absolute', 
        bottom: '15%', 
        left: '50%', 
        transform: 'translateX(-50%)', 
        textAlign: 'center' 
      }}>
        <div style={{ fontSize: '2rem', fontWeight: '700', color: '#fafafa' }}>
          {total > 0 ? Math.round((positiveValue / total) * 100) : 0}%
        </div>
        <div style={{ fontSize: '0.875rem', color: '#a1a1aa', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Positive
        </div>
      </div>
    </div>
  );
};

export const SentimentTimeline: React.FC<SentimentTimelineProps> = ({ rawResults }) => {
  const data = useMemo(() => {
    return rawResults.map((r, i) => {
      let score = 0;
      const sent = r.sentiment.toUpperCase();
      if (sent === 'POSITIVE') score = 1;
      else if (sent === 'NEGATIVE') score = -1;
      
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
        <div style={{ backgroundColor: '#18181b', border: '1px solid #27272a', padding: '12px', borderRadius: '8px', maxWidth: '280px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
          <p style={{ fontWeight: '600', margin: '0 0 6px 0', color: '#fafafa' }}>{p.index} <span style={{opacity: 0.7, fontWeight: 'normal'}}>({p.fullSentiment})</span></p>
          <p style={{ fontSize: '0.875rem', fontStyle: 'italic', margin: 0, color: '#a1a1aa', lineHeight: 1.5 }}>"{p.text}"</p>
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
              <stop offset="5%" stopColor="#22c55e" stopOpacity={0.5}/>
              <stop offset="95%" stopColor="#ef4444" stopOpacity={0.1}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" opacity={0.1} vertical={false} />
          <XAxis dataKey="index" hide />
          <YAxis domain={[-1.2, 1.2]} ticks={[-1, 0, 1]} tickFormatter={(v) => v === 1 ? 'Pos' : v === -1 ? 'Neg' : 'Neu'} stroke="#a1a1aa" tick={{fontSize: 12}} />
          <Tooltip content={<CustomTimelineTooltip />} />
          <Area 
            type="monotoneX" 
            dataKey="score" 
            stroke="#3b82f6" 
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
