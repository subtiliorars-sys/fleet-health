# Fleet Health Dashboard

Single-page status dashboard for all subtiliorars-sys services, PRs, and kanban issues.

## Quick start

```bash
uv run uvicorn main:app --reload --port 8091
```

## API

- `GET /` — HTML dashboard
- `GET /api/status` — JSON status
- `GET /health` — health check

## Deploy

```bash
fly launch
fly deploy
```
