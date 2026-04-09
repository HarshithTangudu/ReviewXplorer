# 02-02 Summary: Sentiment Gauge and Timeline

## Objective Complete
Constructed new dynamic Sentiment views utilizing high-end data mapping with `recharts`.

## Key Updates
- Built `SentimentCharts.tsx`.
- Added `<SentimentGauge>` employing a 180-degree `<PieChart>` geometry to map Positive to Negative.
- Added `<SentimentTimeline>` rendering an `<AreaChart>` that sweeps over the sequential `results[]` array, utilizing X-axes spacing to dynamically render individual comment sentiment impact.
- Created beautiful customized area drop-gradients and textual tooltips detailing each comment dynamically.
