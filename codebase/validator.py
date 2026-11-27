"""Kiểm lịch trình + tính tiền — [B] viết, [C] dùng lại để chấm điểm (eval/auto_grade.py).
Mọi con số (giờ, giá, tổng tiền, vi phạm) đi qua đây — model KHÔNG được tự nhẩm (nguyên tắc
"Chặn rủi ro" ở spec.md §4 / PHAN-CONG.md mục 4.3).

Hợp đồng (PHAN-CONG.md mục 2):
    kiem_lich_trinh(lich, rang_buoc) -> [{"loai": "...", "chi_tiet": "..."}]
    tinh_tong_tien(lich, rang_buoc)  -> {"ve_vao_cong": int, "diem": int, "tong": int}

    lich = [{"diem_id"|"show_id": "...", "bat_dau": "HH:MM", "ket_thuc": "HH:MM", "ly_do": "..."}]
    rang_buoc = {"ngay", "gio_bat_dau", "gio_ket_thuc", "nguoi_lon", "tre_em": [{"tuoi","chieu_cao_cm"}],
                 "ngan_sach", "so_thich", "thieu", "ngoai_pham_vi"}

11 loại vi phạm: truoc_gio_mo · sau_gio_dong · chong_gio · khong_kip_di · vuot_ngan_sach ·
tre_khong_du_chieu_cao · ngoai_troi_khi_mua · show_sai_gio · diem_khong_ton_tai ·
diem_dong_dot_xuat · show_huy_dot_xuat

2 loại cuối (v2, CP3) đọc data/closures.json — điểm bảo trì / show huỷ sự cố phát sinh
riêng cho 1 ngày, khác giờ đóng cố định hay huỷ khi mưa. Lấy từ bằng chứng phỏng vấn
P1 ("đến nơi mới biết bé không đủ chiều cao") + P3 ("qua tới thủy cung thì show đang
diễn rồi") — agent không biết trước sự cố qua 4 công cụ hiện có, validator là lưới
chặn cuối cùng bắt lịch lỡ xếp vào điểm/show đang gặp sự cố.

Hàm này KHÔNG phải công cụ của agent (không @tool) — agent gọi trực tiếp trong vòng tự kiểm
(agent.py), eval/auto_grade.py gọi lại để chấm độc lập với model.
"""
from tools import _park, _weather, _travel, _closures  # dùng lại dữ liệu đã nạp, không gọi qua @tool


