from middleware import setup_logging, LoggingMiddleware   # ← 加在顶部 import 区

# main.py —— Day8 入口：创建 app + 挂异常 + 注册路由（不再含业务）
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models.response import ApiResponse
from routers.items import router
setup_logging()                 # ← 放在 app = FastAPI() 之前
app = FastAPI()
app.include_router(router)   # 把 routers/items.py 里的接口全部挂上来
app.add_middleware(LoggingMiddleware)   # ← 放在 include_router 之前/之后都行
app.include_router(router)

@app.exception_handler(RequestValidationError)
def handle_validation_error(request, exc):
    return JSONResponse(status_code=422, content=ApiResponse(code=422, msg="参数校验失败", data=exc.errors()).model_dump())


@app.exception_handler(HTTPException)
def handle_http_error(request, exc):
    return JSONResponse(status_code=exc.status_code, content=ApiResponse(code=exc.status_code, msg=str(exc.detail), data=None).model_dump())


@app.exception_handler(Exception)
def handle_unexpected_error(request, exc):
    return JSONResponse(status_code=500, content=ApiResponse(code=500, msg="服务器内部错误，请联系管理员", data=None).model_dump())
