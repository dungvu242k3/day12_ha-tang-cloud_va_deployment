"""
Rate Limiter Module — Simple In-memory Sliding Window
"""
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
    logger.info("Rate Limiter: Connected to Redis")
except Exception as e:
    logger.warning(f"Rate Limiter: Redis connection failed ({e}). Falling back to In-Memory.")
    redis_client = None

# Fallback lưu trữ cục bộ
_rate_windows: dict[str, list[float]] = {}

def check_rate_limit(key: str):
    """
    Kiểm tra giới hạn lưu lượng (Rate Limit) sử dụng Redis (Stateless)
    hoặc In-memory (Stateful) nếu Redis lỗi.
    """
    now = time.time()
    limit = settings.rate_limit_per_minute
    redis_key = f"rl:{key}"

    if redis_client:
        try:
            # Sử dụng Redis Transaction để đảm bảo tính nguyên tử
            pipe = redis_client.pipeline()
            # Xóa các request đã cũ (quá 60s)
            pipe.zremrangebyscore(redis_key, 0, now - 60)
            # Đếm số lượng request hiện tại
            pipe.zcard(redis_key)
            # Thêm request hiện tại
            pipe.zadd(redis_key, {str(now): now})
            # Thiết lập TTL cho key
            pipe.expire(redis_key, 60)
            
            results = pipe.execute()
            current_count = results[1]

            if current_count >= limit:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded: {limit} req/min (Stateless)",
                    headers={"Retry-After": "60"},
                )
            return
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Redis Rate Limiter Error: {e}")

    # --- Fallback to In-Memory ---
    if key not in _rate_windows:
        _rate_windows[key] = []
        
    window = _rate_windows[key]
    _rate_windows[key] = [t for t in window if t > now - 60]
    
    if len(_rate_windows[key]) >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {limit} req/min (In-Memory)",
            headers={"Retry-After": "60"},
        )
    
    _rate_windows[key].append(now)
