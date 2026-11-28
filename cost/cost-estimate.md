# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu, đúng tên dùng trong `spec.md` §2:
  - `xep_mot_lan` — share 15% · ~0,125 phiên/người/tháng (≈1–2 chuyến/năm) · 1 lượt hỏi/phiên. Nguồn: `spec.md` §2 ("không ai trong P1–P4 giữ nguyên lịch cả ngày; giữ làm persona tối thiểu").
  - `sua_nhieu_lan` — share 35% · ~0,125 phiên/người/tháng · 3 lượt hỏi/phiên. Nguồn: P1 (~3 lần sửa), P2 (2–3 lần), P3 (2 lần) — `evidence/interviews/`.
  - `ngay_mua` — share 50% · ~0,125 phiên/người/tháng · 2 lượt hỏi/phiên. Nguồn: P4 + 8/12 người khảo sát gặp mưa/show huỷ giữa ngày — `evidence/summary.md`.
- **Số người dùng thật** 3 kịch bản: thấp **200** · cơ sở **500** · cao **1.000** gia đình/tháng (đơn vị: lượt yêu cầu lập lịch/tháng nếu tích hợp vào web công viên). Nguồn: **(tự ước tính)** — `spec.md` §2 ghi rõ số gia đình/tháng thật vẫn **chưa có nguồn công khai tách riêng cho 1 công viên** (chỉ tìm được số khách toàn đảo Phú Quốc ~8,1 triệu lượt/năm 2025 — VnExpress, không tách được bao nhiêu đi VinWonders hay đi cùng trẻ nhỏ, nên không dùng để suy ra con số "có nguồn" giả tạo). Giữ 3 mức tạm ở quy mô nhỏ-vừa-lớn hợp lý cho một tính năng mới trên 1 website để minh hoạ độ nhạy chi phí theo quy mô, không phải số dự báo kinh doanh.
- **Giá** 2 mức model (`further-reading/model-prices.md` / Google AI pricing, xem 25/11/2026): `gemini-3.1-flash-lite` (vào $0,25 · ra $1,50 /1M token) · `gemini-4-hydrogen` (vào $1,50 · ra $7,50 /1M token).
- **Tỉ lệ đạt** dùng để tính: **23/25 (92%)** — lượt `run-2` (lượt 2, sau khi Trường sửa nhóm lỗi B10).
- Đo token trên model `cx/gpt-6-luna`, tính giá theo `gemini-3.1-flash-lite` và `gemini-4-hydrogen` (model khác nhau — bộ tách token có thể lệch, xem mục token ở `cost/simulate-1-summary.md`).

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-110117` · 50 phiên (1 phiên lỗi timeout, không tính vào trung bình) · seed 42

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| xep_mot_lan | 8 | 1 | 2522 | 384 | 2,0 | 3,0 |
| sua_nhieu_lan | 20 | 3 | 6692 | 1031 | 5,5 | 8,1 |
| ngay_mua | 21 | 2 | 4055 | 655 | 3,4 | 5,1 |

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (200) | / tháng — cơ sở (500) | / tháng — cao (1.000) | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| gemini-3.1-flash-lite | $0,0024 | $0,0026 | $0,0576 | $0,1441 | $0,2882 | $0,00029 |
| gemini-4-hydrogen | $0,0131 | $0,0142 | $0,3179 | $0,7947 | $1,59 | $0,0016 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt (92%) — **không coi như đạt 100%**.

## 3. So với impact

- Impact / tháng (`spec.md` §2, hướng H1 đã chọn): **thời gian**, không phải tiền — mỗi gia đình đi chơi mất thêm ước ~35 phút chuẩn bị + ~35 phút vô ích mỗi chuyến (trung vị P1–P4), cộng ~1–2 show/trò bị lỡ. Số gia đình/tháng dùng để quy ra giờ/tháng **vẫn chưa có nguồn công khai** (spec §2 ghi "__ gia đình — cần nguồn", chưa tìm được nguồn tách riêng theo công viên trong thời gian CP3–CP4), nên không quy đổi impact ra một số giờ/tháng chắc chắn ở đây.
- Chi phí / người / tháng (cơ sở, model `gemini-3.1-flash-lite`): **$0,00029** (~7 đồng/người/tháng theo tỷ giá tham khảo) — ở mức mạnh hơn (`gemini-4-hydrogen`): **$0,0016** (~40 đồng/người/tháng).
- **Kết luận một dòng — đáng làm không:** Đáng làm — dù chưa quy đổi được impact ra tiền do thiếu số gia đình/tháng có nguồn, chi phí vận hành mỗi người mỗi tháng ở cả 2 mức model đều dưới 1 xu Mỹ (dưới trăm đồng Việt), quá nhỏ so với pain thật đang đo được bằng thời gian (35–120 phút vô ích + lỡ show mỗi chuyến, theo `evidence/summary.md`); rủi ro chính không nằm ở chi phí model mà ở việc 2/25 câu thử lượt 2 còn trượt (B13, B21) — nên ưu tiên sửa tiếp trước khi mở rộng số người dùng thật.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Chưa làm — ngoài phạm vi CP4, để lại nếu nhóm còn thời gian sau khi nộp.
