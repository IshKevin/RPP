from __future__ import annotations

from fastapi import FastAPI

from .models import BookInput, LaunchPack, HealthResponse
from .generator import build_launch_pack

app = FastAPI(title="RevenuePressAI Engine", version="1.4", docs_url="/docs")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=app.version)


@app.post("/launch-pack", response_model=LaunchPack)
def launch_pack(payload: BookInput) -> LaunchPack:
    return build_launch_pack(payload)
