"""inventory 模块的测试（为 Day 13 的 pytest 打底）。"""

from src.inventory import ReceiptItem, summarize_items


def test_summarize_basic():
    items = [
        ReceiptItem("五花肉", 10.0, "斤", 18.5),
        ReceiptItem("香葱", 2.0, "斤", 6.0),
    ]
    result = summarize_items(items)
    assert result["total_amount"] == 197.0
    assert result["total_qty"] == 12.0
    assert result["item_count"] == 2


def test_summarize_empty_raises():
    try:
        summarize_items([])
        assert False, "空列表应当抛出异常"
    except ValueError:
        pass


def test_summarize_negative_raises():
    try:
        summarize_items([ReceiptItem("测试", -1.0, "斤", 5.0)])
        assert False, "负数量应当抛出异常"
    except ValueError:
        pass
