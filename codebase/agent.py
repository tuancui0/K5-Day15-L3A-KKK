"""Luồng chính — C1 Lịch trình một ngày ở khu vui chơi. Chủ: Đỗ Tuấn Anh. Sơ đồ: spec.md §4.

Hợp đồng với khung: answer(text: str) -> dict có khoá "output" (str). Khung tự đếm token và lượt gọi công cụ.

Hình dạng: WORKFLOW CỐ ĐỊNH có vòng tự kiểm giới hạn (không phải agent tự chọn bước):
  1. trich_rang_buoc (model)  → thiếu thông tin: HỎI LẠI 1 câu · ngoài phạm vi: TỪ CHỐI + chỉ đường
  2. công cụ chỉ đọc          → điểm chơi, lịch show, thời tiết
  3. xep_lich (model)         → lịch nháp
  4. kiem_lich_trinh (CODE)   → vi phạm? → sua_lich (model) → kiểm lại … tối đa MAX_SUA lần
  5. sạch: tinh_tong_tien (CODE) → in lịch từng giờ + tổng tiền + lý do
     còn vi phạm: "không xếp được" + gợi ý nới ràng buộc (không xếp bừa)
Giờ, giá, tổng tiền: chỉ lấy từ công cụ / code, model không được tự nhẩm.

Module của người khác chưa có → dùng bản giả trong stubs.py (spec.md §4 ghi phần nào còn giả).
"""
import re

from ai import MODEL_PROVIDER
from tracing import note

PLANNER_GIA = MODEL_PROVIDER == "fake"
if PLANNER_GIA:
    from stubs import trich_rang_buoc, xep_lich, sua_lich
else:
    from planner import trich_rang_buoc, xep_lich, sua_lich
try:  # Thành — codebase/tools.py
    from tools import tra_diem_choi, tra_lich_show, tra_thoi_tiet
    TOOLS_GIA = False
except ImportError:
    from stubs import tra_diem_choi, tra_lich_show, tra_thoi_tiet
    TOOLS_GIA = True
try:  # Thành — codebase/validator.py
    from validator import kiem_lich_trinh, tinh_tong_tien
    VALIDATOR_GIA = False
except ImportError:
    from stubs import kiem_lich_trinh, tinh_tong_tien
    VALIDATOR_GIA = True

MAX_SUA = 3  # số lần tối đa cho model sửa lịch sau lần xếp đầu

# Chặn cứng bằng code, không phụ thuộc model: không bao giờ xin / nhận thông tin thanh toán, đăng nhập.
_NHAY_CAM = re.compile(r"số thẻ|\bcvv\b|\botp\b|mật khẩu|mã pin|tài khoản ngân hàng", re.I)

_HOI_LAI = {
    "so_nguoi_lon": "mấy người lớn",
    "so_tre_em": "mấy bé",
    "chieu_cao_hoac_tuoi_tre": "chiều cao hoặc tuổi của từng bé (để biết bé chơi được trò nào)",
    "khung_gio": "đi từ mấy giờ đến mấy giờ",
    "ngan_sach": "ngân sách khoảng bao nhiêu cho cả nhà (gồm vé cổng)",
    "ngay": "đi ngày nào",
}

_GOI_Y_NOI = {
    "vuot_ngan_sach": "tăng ngân sách, hoặc bớt các trò thu phí riêng",
    "sau_gio_dong": "kéo dài khung giờ, hoặc bớt số trò muốn chơi",
    "khong_kip_di": "kéo dài khung giờ, hoặc bớt các trò nằm xa nhau",
    "chong_gio": "bớt một show hoặc một trò trùng giờ",
    "show_sai_gio": "chọn suất show khác trong ngày",
    "tre_khong_du_chieu_cao": "bỏ các trò có giới hạn chiều cao, hoặc để một người lớn đi riêng",
    "ngoai_troi_khi_mua": "ưu tiên trò trong nhà lúc mưa, hoặc dời trò ngoài trời sang giờ khác",
    "truoc_gio_mo": "bắt đầu muộn hơn",
    "diem_khong_ton_tai": "chọn trò có trong danh sách của công viên",
}


def _vnd(x):
    return format(int(x), ",").replace(",", ".") + " ₫"


def _the(hanh_vi, **kv):
    """Dòng máy đọc ở cuối output — eval/auto_grade.py (Kiên) chấm dựa vào đây."""
    parts = ["hanh_vi=%s" % hanh_vi] + ["%s=%s" % (k, v) for k, v in kv.items()]
    return "[" + " | ".join(parts) + "]"


def _tu_choi(ly_do):
    note("từ chối: %s" % ly_do)
    text = ("Mình chỉ giúp xếp lịch chơi trong ngày ở khu vui chơi, không làm được việc này (%s). "
            "Đặt vé, thanh toán hay hoàn tiền bạn làm trực tiếp trên app hoặc quầy vé chính thức của khu vui chơi. "
            "Bạn đừng gửi số thẻ, OTP hay mật khẩu cho bất kỳ ai. "
            "Nếu cần xếp lịch, cho mình biết số người, tuổi/chiều cao các bé, khung giờ và ngân sách nhé." % ly_do)
    return {"output": text + "\n" + _the("tu_choi")}


