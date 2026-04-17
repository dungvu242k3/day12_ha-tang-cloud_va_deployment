"""
Cost Guard Module — Budget Protection for LLM usage
"""
import time
import logging
from fastapi import HTTPException
from app.config import settings

import time
import logging
from redis import Redis
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

# Khởi tạo Redis client
try:
    redis_client = Redis.from_url(settings.redis_url, socket_timeout=settings.redis_timeout)
    redis_client.ping()
    logger.info("Cost Guard: Connected to Redis")
except Exception as e:
    logger.warning(f"Cost Guard: Redis connection failed ({e}). Falling back to In-Memory.")
    redis_client = None

# Fallback lưu trữ cục bộ
_daily_cost = 0.0
_cost_reset_day = time.strftime("%Y-%m-%d")

def check_and_record_cost(input_tokens: int, output_tokens: int):
    """
    Kiểm tra và ghi nhận chi phí sử dụng.
    Sử dụng Redis (Stateless) hoặc In-memory làm fallback.
    """
    global _daily_cost, _cost_reset_day
    
    today = time.strftime("%Y-%m-%d")
    cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006
    budget = settings.daily_budget_usd

    # --- Redis Implementation ---
    if redis_client:
        try:
            redis_key = f"cost:{today}"
            # Cộng dồn chi phí vào Redis
            current_cost = redis_client.incrbyfloat(redis_key, cost)
            # Thiết lập expire cho key (48h để audit)
            redis_client.expire(redis_key, 172800)

            if current_cost >= budget:
                logger.warning(f"Stateless Budget exceeded! Used: {current_cost}, Limit: {budget}")
                raise HTTPException(503, "Daily budget exhausted (Stateless). Try tomorrow.")
            
            return current_cost
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Redis Cost Guard Error: {e}")

    # --- Fallback to In-Memory ---
    if today != _cost_reset_day:
        _daily_cost = 0.0
        _cost_reset_day = today
    
    if _daily_cost >= budget:
        raise HTTPException(503, "Daily budget exhausted (In-Memory). Try tomorrow.")
    
    _daily_cost += cost
    return _daily_cost

def get_current_usage():
    """Lấy thông tin sử dụng hiện tại."""
    today = time.strftime("%Y-%m-%d")
    budget = settings.daily_budget_usd
    
    current = _daily_cost
    if redis_client:
        try:
            val = redis_client.get(f"cost:{today}")
            if val:
                current = float(val)
        except:
            pass
            
    return {
        "daily_cost_usd": round(current, 4),
        "daily_budget_usd": budget,
        "is_exhausted": current >= budget
    }
