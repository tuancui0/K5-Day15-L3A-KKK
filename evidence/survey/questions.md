# Khảo sát — bộ câu hỏi, cách gửi, kết quả

- **Công cụ:** Google Form, kết quả lưu ở Google Sheet của nhóm.
- **Kênh gửi:** Zalo, Facebook
- **Mở / chốt:** câu trả lời đầu tiên 27/11/2026 3:07 · câu trả lời cuối lấy về 27/11/2026 6:52 (form vẫn mở).
- **Số câu trả lời:** n = 20 · bản ẩn danh: [`results.csv`](results.csv) (đã bỏ cột "Cách liên hệ"; mã `S01`…`S20` theo thứ tự thời gian).

## Bộ câu hỏi (nguyên văn trên form)

| # | Câu hỏi | Kiểu trả lời | Cột trong `results.csv` |
|---|---|---|---|
| 1 | Bạn là | Chọn một (Phụ huynh có con 3–10 tuổi / Chưa có con / …) | `ban_la` |
| 2 | Lần gần nhất bạn đi khu vui chơi lớn cùng con nhỏ (VinWonders, Sun World, Đầm Sen, Suối Tiên…) là khi nào? | Trong tháng này · 1–3 tháng trước · 3–12 tháng trước · Hơn 1 năm · Chưa bao giờ | `lan_gan_nhat` |
| 3 | Trước chuyến đi đó, bạn có lên kế hoạch trước (giờ chơi, giờ show, trò nào trước/sau) không? | Có lên kỹ · Có nhưng sơ sài · Không, tới đâu tính đó | `len_ke_hoach` |
| 4 | Bạn dựa vào đâu để lên kế hoạch / quyết định tại chỗ? | Chọn nhiều (Web khu vui chơi · Hỏi người quen / review mạng · App bản đồ công viên · Hỏi ChatGPT / AI · Không dựa gì, tới đâu tính đó) | `dua_vao_dau` |
| 5 | Trong chuyến đó, có lần nào lỡ show / trò con muốn xem vì đến sai giờ hoặc trùng giờ việc khác không? | Có, ≥1 lần · Không · Không nhớ rõ | `lo_show_tro` |
| 6 | Có lần nào đến một trò rồi mới biết con không đủ chiều cao/tuổi để chơi không? | Có · Không | `khong_du_chieu_cao` |
| 7 | Có gặp mưa hoặc show bị huỷ giữa chuyến và phải xếp lại kế hoạch tại chỗ không? | Có · Không | `mua_show_huy_xep_lai` |
| 8 | Tính chung cả ngày, bạn thấy chi tiêu thực tế so với dự tính thế nào? | Đúng dự tính · Hơi vượt · Vượt khá nhiều | `chi_tieu_vs_du_tinh` |
| 9 | Điều gì khó chịu nhất trong việc lên kế hoạch / xử lý phát sinh hôm đó? | Đoạn văn | `kho_chiu_nhat` |
| 10 | (Tuỳ chọn) Nếu có công cụ AI tự xếp lịch theo ngân sách, sở thích, giờ giấc và chiều cao/tuổi của con — bạn có muốn nhóm phỏng vấn thêm 10 phút không? | Có — để lại cách liên hệ / Không | `muon_phong_van_them` |
| 11 | Cách liên hệ với bạn (số điện thoại / Zalo / email) | Ngắn — **đã xoá khỏi `results.csv`** | — |

## Kết quả (đếm lại được từ `results.csv`)

**Đạt ngưỡng chưa:** có 20 câu trả lời nhưng **chưa đạt** ngưỡng "≥20 người đúng người dùng". Chỉ **4/20** là phụ huynh có con 3–10 tuổi; 16/20 chọn "Chưa có con"; 8/20 chưa từng đi khu vui chơi lớn cùng con nhỏ.

Nên chỉ đếm hành vi trên những người **đã từng đi** cùng con nhỏ (câu 2 ≠ "Chưa bao giờ"). Nhóm nhỏ nên ghi x/n, không ghi %.

| Câu | Đã từng đi cùng con nhỏ (n = 12) | Trong đó phụ huynh có con 3–10 tuổi (n = 4) |
|---|---|---|
| Lỡ show / trò vì sai giờ, trùng giờ (câu 5: "Có, ≥1 lần") | 8/12 (3 "không nhớ rõ") | 3/4 |
| Đến nơi mới biết con không đủ chiều cao / tuổi (câu 6: "Có") | 9/12 | 4/4 |
| Gặp mưa / show huỷ, phải xếp lại tại chỗ (câu 7: "Có") | 8/12 | 4/4 |
| Chi tiêu vượt dự tính (câu 8: "Hơi vượt" + "Vượt khá nhiều") | 10/12 | 3/4 |
| Lên kế hoạch kỹ trước (câu 3: "Có lên kỹ") | 1/12 (9 "sơ sài", 2 "tới đâu tính đó") | 0/4 (4 "sơ sài") |
| Muốn được phỏng vấn thêm (câu 10: "Có") | 8/12 | 3/4 |

## Trích nguyên văn (câu 9)

- S02 · phụ huynh có con 3–10 tuổi: "thông tin thiếu sự nhất quán không rõ ràng đi từ 7h 30 mà 8h 30 mới mở"
- S09 · phụ huynh có con 3–10 tuổi: "Không căn chỉnh được thời gian xếp hàng để tham gia các trò chơi"
- S08 · chưa có con, đi 1–3 tháng trước: "Thông tin không tập trung"
- S06 · chưa có con, đi 3–12 tháng trước: "trời quá nắng nóng, không đi chơi được nhiều trò"
- S07 · chưa có con, đi 1–3 tháng trước: "Vì ảnh hưởng mà không có buổi vui chơi trọn vẹn"

## Hạn chế

- Mẫu lệch: phần lớn người trả lời chưa có con, không phải người dùng chính của lát cắt.
- Câu 2 hỏi "cùng con nhỏ" nhưng 8 người "chưa có con" vẫn chọn đã từng đi — có thể đi cùng cháu / em nhỏ, form không hỏi rõ.
- Câu 5–9 vẫn được trả lời bởi người chọn "Chưa bao giờ" ở câu 2, nên các câu trả lời đó không tính vào bảng trên.
- Tiếp: gửi form vào nhóm phụ huynh để đủ ≥20 phụ huynh; 3 phụ huynh đồng ý phỏng vấn thêm → ứng viên cho `evidence/interviews/`.