def _phut(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def _khoang_cham(a0, a1, b0, b1):
    """True nếu khoảng [a0,a1) và [b0,b1) (phút) chồng nhau."""
    return a0 < b1 and b0 < a1


def _index_diem():
    return {d["id"]: d for d in _park()["diem"]}


def _index_show():
    return {s["id"]: s for s in _park()["show"]}


def _muc_vi_tri_va_khung_gio(muc, idx_diem, idx_show):
    """Trả (diem_cua_muc, bat_dau_phut, ket_thuc_phut, loai_thieu) cho một mục lịch.
    loai_thieu = "diem_khong_ton_tai" nếu không tìm thấy diem_id/show_id."""
    bd, kt = _phut(muc["bat_dau"]), _phut(muc["ket_thuc"])
    if "diem_id" in muc:
        d = idx_diem.get(muc["diem_id"])
        return d, bd, kt, (None if d else "diem_khong_ton_tai")
    if "show_id" in muc:
        s = idx_show.get(muc["show_id"])
        if not s:
            return None, bd, kt, "diem_khong_ton_tai"
        d = idx_diem.get(s["diem_id"])
        return d, bd, kt, (None if d else "diem_khong_ton_tai")
    return None, bd, kt, "diem_khong_ton_tai"


def kiem_lich_trinh(lich, rang_buoc):
    """Kiểm một lịch trình theo 11 loại vi phạm. Trả list rỗng nếu lịch sạch."""
    idx_diem, idx_show = _index_diem(), _index_show()
    weather = _weather().get(rang_buoc.get("ngay"), {})
    mua_tu = _phut(weather["mua_tu"]) if weather else None
    mua_den = _phut(weather["mua_den"]) if weather else None
    sucos = _closures().get(rang_buoc.get("ngay"), {})
    diem_dong_hom_nay = set(sucos.get("diem_dong", []))
    show_huy_hom_nay = set(sucos.get("show_huy", []))

    vi_pham = []
    muc_hop_le = []  # (muc, diem, bd, kt) — chỉ các mục tra được điểm, dùng cho chong_gio/khong_kip_di

    for muc in lich:
        diem, bd, kt, thieu = _muc_vi_tri_va_khung_gio(muc, idx_diem, idx_show)
        ten = muc.get("diem_id") or muc.get("show_id") or "?"

        if thieu == "diem_khong_ton_tai":
            vi_pham.append({"loai": "diem_khong_ton_tai",
                             "chi_tiet": "Không tìm thấy %s trong dữ liệu công viên" % ten})
            continue

        if "show_id" in muc:
            show = idx_show[muc["show_id"]]
            if muc["bat_dau"] not in show["gio"]:
                vi_pham.append({"loai": "show_sai_gio",
                                "chi_tiet": "Show %s không diễn lúc %s (giờ diễn: %s)"
                                            % (ten, muc["bat_dau"], ", ".join(show["gio"]))})
            if show["huy_khi_mua"] and not diem["trong_nha"] and mua_tu is not None \
                    and _khoang_cham(bd, kt, mua_tu, mua_den):
                vi_pham.append({"loai": "ngoai_troi_khi_mua",
                                "chi_tiet": "Show %s ngoài trời, huỷ khi mưa — trùng khoảng mưa %s-%s"
                                            % (ten, weather["mua_tu"], weather["mua_den"])})
            if muc["show_id"] in show_huy_hom_nay:
                vi_pham.append({"loai": "show_huy_dot_xuat",
                                "chi_tiet": "Show %s bị huỷ đột xuất ngày %s (sự cố kỹ thuật, không báo trước)"
                                            % (ten, rang_buoc.get("ngay"))})
        else:
            if muc["diem_id"] in diem_dong_hom_nay:
                vi_pham.append({"loai": "diem_dong_dot_xuat",
                                 "chi_tiet": "%s đóng bảo trì đột xuất ngày %s, không mở cửa"
                                             % (ten, rang_buoc.get("ngay"))})
            if bd < _phut(diem["mo"]):
                vi_pham.append({"loai": "truoc_gio_mo",
                                 "chi_tiet": "%s mở cửa %s, lịch xếp %s" % (ten, diem["mo"], muc["bat_dau"])})
            if kt > _phut(diem["dong"]):
                vi_pham.append({"loai": "sau_gio_dong",
                                 "chi_tiet": "%s đóng cửa %s, lịch xếp đến %s" % (ten, diem["dong"], muc["ket_thuc"])})
            if diem["chieu_cao_min_cm"] > 0:
                thieu_tre = [te for te in rang_buoc.get("tre_em", [])
                             if te.get("chieu_cao_cm", 9999) < diem["chieu_cao_min_cm"]]
                if thieu_tre:
                    vi_pham.append({"loai": "tre_khong_du_chieu_cao",
                                     "chi_tiet": "%s yêu cầu cao tối thiểu %dcm, có %d trẻ chưa đủ"
                                                 % (ten, diem["chieu_cao_min_cm"], len(thieu_tre))})
            if not diem["trong_nha"] and mua_tu is not None and _khoang_cham(bd, kt, mua_tu, mua_den):
                vi_pham.append({"loai": "ngoai_troi_khi_mua",
                                 "chi_tiet": "%s ngoài trời — trùng khoảng mưa %s-%s"
                                             % (ten, weather["mua_tu"], weather["mua_den"])})

        muc_hop_le.append((muc, diem, bd, kt))

    # chong_gio + khong_kip_di: so các mục liên tiếp theo giờ bắt đầu
    muc_hop_le.sort(key=lambda x: x[2])
    for (m1, d1, bd1, kt1), (m2, d2, bd2, kt2) in zip(muc_hop_le, muc_hop_le[1:]):
        ten1 = m1.get("diem_id") or m1.get("show_id")
        ten2 = m2.get("diem_id") or m2.get("show_id")
        if bd2 < kt1:
            vi_pham.append({"loai": "chong_gio",
                             "chi_tiet": "%s (đến %s) chồng giờ với %s (bắt đầu %s)"
                                         % (ten1, m1["ket_thuc"], ten2, m2["bat_dau"])})
            continue  # chồng giờ thì không kiểm tiếp khong_kip_di cho cặp này
        gap = bd2 - kt1
        can_di = _travel().get((d1["id"], d2["id"]), 10)
        if gap < can_di:
            vi_pham.append({"loai": "khong_kip_di",
                             "chi_tiet": "Từ %s đến %s cần %d phút đi bộ, lịch chỉ chừa %d phút"
                                         % (ten1, ten2, can_di, gap)})

    tong_tien = tinh_tong_tien(lich, rang_buoc)
    if tong_tien["tong"] > rang_buoc.get("ngan_sach", float("inf")):
        vi_pham.append({"loai": "vuot_ngan_sach",
                         "chi_tiet": "Tổng %d vượt ngân sách %d"
                                     % (tong_tien["tong"], rang_buoc["ngan_sach"])})

    return vi_pham


def tinh_tong_tien(lich, rang_buoc):
    """Tính tổng tiền: vé vào cổng (theo số người lớn/trẻ em, trẻ dưới 1m4 miễn phí)
    + giá từng điểm chơi trong lịch (show không tính thêm, coi như đã gồm trong vé vào cổng)."""
    idx_diem = _index_diem()
    ve = _park()["ve_vao_cong"]
    so_nl = rang_buoc.get("nguoi_lon", 0)
    tre_em = rang_buoc.get("tre_em", [])
    so_tre_duoi_1m = sum(1 for te in tre_em if te.get("chieu_cao_cm", 9999) < 100)
    so_tre_tinh_tien = len(tre_em) - so_tre_duoi_1m

    ve_vao_cong = (so_nl * ve["nguoi_lon"] + so_tre_tinh_tien * ve["tre_em"]
                   + so_tre_duoi_1m * ve.get("tre_duoi_1m", 0))

    tien_diem = 0
    for muc in lich:
        if "diem_id" not in muc:
            continue
        d = idx_diem.get(muc["diem_id"])
        if not d:
            continue
        tien_diem += so_nl * d["gia"]["nguoi_lon"] + so_tre_tinh_tien * d["gia"]["tre_em"]

    return {"ve_vao_cong": ve_vao_cong, "diem": tien_diem, "tong": ve_vao_cong + tien_diem}
