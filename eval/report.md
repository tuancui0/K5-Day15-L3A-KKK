# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-234913` | 22/25 | 88% | 8/8 | 10/13 | 4/4 | Chưa đạt. B10 trả lịch khi yêu cầu bắt buộc bất khả thi. |
| 2 | Chờ chốt mã nguồn ở bước 11 | — | — | — | — | — | Chưa chấm |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Báo sai nguyên nhân khi báo không xếp được | 1 | B08 |
| Bỏ bớt yêu cầu bắt buộc rồi trả lịch | 1 | B10 |
| Giải thích dựa trên thời tiết sai | 1 | B22 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B08 | Bé cao 95 cm, gia đình muốn toàn trò tốc độ cao | “không còn trò nào vừa khung giờ”, gợi ý kéo dài giờ hoặc bớt trò xa | Cần giải thích giới hạn chiều cao và gợi ý đổi sở thích sang trò phù hợp cho bé. |
| B10 | Bắt buộc ít nhất 8 trò và 2 show từ 10:00 đến 12:30 | Trả lịch 3 trò và 1 show, ghi “không có vi phạm” | Lịch đã bỏ mức tối thiểu của cả hai nhóm. Cần báo không xếp được, giải thích giới hạn thời gian và đề xuất nới. |
| B22 | Đi ngày 08/12, đến 07:30, thích khu trẻ em và Rạp 4D | Nhà bóng lúc 09:05, Rạp 4D lúc 09:40. Chọn Nhà bóng vì “phù hợp sở thích khu trẻ em và trời mưa” | Lịch nằm trong giờ mở cửa, nhưng lý do nhắc mưa trong ngày được đánh dấu trời quang. |

## 3. Một lần cải tiến

- Chọn nhóm bỏ bớt yêu cầu bắt buộc (B10). Gia đình có thể dựa vào lịch để lên kế hoạch cho cả chuyến dù lịch thiếu các hoạt động họ yêu cầu. Lỗi này vướng điều kiện cứng ở §7.
- Trường cập nhật planner ở `dfe671a`. Planner lấy số trò và show tối thiểu, kiểm cận dưới thời lượng gồm thời gian chơi và chờ, rồi thử lại một lần nếu lịch nháp thiếu mục.
- Khi có lượt 2, ghi lại số câu mắc lỗi bỏ bớt yêu cầu bắt buộc (lượt 1 có 1 câu, B10) và đối chiếu tổng % với mốc 88%. Với B10, kiểm cả lời giải thích vì sao 150 phút không đủ và gợi ý nới. Liệt kê câu nào chuyển từ đạt sang trượt trên cùng bộ 25 câu.

## 4. Còn lại

- Hai lỗi lý do từ lượt 1 cần kiểm lại ở lượt 2. Báo sai nguyên nhân có thể khiến gia đình đổi khung giờ vô ích. Lý do thời tiết sai có thể khiến họ chuẩn bị sai cho ngày đi.
