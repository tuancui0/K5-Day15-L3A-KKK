# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Codex | Hỗ trợ nối gateway và viết phần đọc JSON, lọc mục khả thi và tính giờ bằng dữ liệu công viên | Đã chạy thử qua CLI và đối chiếu lịch với validator | Phan Nhật Trường |
| Prompt / thiết kế lời gọi mô hình | Codex, cx/gpt-6-luna | Soạn ba prompt trích, xếp và sửa. Thử đầu ra thật trên các ca thiếu dữ liệu, điểm đóng và show hủy | Đã đối chiếu tên điểm, giờ, lý do phản hồi và hành vi với dữ liệu v2 | Phan Nhật Trường |
| Bằng chứng, spec §0–3, luồng chính | Claude Code | Soạn nháp `evidence/summary.md`, `spec.md` §0–3, ẩn danh khảo sát (`evidence/survey/`) và sửa nhỏ `agent.py` theo yêu cầu | Tuấn Anh quyết định nội dung và phạm vi, chọn cách đếm (chỉ tính người đã đi cùng con nhỏ, ghi x/n), duyệt từng số với file nguồn và tự commit | Đỗ Tuấn Anh |
| Đào data (viết script đếm, gợi ý nhãn) | Antigravity | Hỗ trợ thu thập 60 review công khai mới nhất trên Google Maps (VinWonders Phú Quốc, 27/11/2026), gợi ý gắn nhãn 6 nhóm vào `evidence/reviews_labeled.csv`, viết `evidence/count_reviews.py` và soạn nháp `evidence/data-mining.md` | Kiên chốt quy tắc gán nhãn trước khi đếm, ẩn danh toàn bộ tác giả và giới hạn ≤2 câu/review, chạy lại `evidence/count_reviews.py` khớp 60/60 dòng và rà trực tiếp 7/7 ví dụ có tín hiệu C1 | Hoàng Đăng Kiên |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | Antigravity | Soạn nháp `eval/benchmark.csv` (15 câu CP2, mở rộng 25 câu CP3), `eval/metric_spec.yaml`, `eval/README.md` và `spec.md` §5–§7 theo lưới input 5 chiều và dữ kiện từ `P1`–`P4` + review | Kiên kiểm độ phủ 4 lớp chỗ khó + 2 câu tấn công, gắn `source` thật cho từng câu (13/25 = 52% từ `nguoi_dung`/`data_that`; không sửa `expected` câu cũ hay chuẩn "đạt" sau CP2), chạy `python run.py check` sạch và duyệt trước khi push | Hoàng Đăng Kiên |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | Antigravity *(chưa dùng LLM chấm ở lượt 1)* | Viết `eval/auto_grade.py` kiểm tự động bằng code 3 metric (`rang_buoc_cung`, `so_khop_cong_cu`, `hanh_vi_dung`) qua `validator.py` và hỗ trợ rà output `eval/run-1.csv`; chưa bật LLM chấm cho `co_ly_do` | Kiểm tra thủ công 25/25 câu của `eval/run-1.csv` (phát hiện 3 câu trượt `B08`, `B10`, `B22`), chạy `python run.py score eval/run-1.csv` ra 22/25 (88%), không sửa `output`/`tokens` | Hoàng Đăng Kiên |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
