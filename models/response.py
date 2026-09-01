# models/response.py —— 统一响应模型（model 层）
from pydantic import BaseModel


class ApiResponse(BaseModel):
    code: int
    msg: str
    data: object | None = None
