"""Fleet Health Dashboard - single-page status for subtiliorars-sys services."""

import os
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Fleet Health Dashboard", version="0.1.0")

SERVICES = {
    # --- Fleet / Infrastructure ---
    "Backoffice MCP (office)": {"url": "http://desktop-cjtcaqf.tail9ef210.ts.net:3000/health", "type": "health", "repo": "subtiliorars-sys/backoffice-mcp-server", "note": "Office PC primary; Tailscale DNS"},
    "Backoffice MCP (fly)":  {"url": "https://backoffice-mcp-server.fly.dev/health", "type": "health", "repo": "subtiliorars-sys/backoffice-mcp-server", "note": "Fly fallback; cold-start ~10-20s"},
    "Fleet Health":          {"url": "https://fleet-health.fly.dev/health", "type": "health", "repo": "subtiliorars-sys/fleet-health", "note": "This dashboard; Fly suspended 2026-07-15"},

    # --- OmniVerse / OmniTender ---
    "OmniVerse (OmniTender)":{"url": "https://omnitender.fly.dev/health", "type": "health", "repo": "subtiliorars-sys/OmniVerse", "note": "Telegram bot + SMS + WhatsApp + mail + CRM relay"},
    "OmniTender CRM":        {"url": "https://omnitender-crm.fly.dev/health", "type": "web",   "repo": "subtiliorars-sys/OmniTenderCRM", "note": "Mail + leads active"},
    "OmniTender Exchange":   {"url": "https://omnitender-exchange.fly.dev/health", "type": "health", "repo": "subtiliorars-sys/OmniTender", "note": "Exchange API; DB + Redis OK"},
    "OmniTender Exch Web":   {"url": "https://omnitender-exchange-web.fly.dev/health", "type": "web",   "repo": "subtiliorars-sys/omnitender-web", "note": "Exchange web frontend"},

    # --- Meniscus Maximus ---
    "Meniscus Maximus":      {"url": "https://system32-autumn-tide-1990.fly.dev/", "type": "web",   "repo": "subtiliorars-sys/MeniscusMaximus", "note": "No /health endpoint; serves HTML OK"},
    "MM Preview":            {"url": "https://meniscusmaximus-preview.fly.dev/", "type": "web",   "repo": "subtiliorars-sys/MeniscusMaximus-Preview", "note": "Preview deploy (check)"},

    # --- Suspended (cost-saving) ---
    "CodeMonkeys":           {"url": "https://codemonkeys.fly.dev/healthz", "type": "health", "repo": "subtiliorars-sys/CodeMonkeys", "note": "SUSPENDED 2026-07-20"},
    "OmniSecure API":        {"url": "https://omnisecure-api.fly.dev/health", "type": "health", "repo": "subtiliorars-sys/OmniSecure", "note": "SUSPENDED 2026-07-02"},
    "Cairn":                 {"url": "https://trycairn.fly.dev/", "type": "web",   "repo": "subtiliorars-sys/Cairn", "note": "SUSPENDED 2026-07-18"},
    "Driving Me Nuts":       {"url": "https://driving-me-nuts.fly.dev/", "type": "web",   "repo": "subtiliorars-sys/DrivingMeNuts", "note": "SUSPENDED 2026-06-11"},
    "Crypto Exchange":       {"url": "https://backend-lucid-harbor-7653.fly.dev/api/v1/health", "type": "health", "repo": "subtiliorars-sys/crypto", "note": "SUSPENDED 2026-07-15"},
    "Omni Herald":           {"url": "https://omni-herald.fly.dev/health", "type": "health", "repo": "subtiliorars-sys/omni-herald", "note": "SUSPENDED 2026-06-11"},
}

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
GITHUB_OWNER = "subtiliorars-sys"

# Repos to track PRs and issues for (active, prioritized)
REPOS = [
    "neural-network",
    "AgentCorps",
    "backoffice-mcp-server",
    "fleet-health",
    "OmniTender",
    "OmniTenderCRM",
    "omnitender-web",
    "OmniVerse",
    "OmniRails",
    "OmniWash",
    "OmniCater",
    "OmniLocal",
    "OmniSecure",
    "OmniAuth",
    "OmniDesk",
    "MeniscusMaximus",
    "CodeMonkeys",
    "Cairn",
    "TradeGame",
    "PixelSports",
    "Clean-Sheet",
    "jimmythehat-volunteers",
    "GameAds",
    "crypto",
    "scribe-dictation",
    "ebay-dropship-automation",
    "DrivingMeNuts",
    "yes-man",
    "Bocce",
    "Volleyball",
    "Curling",
]


async def check_health(url: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            return {"url": url, "status": resp.status_code, "ok": resp.status_code < 500, "latency_ms": resp.elapsed.total_seconds() * 1000}
    except Exception as e:
        return {"url": url, "status": 0, "ok": False, "error": str(e)}


async def fetch_prs(repo: str) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/pulls", headers=GITHUB_HEADERS, params={"state": "open", "per_page": 5})
            if resp.status_code == 200:
                return [{"number": pr["number"], "title": pr["title"], "author": pr["user"]["login"], "url": pr["html_url"], "draft": pr.get("draft", False)} for pr in resp.json()]
    except Exception:
        pass
    return []


async def fetch_issues(repo: str) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/issues", headers=GITHUB_HEADERS, params={"state": "open", "per_page": 5, "labels": "status:todo"})
            if resp.status_code == 200:
                return [{"number": i["number"], "title": i["title"], "url": i["html_url"], "labels": [l["name"] for l in i.get("labels", [])]} for i in resp.json() if "pull_request" not in i]
    except Exception:
        pass
    return []


@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.get("/api/status")
async def api_status():
    results = {}
    for n, s in SERVICES.items():
        r = await check_health(s["url"])
        r["note"] = s.get("note", "")
        r["repo"] = s.get("repo", "")
        results[n] = r
    prs = {r: await fetch_prs(r) for r in REPOS}
    issues = {r: await fetch_issues(r) for r in REPOS}
    return {
        "services": results,
        "summary": {"total_repos": len(REPOS), "open_prs": sum(len(v) for v in prs.values()), "todo_issues": sum(len(v) for v in issues.values())},
        "prs": prs, "issues": issues,
        "updated": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    html_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
    try:
        with open(html_path, encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>Dashboard</h1><p>dashboard.html not found</p>")
