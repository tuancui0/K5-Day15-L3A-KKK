"""Sinh dữ liệu công viên giả — NHÓM [B] viết. seed=42, khu dựng tên "Công Viên Mẫu".
Dữ liệu tự dựng, KHÔNG phải bằng chứng pain (xem evidence/data-mining.md cho bằng chứng thật).

Chạy: python data/gen_data.py
Ghi ra: data/park.json, data/weather.json, data/travel.csv

Mỗi lần chạy ra kết quả giống hệt nhau nhờ random.seed(SEED) — nếu cần sinh bộ dữ liệu
"bẩn" hơn (điểm đóng sớm, show huỷ khi mưa, ngân sách sát...) cho CP3, chỉnh thủ công
ở phần DIEM / SHOW / WEATHER bên dưới chứ không đổi SEED, để kết quả vẫn lặp lại được.
"""
import csv
import json
import math
import os
import random

SEED = 42
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

random.seed(SEED)

# ---------------------------------------------------------------------------
# 15 điểm chơi, chia 4 khu + 1 khu sân khấu. the_loai dùng để lọc theo sở thích.
# chieu_cao_min_cm > 0 ở các trò cảm giác mạnh / máng trượt — khớp bằng chứng
# thật đã đào (review Google Maps: ràng buộc 1,4m khiến trẻ nhỏ không được chơi).
# ---------------------------------------------------------------------------
DIEM = [
    {"id": "D01", "ten": "Tàu lượn siêu tốc", "khu": "Khu Cảm Giác Mạnh",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 3, "cho_doi_phut": 20,
     "gia": {"nguoi_lon": 50000, "tre_em": 50000}, "chieu_cao_min_cm": 140,
     "trong_nha": False, "the_loai": ["cam_giac_manh"]},
    {"id": "D02", "ten": "Đu quay dây văng", "khu": "Khu Cảm Giác Mạnh",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 2, "cho_doi_phut": 15,
     "gia": {"nguoi_lon": 40000, "tre_em": 40000}, "chieu_cao_min_cm": 130,
     "trong_nha": False, "the_loai": ["cam_giac_manh"]},
    {"id": "D03", "ten": "Nhà ma", "khu": "Khu Cảm Giác Mạnh",
     "mo": "09:00", "dong": "16:30", "thoi_luong_phut": 10, "cho_doi_phut": 10,
     "gia": {"nguoi_lon": 60000, "tre_em": 60000}, "chieu_cao_min_cm": 120,
     "trong_nha": True, "the_loai": ["cam_giac_manh"]},
    {"id": "D04", "ten": "Đu quay ngựa gỗ", "khu": "Khu Trẻ Em",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 5, "cho_doi_phut": 5,
     "gia": {"nguoi_lon": 30000, "tre_em": 20000}, "chieu_cao_min_cm": 0,
     "trong_nha": False, "the_loai": ["tre_em"]},
    {"id": "D05", "ten": "Nhà bóng", "khu": "Khu Trẻ Em",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 15, "cho_doi_phut": 5,
     "gia": {"nguoi_lon": 0, "tre_em": 30000}, "chieu_cao_min_cm": 0,
     "trong_nha": True, "the_loai": ["tre_em"]},
    {"id": "D06", "ten": "Xe điện đụng", "khu": "Khu Trẻ Em",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 5, "cho_doi_phut": 10,
     "gia": {"nguoi_lon": 30000, "tre_em": 30000}, "chieu_cao_min_cm": 100,
     "trong_nha": False, "the_loai": ["tre_em"]},
    {"id": "D07", "ten": "Hồ bơi tạo sóng", "khu": "Khu Nước",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 30, "cho_doi_phut": 0,
     "gia": {"nguoi_lon": 0, "tre_em": 0}, "chieu_cao_min_cm": 0,
     "trong_nha": False, "the_loai": ["nuoc"]},
    {"id": "D08", "ten": "Sông lười", "khu": "Khu Nước",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 20, "cho_doi_phut": 0,
     "gia": {"nguoi_lon": 0, "tre_em": 0}, "chieu_cao_min_cm": 0,
     "trong_nha": False, "the_loai": ["nuoc"]},
    {"id": "D09", "ten": "Máng trượt cao tốc", "khu": "Khu Nước",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 2, "cho_doi_phut": 20,
     "gia": {"nguoi_lon": 20000, "tre_em": 20000}, "chieu_cao_min_cm": 140,
     "trong_nha": False, "the_loai": ["nuoc"]},
    {"id": "D10", "ten": "Thuỷ cung", "khu": "Khu Văn Hoá",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 30, "cho_doi_phut": 5,
     "gia": {"nguoi_lon": 80000, "tre_em": 50000}, "chieu_cao_min_cm": 0,
     "trong_nha": True, "the_loai": ["van_hoa"]},
    {"id": "D11", "ten": "Vườn thú mini", "khu": "Khu Văn Hoá",
     "mo": "09:00", "dong": "16:30", "thoi_luong_phut": 20, "cho_doi_phut": 0,
     "gia": {"nguoi_lon": 0, "tre_em": 0}, "chieu_cao_min_cm": 0,
     "trong_nha": False, "the_loai": ["van_hoa"]},
    {"id": "D12", "ten": "Rạp chiếu phim 4D", "khu": "Khu Văn Hoá",
     "mo": "09:30", "dong": "16:30", "thoi_luong_phut": 15, "cho_doi_phut": 10,
     "gia": {"nguoi_lon": 50000, "tre_em": 50000}, "chieu_cao_min_cm": 0,
     "trong_nha": True, "the_loai": ["van_hoa"]},
    {"id": "D13", "ten": "Đu quay vòng trời", "khu": "Khu Cảm Giác Mạnh",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 8, "cho_doi_phut": 15,
     "gia": {"nguoi_lon": 40000, "tre_em": 40000}, "chieu_cao_min_cm": 100,
     "trong_nha": False, "the_loai": ["cam_giac_manh"]},
    {"id": "D14", "ten": "Sân khấu ngoài trời", "khu": "Khu Trung Tâm",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 0, "cho_doi_phut": 0,
     "gia": {"nguoi_lon": 0, "tre_em": 0}, "chieu_cao_min_cm": 0,
     "trong_nha": False, "the_loai": ["san_khau"]},
    {"id": "D15", "ten": "Nhà hát trong nhà", "khu": "Khu Trung Tâm",
     "mo": "09:00", "dong": "17:00", "thoi_luong_phut": 0, "cho_doi_phut": 0,
     "gia": {"nguoi_lon": 0, "tre_em": 0}, "chieu_cao_min_cm": 0,
     "trong_nha": True, "the_loai": ["san_khau"]},
]

