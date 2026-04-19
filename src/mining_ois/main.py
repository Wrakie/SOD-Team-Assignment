from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from mining_ois.api.routes import router
from mining_ois.db.database import init_db, seed_demo_data

app = FastAPI(
    title="Mining Operational Information System",
    version="0.1.0",
    description="Prototype OIS for production, maintenance, safety, and inventory workflows.",
)

web_dir = Path(__file__).resolve().parent / "web"

app.add_middleware(SessionMiddleware, secret_key="mining-ois-demo-secret-key")


@app.on_event("startup")
def startup() -> None:
    init_db()
    seed_demo_data()


app.include_router(router)
app.mount("/ui", StaticFiles(directory=str(web_dir), html=True), name="ui")


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/ui/")
