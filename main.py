"""Fleet Health Dashboard - single-page status for subtiliorars-sys services."""

import os
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Fleet Health Dashboard", version="0.1.0")

SERVICES = {
    "CodeMonkeys": {"url": "https://codemonkeys.fly.dev/healthz", "type": "health", "repo": "subtiliorars-sys/CodeMonkeys"},
    "OmniTender CRM": {"url": "https://omnitender-crm.fly.dev/", "type": "web", "repo": "subtiliorars-sys/OmniTenderCRM"},
}

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
GITHUB_OWNER = "subtiliorars-sys"
REPOS = ["CodeMonkeys","OmniTender","OmniTenderCRM","crypto","scribe-dictation","jimmythehat-volunteers","neural-network"]


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
    results = {n: await check_health(s["url"]) for n, s in SERVICES.items()}
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
