"""收货单清洗：读取文本 → 解析 → 容错 → 写出 CSV。"""

from dataclasses import dataclass


@dataclass
class ReceiptItem:
    name: str          # 品名
    qty: float         # 数量
    unit: str          # 单位
    price: float       # 单价
    ok: bool = True    # 这条是否合法（脏数据标 False）


def parse_line(line: str) -> ReceiptItem:
    """把一行 '品名,数量,单位,单价' 解析成 ReceiptItem。"""
    try:
        name, qty_s, unit, price_s = line.strip().split(",")
        qty = float(qty_s)
        price = float(price_s)
        if qty < 0 or price < 0:
            raise ValueError("数量或价格为负")
        return ReceiptItem(name, qty, unit, price)
    except (ValueError, IndexError) as e:
        return ReceiptItem(line, 0.0, "", 0.0, ok=False)


def main() -> None:
    ok_items: list[ReceiptItem] = []
    bad_lines: list[str] = []

    with open("sample_receipt.txt", encoding="utf-8") as f:
        for raw in f:
            item = parse_line(raw)
            if item.ok:
                ok_items.append(item)
            else:
                bad_lines.append(raw.strip())

    total = sum(i.qty * i.price for i in ok_items)
    print(f"合法条目 {len(ok_items)} 条，合计 ¥{total:.2f}")
    print(f"脏数据 {len(bad_lines)} 条：{bad_lines}")

    with open("cleaned.csv", "w", encoding="utf-8") as out:
        out.write("name,qty,unit,price\n")
        for i in ok_items:
            out.write(f"{i.name},{i.qty},{i.unit},{i.price}\n")


if __name__ == "__main__":
    main()