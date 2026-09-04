# auth.py —— Day14：API Key 鉴权依赖
# 作用：每个请求进来先查“钥匙”，没有或错了就返 401，对了才放行。
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings

# 从请求头 X-API-Key 取钥匙；auto_error=False：没带也不自己报错，交给下面判断
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(x_api_key: str | None = Depends(api_key_header)):
    # 没带钥匙，或钥匙不对 → 401（会被全局兜底网包成统一结构 {code:401,...}）
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少或错误的 API Key",
        )
    return x_api_key
