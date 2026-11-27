"""Công cụ của bài toán — [B] viết. 4 công cụ chỉ đọc (không tác động ra ngoài),
khớp hợp đồng ở PHAN-CONG.md mục 2 và bảng công cụ ở spec.md §4.

Dữ liệu đọc từ data/park.json (diem, show, ve_vao_cong), data/weather.json,
data/travel.csv — xem data/DATA_CARD.md. Tạo bằng data/gen_data.py (seed=42).

Mỗi hàm: tên · input · output · có tác động ra ngoài không (gửi tin, sửa dữ liệu, chấm điểm…)
Khung tự ghi mỗi lần gọi công cụ vào trace qua @tool (xem tracing.py).
"""
import csv
import json
import os

from tracing import tool, TOOLS  # noqa: F401  (TOOLS: danh sách công cụ đã đăng ký)

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

_cache = {}


def _park():
    if "park" not in _cache:
        with open(os.path.join(_DATA_DIR, "park.json"), encoding="utf-8") as f:
            _cache["park"] = json.load(f)
    return _cache["park"]


def _weather():
    if "weather" not in _cache:
        with open(os.path.join(_DATA_DIR, "weather.json"), encoding="utf-8") as f:
            _cache["weather"] = json.load(f)
    return _cache["weather"]


def _travel():
    if "travel" not in _cache:
        table = {}
        with open(os.path.join(_DATA_DIR, "travel.csv"), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                a, b, phut = row["a"], row["b"], int(row["phut"])
                table[(a, b)] = phut
                table[(b, a)] = phut
        _cache["travel"] = table
    return _cache["travel"]


def _closures():
    """data/closures.json (v2, CP3) — điểm đóng bảo trì / show huỷ đột xuất theo ngày,
    KHÁC với giờ đóng cố định (park.json) hay huỷ khi mưa (weather.json). Dùng nội bộ
    bởi validator.py để bắt lịch xếp vào điểm/show đang gặp sự cố ngày đó.
    File không tồn tại (bản dữ liệu cũ) vẫn chạy được — coi như không ngày nào có sự cố."""
    if "closures" not in _cache:
        path = os.path.join(_DATA_DIR, "closures.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                _cache["closures"] = json.load(f)
        else:
            _cache["closures"] = {}
    return _cache["closures"]


@tool
def tra_diem_choi(the_loai: str = None, khu: str = None) -> list:
    """Tra danh sách điểm chơi trong công viên, lọc theo thể loại và/hoặc khu (tuỳ chọn).
    Input: the_loai (str, vd "cam_giac_manh"|"tre_em"|"nuoc"|"van_hoa"|"san_khau", hoặc None lấy hết),
           khu (str, tên khu, hoặc None lấy hết).
    Output: list điểm chơi {id, ten, khu, mo, dong, thoi_luong_phut, cho_doi_phut, gia,
            chieu_cao_min_cm, trong_nha, the_loai}. Không tác động ra ngoài."""
    diem = _park()["diem"]
    out = diem
    if the_loai:
        out = [d for d in out if the_loai in d["the_loai"]]
    if khu:
        out = [d for d in out if d["khu"] == khu]
    return out


@tool
def tra_lich_show(diem_id: str = None) -> list:
    """Tra lịch diễn của các show trong công viên, lọc theo điểm diễn ra (tuỳ chọn).
    Input: diem_id (str, vd "D14", hoặc None lấy hết các show).
    Output: list show {id, ten, diem_id, gio (list giờ diễn trong ngày), thoi_luong_phut,
            huy_khi_mua}. Không tác động ra ngoài."""
    show = _park()["show"]
    if diem_id:
        return [s for s in show if s["diem_id"] == diem_id]
    return show


@tool
def tra_thoi_tiet(ngay: str) -> dict:
    """Tra thời tiết dự báo của một ngày trong công viên.
    Input: ngay (str, định dạng "YYYY-MM-DD").
    Output: {"mua_tu": "HH:MM", "mua_den": "HH:MM"} nếu có mưa, hoặc {} nếu không có
    dữ liệu mưa cho ngày đó (coi như trời quang). Không tác động ra ngoài."""
    return _weather().get(ngay, {})


@tool
def uoc_thoi_gian_di(tu_id: str, den_id: str) -> int:
    """Ước lượng thời gian đi bộ giữa hai điểm (hoặc từ cổng "CONG" đến một điểm).
    Input: tu_id (str, id điểm hoặc "CONG"), den_id (str, id điểm hoặc "CONG").
    Output: số phút đi bộ (int). Nếu không có dữ liệu cho cặp này, trả về ước lượng
    mặc định 10 phút (an toàn, không chặn luồng). Không tác động ra ngoài."""
    if tu_id == den_id:
        return 0
    return _travel().get((tu_id, den_id), 10)