# show diễn ra tại D14 (ngoài trời, huỷ khi mưa) hoặc D15 (trong nhà, không huỷ)
SHOW = [
    {"id": "S01", "ten": "Xiếc thú", "diem_id": "D14", "gio": ["10:30", "15:30"],
     "thoi_luong_phut": 30, "huy_khi_mua": True},
    {"id": "S02", "ten": "Nhạc nước", "diem_id": "D14", "gio": ["11:30", "16:30"],
     "thoi_luong_phut": 20, "huy_khi_mua": True},
    {"id": "S03", "ten": "Múa rối nước", "diem_id": "D15", "gio": ["13:00", "16:00"],
     "thoi_luong_phut": 45, "huy_khi_mua": False},
    {"id": "S04", "ten": "Kịch thiếu nhi", "diem_id": "D15", "gio": ["10:00", "14:30"],
     "thoi_luong_phut": 30, "huy_khi_mua": False},
]

VE_VAO_CONG = {"nguoi_lon": 220000, "tre_em": 150000, "tre_duoi_1m": 0}

# 1 ngày mưa — khoảng mưa đè lên giờ chạy S01 (10:30, ngoài trời, huỷ khi mưa)
# và một phần giờ mở của D01/D02/D13 (ngoài trời) để bài toán có câu thử "ngoai_troi_khi_mua".
WEATHER = {
    "2026-12-05": {"mua_tu": "10:00", "mua_den": "12:00"},
}

