# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Bố mẹ có con nhỏ tới trò mới biết bé không được chơi · 4/4 phỏng vấn · 8/12 khảo sát lỡ show · 35–120' mất vô ích · trích P3 | `evidence/summary.md` | ☑ |
| 2 | Vì sao chọn bài này | H1 chọn (~70' / chuyến) · H2 gộp làm câu thử khó · H3 loại (không có data chờ hàng) · web công viên và chatbot chưa giải được | `spec.md` §2–3 | ☑ |
| 3 | Giải pháp | Luồng 4 bước: trích → đề xuất → kiểm bằng code (sửa ≤3 lượt) → trả lịch · giờ / giá chỉ lấy từ dữ liệu · không xếp bừa · phụ huynh tự đặt vé | `spec.md` §4 | ☑ |
| 4 | Demo live | B01 (thường, 800.000 ₫, 0 vi phạm) + B10 (khó, 150' không đủ 8 trò + 2 show); video dự phòng trên Drive | `eval/benchmark.csv` | ☑ |
| 5 | **Đánh giá thế nào** | 25 câu (8 · 13 · 4), 13/25 từ người dùng / data thật · lượt 1 22/25 (88%) `run-1@20261127-234913` → lượt 2 23/25 (92%) `run-2@20261128-104450` · chưa đạt §7 vì từ chối 3/4 (B13) | `eval/README.md`, `eval/report.md` | ☑ |
| 6 | **Chi phí khi dùng thật** | $0,0026 – $0,0142 / task thành công · 200 / 500 / 1.000 gia đình *(tự ước tính)* · so với ~70' mất mỗi chuyến | `cost/cost-estimate.md` | ☑ |
| 7 | Kết luận | **Iterate**: pain có thật ✓ · chi phí rẻ ✓ · chất lượng chưa đạt §7 ✗ | trang 1, 5, 6 | ☑ |
| 8 | Nếu có thêm 1 tuần | Chặn giả danh B13 bằng code · lý do thời tiết đúng ngày (B21) · khảo sát đủ 20 phụ huynh và thử với phụ huynh thật | `eval/report.md` mục 4 · `evidence/summary.md` | ☑ |

Bản xuất: `demo-slides.pdf` ở thư mục gốc · nguồn HTML `slides/demo-slides.html`.

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| 1 · Người dùng & pain, 2 · Vì sao chọn | Đỗ Tuấn Anh |
| 3 · Giải pháp, 4 · Demo live | Phan Nhật Trường |
| 5 · Đánh giá thế nào | Hoàng Đăng Kiên |
| 6 · Chi phí khi dùng thật | Bùi Xuân Thành |
| 7 · Kết luận, 8 · Nếu có thêm 1 tuần | Đỗ Tuấn Anh |
