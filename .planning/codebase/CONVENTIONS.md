# Conventions

## Frontend
- **Linting:** Enforced via `eslint.config.js`. Uses React hooks and standard Vite TypeScript recommended rules.
- **Styling:** CSS classes are defined with semantic names (e.g., `.glow-card`, `.badge-positive`). Glassmorphic glow effects are widely used.
- **Components:** Functional components using React Hooks (`useState`, `useMemo`).
- **File Naming:** `.tsx` for React components.

## Backend
- **Type Hinting:** Extensive use of Python type hints supported by `typing` (`List`, `Dict`, `Optional`) and Pydantic models for request/response payloads.
- **Error Handling:** Standardized HTTP exceptions (`fastapi.HTTPException`) to relay error messages back to the client.
- **Logging:** Simple `print` statements are used at the moment for tracing execution.