# --- Dữ liệu "bẩn" v2 (CP3) — dựa trên bằng chứng phỏng vấn P1, P3: lỡ show vì
# không biết trước show bị huỷ, đến trò mới biết đóng bảo trì đột xuất. Khác
# "huy_khi_mua"/giờ đóng cố định: đây là sự cố phát sinh riêng cho 1 ngày cụ thể,
# không báo trước trong giờ mở/đóng bình thường của park.json.
# diem_dong: điểm chơi bị đóng cả ngày đó (bảo trì/sự cố) dù park.json ghi vẫn mở.
# show_huy: show bị huỷ ngày đó (sự cố kỹ thuật) dù lịch show (park.json) vẫn ghi diễn.
CLOSURES = {
    "2026-12-06": {
        "diem_dong": ["D09"],   # Máng trượt cao tốc — bảo trì đột xuất, không báo trước
        "show_huy": [],
    },
    "2026-12-07": {
        "diem_dong": [],
        "show_huy": ["S03"],    # Múa rối nước — huỷ vì sự cố kỹ thuật, không phải do mưa
    },
}


def _sinh_toa_do():
    """Gán toạ độ (m) cho mỗi điểm — các điểm cùng khu đứng gần nhau hơn, dùng seed=42.
    Cổng chính ("CONG") đặt ở gốc (0, 0)."""
    tam_khu = {
        "Khu Cảm Giác Mạnh": (600, 100),
        "Khu Trẻ Em": (150, 450),
        "Khu Nước": (650, 450),
        "Khu Văn Hoá": (150, 150),
        "Khu Trung Tâm": (350, 300),
    }
    toa_do = {"CONG": (0, 0)}
    for d in DIEM:
        cx, cy = tam_khu[d["khu"]]
        toa_do[d["id"]] = (cx + random.uniform(-60, 60), cy + random.uniform(-60, 60))
    return toa_do


def _sinh_travel_csv():
    """Thời gian đi bộ (phút) giữa mọi cặp điểm + cổng, suy ra từ khoảng cách Euclid
    với tốc độ đi bộ trung bình 70 m/phút, làm tròn lên phút gần nhất, tối thiểu 1 phút."""
    toa_do = _sinh_toa_do()
    ids = list(toa_do.keys())
    rows = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            (ax, ay), (bx, by) = toa_do[a], toa_do[b]
            met = math.dist((ax, ay), (bx, by))
            phut = max(1, math.ceil(met / 70))
            rows.append((a, b, phut))
    return rows


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    park = {"diem": DIEM, "show": SHOW, "ve_vao_cong": VE_VAO_CONG}
    with open(os.path.join(DATA_DIR, "park.json"), "w", encoding="utf-8") as f:
        json.dump(park, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA_DIR, "weather.json"), "w", encoding="utf-8") as f:
        json.dump(WEATHER, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA_DIR, "closures.json"), "w", encoding="utf-8") as f:
        json.dump(CLOSURES, f, ensure_ascii=False, indent=2)

    rows = _sinh_travel_csv()
    with open(os.path.join(DATA_DIR, "travel.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["a", "b", "phut"])
        w.writerows(rows)

    print("Đã sinh: data/park.json (%d điểm, %d show), data/weather.json (%d ngày mưa), "
          "data/closures.json (%d ngày có sự cố đóng/huỷ đột xuất), "
          "data/travel.csv (%d cặp điểm)"
          % (len(DIEM), len(SHOW), len(WEATHER), len(CLOSURES), len(rows)))


if __name__ == "__main__":
    main()
