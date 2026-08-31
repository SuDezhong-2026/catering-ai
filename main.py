
# main.py —— 你的第一个 FastAPI 服务
from fastapi import FastAPI
from pydantic import BaseModel

# 创建一个"服务实例"，后面所有接口都挂它下面
app = FastAPI()
class ReceiptItem(BaseModel):
    name: str
    qty: float
    unit: str = "份"
    price: float


# @app.get("/hello") 是"装饰器"：告诉 FastAPI
# 当有人用 GET 方式访问网址 /hello 时，就执行下面这个函数
@app.get("/hello")
def say_hello():
    # return 一个字典，FastAPI 会自动把它变成 JSON 返回
    return {"msg": "你好，正斗！", "status": "ok"}

@app.post("/echo")
def echo(item: ReceiptItem):
    return {"you_sent": item}
