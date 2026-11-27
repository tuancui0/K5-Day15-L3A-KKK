"""Unit test nhỏ cho validator.py — chạy: python test_validator.py (từ thư mục codebase/)."""
import sys
sys.path.insert(0, ".")
from validator import kiem_lich_trinh, tinh_tong_tien  # noqa: E402

RANG_BUOC_OK = {
    "ngay": "2026-12-06", "gio_bat_dau": "09:00", "gio_ket_thuc": "17:00",
    "nguoi_lon": 2, "tre_em": [{"tuoi": 8, "chieu_cao_cm": 130}],
    "ngan_sach": 1500000, "so_thich": ["tre_em"], "thieu": [], "ngoai_pham_vi": None,
}

LICH_SACH = [
    {"diem_id": "D04", "bat_dau": "09:15", "ket_thuc": "09:20", "ly_do": "khởi động nhẹ"},
    {"diem_id": "D06", "bat_dau": "09:40", "ket_thuc": "09:45", "ly_do": "trẻ thích xe điện đụng"},
]


def test_lich_sach_khong_vi_pham():
    vi_pham = kiem_lich_trinh(LICH_SACH, RANG_BUOC_OK)
    assert vi_pham == [], "Lịch sạch nhưng báo vi phạm: %r" % vi_pham


def test_chieu_cao_khong_du():
    rb = dict(RANG_BUOC_OK, tre_em=[{"tuoi": 5, "chieu_cao_cm": 100}])
    lich = [{"diem_id": "D01", "bat_dau": "09:15", "ket_thuc": "09:18", "ly_do": "thử"}]
    vi_pham = kiem_lich_trinh(lich, rb)
    assert any(v["loai"] == "tre_khong_du_chieu_cao" for v in vi_pham)


def test_truoc_gio_mo():
    lich = [{"diem_id": "D12", "bat_dau": "09:00", "ket_thuc": "09:15", "ly_do": "thử"}]
    vi_pham = kiem_lich_trinh(lich, RANG_BUOC_OK)  # D12 mở 09:30
    assert any(v["loai"] == "truoc_gio_mo" for v in vi_pham)


def test_chong_gio():
    lich = [
        {"diem_id": "D04", "bat_dau": "09:00", "ket_thuc": "09:30", "ly_do": "a"},
        {"diem_id": "D05", "bat_dau": "09:10", "ket_thuc": "09:20", "ly_do": "b"},
    ]
    vi_pham = kiem_lich_trinh(lich, RANG_BUOC_OK)
    assert any(v["loai"] == "chong_gio" for v in vi_pham)


def test_khong_kip_di():
    # D01 (Khu Cảm Giác Mạnh) và D07 (Khu Nước) cách xa nhau, 2 phút là không đủ
    lich = [
        {"diem_id": "D01", "bat_dau": "09:00", "ket_thuc": "09:03", "ly_do": "a"},
        {"diem_id": "D07", "bat_dau": "09:05", "ket_thuc": "09:20", "ly_do": "b"},
    ]
    rb = dict(RANG_BUOC_OK, tre_em=[{"tuoi": 10, "chieu_cao_cm": 150}])
    vi_pham = kiem_lich_trinh(lich, rb)
    assert any(v["loai"] == "khong_kip_di" for v in vi_pham)


def test_vuot_ngan_sach():
    rb = dict(RANG_BUOC_OK, ngan_sach=1000)  # ngân sách cực thấp, chắc chắn vượt
    vi_pham = kiem_lich_trinh(LICH_SACH, rb)
    assert any(v["loai"] == "vuot_ngan_sach" for v in vi_pham)


def test_diem_khong_ton_tai():
    lich = [{"diem_id": "D99", "bat_dau": "09:00", "ket_thuc": "09:10", "ly_do": "a"}]
    vi_pham = kiem_lich_trinh(lich, RANG_BUOC_OK)
    assert any(v["loai"] == "diem_khong_ton_tai" for v in vi_pham)


def test_show_sai_gio():
    lich = [{"show_id": "S01", "bat_dau": "12:00", "ket_thuc": "12:30", "ly_do": "a"}]  # S01 diễn 10:30/15:30
    vi_pham = kiem_lich_trinh(lich, RANG_BUOC_OK)
    assert any(v["loai"] == "show_sai_gio" for v in vi_pham)


def test_ngoai_troi_khi_mua():
    rb = dict(RANG_BUOC_OK, ngay="2026-12-05")  # ngày có mưa 10:00-12:00 (xem gen_data.py)
    lich = [{"diem_id": "D01", "bat_dau": "10:30", "ket_thuc": "10:33", "ly_do": "a"}]  # D01 ngoài trời
    vi_pham = kiem_lich_trinh(lich, rb)
    assert any(v["loai"] == "ngoai_troi_khi_mua" for v in vi_pham)


def test_tinh_tong_tien():
    tong = tinh_tong_tien(LICH_SACH, RANG_BUOC_OK)
    assert tong["tong"] == tong["ve_vao_cong"] + tong["diem"]
    assert tong["ve_vao_cong"] > 0


if __name__ == "__main__":
    import inspect
    mod = sys.modules[__name__]
    tests = [f for name, f in inspect.getmembers(mod, inspect.isfunction) if name.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print("OK   ", t.__name__)
        except AssertionError as e:
            failed += 1
            print("FAIL ", t.__name__, "-", e)
    print("\n%d/%d test qua" % (len(tests) - failed, len(tests)))
    sys.exit(1 if failed else 0)
