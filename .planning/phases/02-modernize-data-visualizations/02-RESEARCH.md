# Phase 2 Research: Modernize Data Visualizations

## Domain Patterns & Discoveries

1. **Existing Architecture**: 
   The current dashboard visualizations are entirely hardcoded HTML/CSS flexbox elements (using `simple-bar-chart`, `.bar-bg`, `.bar-fill`) located directly inside `App.tsx`. While `recharts` is installed in `package.json` (^3.8.1), it is currently unused.

2. **Component Refactor Pipeline**:
   Since `App.tsx` is sitting at 220 lines with monolithic rendering logic, the injection of Recharts logic MUST be compartmentalized. We will extract the charting logic into bespoke layout wrappers (e.g. `EmotionBreakdownChart.tsx`, `SentimentGauge.tsx`).

3. **Data Payload Utilization**:
   The `AnalysisData` structure provides rich arrays suitable for charts:
   - `<Tooltip>` Contextual text fetching: The raw `results: CommentResult[]` array contains the exact text fragments stringly mapped to sentiments.
   - Timeline Construction: We can map the `results` array index directly to sequential 'Review N' occurrences if temporal timestamps don't exist.

## Verification / Validation

- Component integration should be type-checked with `npm run tsc -b`.
- The Vite preview build must show no critical breaking prop-types warnings.

## Pitfalls & Recommendations

- **Tooltip Formatting limitations**: Standard `Recharts` `<Tooltip/>` only parses numbers. To implement the user's Contextual Text requirement, we must build a custom `TooltipContent` functional component mapping the payload values back to a random sample from `results: CommentResult[]` with matching criteria.
- **Animations constraints**: By user decision, we are omitting Framer Motion. We will exclusively use Recharts' built-in `isAnimationActive=true` combined with CSS `:hover` states and `@keyframes` for load transitions to guarantee lightweight payload sizes.
