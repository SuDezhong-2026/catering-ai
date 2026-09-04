# tests/test_items.py —— Day 13 单元测试
# 作用：用 pytest 自动验证接口行为，以后改代码一跑测试就知道有没有改坏。
import sys
import os

# tests/ 在子目录，main.py 在项目根。把这行加进路径，测试才能 `from main import app`。
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from config import settings
# TestClient 是 FastAPI 自带的“假浏览器”：不发真实网络请求，直接调你的 app。
# raise_server_exceptions=False：让 TestClient 不把 500 异常再抛出来，
# 这样我们才能“看到”全局兜底网返回的统一 500 结构（否则测试会直接报错退出）。
client = TestClient(app, raise_server_exceptions=False)
# Day14：所有接口现在都要钥匙，测试客户端也带上，否则 9 个测试全 401
client.headers["X-API-Key"] = settings.api_key


def test_hello_returns_ok():
    # GET /hello 应返回统一结构 code=0 / msg=ok
    resp = client.get("/hello")
    assert resp.status_code == 200
    body = resp.json()
    assert body["code"] == 0
    assert body["msg"] == "ok"
    assert "app_name" in body["data"]


def test_boom_returns_500_unified():
    # GET /boom 故意除零，验证全局兜底网：返回 500 + 统一格式（不裸奔）
    resp = client.get("/boom")
    assert resp.status_code == 500
    body = resp.json()
    assert body["code"] == 500
    assert body["msg"] == "服务器内部错误，请联系管理员"


def test_invalid_post_returns_422():
    # POST /items 缺 price 字段，应触发 Pydantic 校验，返回 422 统一格式
    resp = client.post("/items", json={"name": "测试", "qty": 1.0})
    assert resp.status_code == 422
    body = resp.json()
    assert body["code"] == 422
    assert body["msg"] == "参数校验失败"


def test_list_all_has_rows():
    # GET /items 默认返回全部；Day12 种子数据是 6 条
    resp = client.get("/items")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] >= 6                 # 至少有种子那 6 条
    assert len(data["items"]) == data["total"]  # 默认 size=10，第一页取完
    assert data["page"] == 1
    assert data["size"] == 10


def test_pagination_second_page():
    # page=2&size=3：跳过前 3 条，返回接下来的 3 条
    resp = client.get("/items", params={"page": 2, "size": 3})
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["page"] == 2
    assert data["size"] == 3
    assert len(data["items"]) == 3


def test_filter_by_supplier():
    # 只查锦绣大地，应是 2 条（基围虾 + 三文鱼）
    resp = client.get("/items", params={"supplier": "锦绣大地"})
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] == 2
    for it in data["items"]:
        assert it["supplier"] == "锦绣大地"


def test_sort_price_desc():
    # order_by=price&desc=true：第一条价格最高，整体是降序
    resp = client.get("/items", params={"order_by": "price", "desc": True})
    assert resp.status_code == 200
    items = resp.json()["data"]["items"]
    prices = [it["price"] for it in items]
    assert prices == sorted(prices, reverse=True)   # 确认确实是降序


def test_get_nonexistent_returns_404():
    # 查不存在的 id，应走 HTTPException 兜底网，返回 404 统一结构
    resp = client.get("/items/999999")
    assert resp.status_code == 404
    assert resp.json()["code"] == 404


def test_create_then_delete():
    # ① 新增 ② 确认能查到 ③ 删除 ④ 确认已删（测试前后数据库保持干净）
    new_item = {"name": "单元测试专用", "qty": 2.0, "unit": "斤", "price": 5.0, "supplier": "测试供应商"}
    create_resp = client.post("/items", json=new_item)
    assert create_resp.status_code == 200
    created = create_resp.json()["data"]
    assert created["total"] == 10.0   # 2.0 × 5.0 = 10.0，验证 service 算金额
    new_id = created["id"]

    assert client.get(f"/items/{new_id}").status_code == 200

    del_resp = client.delete(f"/items/{new_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["data"]["deleted_id"] == new_id

    assert client.get(f"/items/{new_id}").status_code == 404
