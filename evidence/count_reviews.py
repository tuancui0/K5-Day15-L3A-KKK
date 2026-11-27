"""Đếm nhãn review đã ẩn danh trong evidence/reviews_labeled.csv.

Chạy:
  python evidence/count_reviews.py

Chỉ dùng thư viện chuẩn của Python. Người khác chạy lại trên repo phải ra đúng cùng số
với bảng kết quả trong evidence/data-mining.md.
"""
import collections
import csv
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(ROOT, "reviews_labeled.csv")
C1_LABELS = {
    "lich_trinh_khuon_vien_rong",
    "cho_doi_dong_duc",
    "gio_show_chi_phi",
}
LABEL_ORDER = [
    "lich_trinh_khuon_vien_rong",
    "cho_doi_dong_duc",
    "gio_show_chi_phi",
    "khen_nhan_vien",
    "khen_chung",
    "khong_noi_dung_chu",
]


def main():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    n = len(rows)
    text_rows = [r for r in rows if r["nhan_chinh"] != "khong_noi_dung_chu"]
    n_text = len(text_rows)

    print(f"Nguon: evidence/reviews_labeled.csv")
    print(f"Tong mau N = {n} (co noi dung chu: {n_text}, chi bam sao: {n - n_text})")
    print()

    stars = collections.Counter(r["sao"].strip() for r in rows)
    print("1) Phan bo sao:")
    for s in ["5", "4", "3", "2", "1"]:
        c = stars.get(s, 0)
        print(f"  {s} sao: {c}/{n} ({c * 100.0 / n:.1f}%)")
    print()

    labels = collections.Counter(r["nhan_chinh"].strip() for r in rows)
    print("2) Phan bo theo nhan chinh:")
    for lb in LABEL_ORDER:
        c = labels.get(lb, 0)
        pct_all = c * 100.0 / n if n else 0.0
        pct_txt = f"{c * 100.0 / n_text:.1f}%" if (n_text and lb != "khong_noi_dung_chu") else "-"
        ids = [r["id"] for r in rows if r["nhan_chinh"].strip() == lb]
        print(f"  {lb:28s}: {c:2d}/{n} ({pct_all:5.1f}% toan mau | {pct_txt:>5s} co chu)  [{', '.join(ids[:8])}{'...' if len(ids) > 8 else ''}]")

    c1_rows = [r for r in rows if r["nhan_chinh"].strip() in C1_LABELS]
    c1_n = len(c1_rows)
    print()
    print(
        f"3) Tong nhom co tin hieu lap lich / van hanh / chi phi (C1): "
        f"{c1_n}/{n} ({c1_n * 100.0 / n:.1f}% toan mau | {c1_n * 100.0 / n_text:.1f}% tren {n_text} review co chu)"
    )
    print(f"   Ma dong: {', '.join(r['id'] for r in c1_rows)}")


if __name__ == "__main__":
    main()
