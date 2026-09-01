# main.py —— Day6 Part A：统一响应 + 全局异常处理
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# 创建服务实例，后面所有接口都挂它下面
app = FastAPI()


# ① 统一响应模型：所有接口都返回这个结构
class ApiResponse(BaseModel):
    code: int
    msg: str
    data: object | None = None


# ② 收货单模型（Day5 已有，移到前面更规范）
class ReceiptItem(BaseModel):
    name: str
    qty: float
    unit: str = "份"
    price: float


# ③ 兜底网1：Pydantic 校验失败（原本裸 422）→ 包成统一格式
@app.exception_handler(RequestValidationError)
def handle_validation_error(request, exc):
    return JSONResponse(
        status_code=422,
        content=ApiResponse(code=422, msg="参数校验失败", data=exc.errors()).model_dump(),
    )


# ④ 兜底网2：主动抛的 HTTPException → 统一格式
@app.exception_handler(HTTPException)
def handle_http_error(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(code=exc.status_code, msg=str(exc.detail), data=None).model_dump(),
    )


# ⑤ 兜底网3：任何没料到的异常 → 统一 500，不裸奔
@app.exception_handler(Exception)
def handle_unexpected_error(request, exc):
    return JSONResponse(
        status_code=500,
        content=ApiResponse(code=500, msg="服务器内部错误，请联系管理员", data=None).model_dump(),
    )


# ⑥ 正常接口，统一用 ApiResponse 包裹
@app.get("/hello")
def hello():
    return ApiResponse(code=0, msg="ok", data={"msg": "你好，正斗！"})


@app.post("/echo")
def echo(item: dict):
    return ApiResponse(code=0, msg="ok", data={"you_sent": item})


@app.post("/items")
def create_item(item: ReceiptItem):
    total = item.qty * item.price
    return ApiResponse(code=0, msg="ok", data={"name": item.name, "total": total})


# ⑦ 测试用：故意制造一个会崩的接口（验证兜底网3）
@app.get("/boom")
def boom():
    return 1 / 0  # 除零异常，会被 handle_unexpected_error 接住
