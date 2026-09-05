# middleware.py —— Day18：结构化日志中间件
# 作用：给每个请求发唯一 request_id，记录「收到→处理→返回(含耗时)」，
#       出错时把堆栈也带上同一个 request_id；用 ID 就能拼出一次请求的完整日志。
import time, uuid, logging, traceback
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware

# contextvars：请求级别的「全局变量」，一次请求内任何地方打日志都能拿到同一 ID
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")

class RequestIDFilter(logging.Filter):
    # 过滤器：把当前请求的 request_id 塞进每一条日志记录
    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True

def setup_logging():
    fmt = "%(asctime)s | %(levelname)s | req_id=%(request_id)s | %(message)s"
    handler = logging.StreamHandler()          # 输出到控制台
    handler.setFormatter(logging.Formatter(fmt))
    handler.addFilter(RequestIDFilter())       # 每条日志都带 request_id
    logger = logging.getLogger("catering")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = uuid.uuid4().hex[:12]            # 1) 这次请求的唯一 ID
        request_id_ctx.set(rid)
        logger = logging.getLogger("catering")
        start = time.perf_counter()
        logger.info(f"▶ 收到请求 {request.method} {request.url.path}")  # 2) 请求进来
        try:
            response = await call_next(request)
        except Exception:
            logger.error(f"✖ 请求处理异常:\n{traceback.format_exc()}")  # 3) 出错记堆栈
            raise
        cost_ms = (time.perf_counter() - start) * 1000
        logger.info(f"◀ 请求完成 status={response.status_code} 耗时={cost_ms:.1f}ms")  # 4) 结束+耗时
        return response
