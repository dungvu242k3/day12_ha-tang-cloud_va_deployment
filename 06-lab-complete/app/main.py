"""
Production AI Agent — Kết hợp tất cả Day 12 concepts

Checklist:
  ✅ Config từ environment (12-factor)
  ✅ Structured JSON logging
  ✅ API Key authentication
  ✅ Rate limiting
  ✅ Cost guard
  ✅ Input validation (Pydantic)
  ✅ Health check + Readiness probe
  ✅ Graceful shutdown
  ✅ Security headers
  ✅ CORS
  ✅ Error handling
"""
import os
import time
import signal
import logging
import json
from datetime import datetime, timezone
from collections import defaultdict, deque
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Security, Depends, Request, Response
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from app.config import settings

# Mock LLM (thay bằng OpenAI/Anthropic khi có API key)
from utils.mock_llm import ask as llm_ask

# ─────────────────────────────────────────────────────────
# Logging — JSON structured
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
_is_ready = False
_request_count = 0
_error_count = 0

# Auth, Rate Limiter, Cost Guard
from app.auth import verify_api_key
from app.rate_limiter import check_rate_limit
from app.cost_guard import check_and_record_cost, get_current_usage

# ─────────────────────────────────────────────────────────
# Logging — JSON structured
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
_is_ready = False
_request_count = 0
_error_count = 0

# ─────────────────────────────────────────────────────────
# Lifespan
# ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    logger.info(json.dumps({
        "event": "startup",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }))
    time.sleep(0.1)  # simulate init
    _is_ready = True
    logger.info(json.dumps({"event": "ready"}))

    yield

    _is_ready = False
    logger.info(json.dumps({"event": "shutdown"}))

# ─────────────────────────────────────────────────────────
# App
# ─────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    global _request_count, _error_count
    start = time.time()
    _request_count += 1
    try:
        response: Response = await call_next(request)
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        if "server" in response.headers:
            del response.headers["server"]
        duration = round((time.time() - start) * 1000, 1)
        logger.info(json.dumps({
            "event": "request",
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "ms": duration,
        }))
        return response
    except Exception as e:
        _error_count += 1
        logger.error(json.dumps({"event": "error", "msg": str(e)}))
        raise

# ─────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50,
                        description="Unique ID for the user/conversation session")
    question: str = Field(..., min_length=1, max_length=2000,
                          description="Your question for the agent")

class AskResponse(BaseModel):
    user_id: str
    question: str
    answer: str
    model: str
    timestamp: str
    usage: dict

# ─────────────────────────────────────────────────────────
# Redis History Helper
# ─────────────────────────────────────────────────────────
from redis import Redis
_redis_history = None
try:
    _redis_history = Redis.from_url(settings.redis_url, socket_timeout=settings.redis_timeout)
    _redis_history.ping()
except:
    _redis_history = None

# ─────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────

@app.get("/", tags=["Info"])
def root():
    return {
        "app": settings.app_name,
        "status": "online",
        "stateless": _redis_history is not None
    }


@app.post("/ask", response_model=AskResponse, tags=["Agent"])
async def ask_agent(
    body: AskRequest,
    request: Request,
    _key: str = Depends(verify_api_key),
):
    """
    Send a question to the AI agent with conversation context.
    
    **Context:** Agent will try to remember the last 5 messages for the given `user_id`.
    """
    # Rate limit & Budget check
    check_rate_limit(_key[:8])
    input_tokens = len(body.question.split()) * 2
    check_and_record_cost(input_tokens, 0)

    # 1. Retrieve history from Redis
    history_key = f"hist:{body.user_id}"
    context = ""
    if _redis_history:
        try:
            # Lấy 5 tin nhắn gần nhất
            past_messages = _redis_history.lrange(history_key, 0, 4)
            if past_messages:
                context = "\n".join([m.decode('utf-8') for m in reversed(past_messages)])
        except Exception as e:
            logger.error(f"History retrieval error: {e}")

    # 2. Call LLM with context
    prompt = f"Context:\n{context}\n\nQuestion: {body.question}" if context else body.question
    answer = llm_ask(prompt)

    # 3. Save new message to history
    if _redis_history:
        try:
            new_entry = f"User: {body.question} | Agent: {answer}"
            _redis_history.lpush(history_key, new_entry)
            _redis_history.ltrim(history_key, 0, 9)  # Keep last 10 entries
            _redis_history.expire(history_key, 3600)  # Expire in 1h
        except Exception as e:
            logger.error(f"History save error: {e}")

    # Record output tokens
    output_tokens = len(answer.split()) * 2
    usage_info = check_and_record_cost(0, output_tokens)

    return AskResponse(
        user_id=body.user_id,
        question=body.question,
        answer=answer,
        model=settings.llm_model,
        timestamp=datetime.now(timezone.utc).isoformat(),
        usage={
            "daily_cost_usd": round(usage_info, 4),
            "budget_usd": settings.daily_budget_usd
        }
    )


@app.get("/health", tags=["Operations"])
def health():
    """Liveness probe. Platform restarts container if this fails."""
    status = "ok"
    checks = {"llm": "mock" if not settings.openai_api_key else "openai"}
    return {
        "status": status,
        "version": settings.app_version,
        "environment": settings.environment,
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "total_requests": _request_count,
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready", tags=["Operations"])
def ready():
    """Readiness probe. Load balancer stops routing here if not ready."""
    if not _is_ready:
        raise HTTPException(503, "Not ready")
    return {"ready": True}


@app.get("/metrics", tags=["Operations"])
def metrics(_key: str = Depends(verify_api_key)):
    """Basic metrics (protected)."""
    usage = get_current_usage()
    return {
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "total_requests": _request_count,
        "error_count": _error_count,
        "daily_cost_usd": usage["daily_cost_usd"],
        "daily_budget_usd": usage["daily_budget_usd"],
        "budget_used_pct": round(usage["daily_cost_usd"] / usage["daily_budget_usd"] * 100, 1) if usage["daily_budget_usd"] > 0 else 0,
    }


# ─────────────────────────────────────────────────────────
# Graceful Shutdown
# ─────────────────────────────────────────────────────────
def _handle_signal(signum, _frame):
    logger.info(json.dumps({"event": "signal", "signum": signum}))

signal.signal(signal.SIGTERM, _handle_signal)


if __name__ == "__main__":
    logger.info(f"Starting {settings.app_name} on {settings.host}:{settings.port}")
    logger.info(f"API Key: {settings.agent_api_key[:4]}****")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        timeout_graceful_shutdown=30,
    )
