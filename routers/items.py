# routers/items.py —— 接口路由（router 层）
# 路由层只负责：收请求 → 调 service → 用 ApiResponse 包好返回。不写任何业务计算。
from fastapi import APIRouter
from models.receipt import ReceiptItem
from models.response import ApiResponse
from services.receipt_service import build_item_result
from config import settings

router = APIRouter()


@router.get("/hello")
def hello():
    return ApiResponse(code=0, msg="ok", data={"app_name": settings.app_name, "debug": settings.debug})


@router.post("/echo")
def echo(item: dict):
    return ApiResponse(code=0, msg="ok", data={"you_sent": item})


@router.post("/items")
def create_item(item: ReceiptItem):
    result = build_item_result(item)   # 业务交给 service 层
    return ApiResponse(code=0, msg="ok", data=result)


@router.get("/boom")
def boom():
    return 1 / 0   # 故意制造异常，验证全局兜底网（测试用）