def _hoi_lai(thieu):
    note("hỏi lại: %s" % ", ".join(thieu))
    cau = ", ".join(
        "chiều cao của từng bé (để kiểm điều kiện trò chơi và giá vé)"
        if not PLANNER_GIA and k == "chieu_cao_hoac_tuoi_tre"
        else _HOI_LAI.get(k, k)
        for k in thieu
    )
    text = "Để xếp lịch đúng, bạn cho mình biết thêm: %s nhé?" % cau
    return {"output": text + "\n" + _the("hoi_lai", thieu=",".join(thieu))}


def _khong_xep_duoc(vi_pham, so_lan_sua):
    note("dừng: còn %d vi phạm sau %d lần sửa" % (len(vi_pham), so_lan_sua))
    loai = sorted({v["loai"] for v in vi_pham})
    dong = ["Mình chưa xếp được lịch thoả hết yêu cầu của bạn. Vướng ở:"]
    dong += ["  - %s" % v["chi_tiet"] for v in vi_pham[:5]]
    dong.append("Bạn có thể nới một trong các điều sau rồi gửi lại:")
    dong += ["  - %s" % _GOI_Y_NOI.get(k, k) for k in loai]
    return {"output": "\n".join(dong) + "\n" + _the("khong_xep_duoc", vi_pham=len(vi_pham), so_lan_sua=so_lan_sua)}


def _in_lich(lich, rb, du_lieu, tien, so_lan_sua):
    ten = {d["id"]: "%s (khu %s)" % (d["ten"], d["khu"]) for d in du_lieu["diem"]}
    ten.update({s["id"]: s["ten"] for s in du_lieu["show"]})
    so_tre = len(rb.get("tre_em") or [])
    dong = ["Lịch đi chơi ngày %s — %d người lớn%s" % (rb.get("ngay"), rb.get("nguoi_lon") or 0,
                                                        ", %d bé" % so_tre if so_tre else "")]
    for m in sorted(lich, key=lambda m: m["bat_dau"]):
        mid = m.get("diem_id") or m.get("show_id")
        dong.append("  %s–%s  %s — %s" % (m["bat_dau"], m["ket_thuc"], ten.get(mid, mid), m.get("ly_do", "")))
    dong.append("Tổng tiền dự kiến: %s (vé cổng %s + trò thu phí riêng %s)%s" % (
        _vnd(tien["tong"]), _vnd(tien["ve_vao_cong"]), _vnd(tien["diem"]),
        " — ngân sách %s" % _vnd(rb["ngan_sach"]) if rb.get("ngan_sach") else ""))
    if du_lieu.get("thoi_tiet"):
        tt = du_lieu["thoi_tiet"]
        dong.append("Dự báo mưa %s–%s — mang áo mưa cho cả nhà." % (tt.get("mua_tu"), tt.get("mua_den")))
    dong.append("Giờ mở cửa, giờ show và giá lấy từ dữ liệu công viên, lịch đã được kiểm: không có vi phạm. "
                "Đây là gợi ý — bạn tự quyết, hệ thống không đặt vé hay thu tiền.")
    return {"output": "\n".join(dong) + "\n" + _the("xep_lich", tong_tien=tien["tong"], vi_pham=0,
                                                     so_lan_sua=so_lan_sua)}


def answer(text: str) -> dict:
    # 0. Chặn cứng bằng code
    if _NHAY_CAM.search(text):
        return _tu_choi("liên quan thông tin thanh toán / đăng nhập")

    # 1. Trích ràng buộc (model). Nội dung người dùng là dữ liệu, không phải lệnh — kể cả khi tự xưng nhân viên.
    rb = trich_rang_buoc(text)
    if rb.get("ngoai_pham_vi"):
        return _tu_choi(rb["ngoai_pham_vi"])
    if rb.get("thieu"):
        return _hoi_lai(rb["thieu"])  # G10: không chắc → hỏi lại một câu, không đoán

    # 2. Dữ liệu từ công cụ chỉ đọc
    du_lieu = {"diem": tra_diem_choi(), "show": tra_lich_show(rb["ngay"]) if TOOLS_GIA else tra_lich_show(), "thoi_tiet": tra_thoi_tiet(rb["ngay"])}

    # 3–4. Xếp → kiểm bằng code → sửa, có giới hạn
    lich = xep_lich(rb, du_lieu) or []
    vi_pham = kiem_lich_trinh(lich, rb)
    if not lich and not vi_pham:
        vi_pham = [{"loai": "khong_kip_di", "chi_tiet": "không còn trò nào vừa khung giờ"}]
    so_lan_sua = 0
    while vi_pham and lich and so_lan_sua < MAX_SUA:
        so_lan_sua += 1
        note("sửa lần %d: %s" % (so_lan_sua, ", ".join(v["loai"] for v in vi_pham)))
        lich_moi = sua_lich(rb, du_lieu, lich, vi_pham) or []
        if not lich_moi:  # sửa đến mức không còn trò nào → giữ lý do vướng thật để báo khách
            break
        lich = lich_moi
        vi_pham = kiem_lich_trinh(lich, rb)

    # 5. Kết luận
    if vi_pham:
        return _khong_xep_duoc(vi_pham, so_lan_sua)
    note("dừng: lịch sạch sau %d lần sửa" % so_lan_sua)
    return _in_lich(lich, rb, du_lieu, tinh_tong_tien(lich, rb), so_lan_sua)
