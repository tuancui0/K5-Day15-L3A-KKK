# Reflection — Bùi Xuân Thành

## 1. Vai trò và đóng góp

Phụ trách vai trò B (Dữ liệu & công cụ) của nhóm KKK: dữ liệu công viên mẫu, `codebase/tools.py`, `codebase/validator.py`, `data/DATA_CARD.md` và toàn bộ phần `cost/` (persona, mô phỏng, chi phí).
Phỏng vấn 2 người (`P1`, `P3` — commit `db7cc3c`), sau đó thêm dữ liệu "bẩn" v2 cho CP3: `data/closures.json` (điểm đóng bảo trì, show huỷ đột xuất) lấy đúng từ 2 bằng chứng phỏng vấn đó, nâng `validator.py` từ 9 lên 11 loại vi phạm (commit `b21b4c8`).
Sang CP4, viết `cost/personas.yaml` với 3 persona đúng tên trong `spec.md` §2 (`xep_mot_lan`, `sua_nhieu_lan`, `ngay_mua`, commit `5fb5bfd`), chạy mô phỏng chính thức 50 phiên dựa trên tỉ lệ đạt lượt 2 (commit `ce80f1f`) và viết `cost/cost-estimate.md` (commit `1882bf6`).

## 2. Sử dụng AI và kiểm tra kết quả

Dùng Claude Code để soạn nháp 5–6 câu hỏi phỏng vấn kiểu Mom Test (hỏi hành vi/số cụ thể, không hỏi ý kiến về giải pháp), và để viết code `closures.json`/`tools.py`/`validator.py`/`gen_data.py`.
Mình tự đặt câu hỏi và ghi chép khi phỏng vấn thật — AI chỉ rà câu dẫn dắt trước và sửa định dạng/tiêu đề lệch persona sau khi ghi (bản đầu AI viết tiêu đề "người trung tuổi" sai với persona nhóm nhắm, mình phải yêu cầu sửa lại).
Với code, mọi thay đổi đều chạy `codebase/test_validator.py` (12/12 qua) trước khi commit, và đối chiếu lại với `eval/benchmark.csv` của Kiên (câu B20, B21 dùng đúng ngày/điểm trong `closures.json`) để chắc dữ liệu hai bên khớp nhau, không tự tin theo lời AI nói là đúng. Phần khai AI chi tiết ở `docs/ai-usage.md`.

## 3. Một câu thử trượt và bài học

Ở lượt 2, câu B21 (show `S03` bị huỷ đột xuất ngày 2026-12-07, không liên quan mưa — đúng ca mình thêm ở `closures.json`) vẫn bị chấm trượt: agent xếp lịch đúng, tính tiền đúng, loại đúng show khỏi lịch, nhưng phần giải thích lại viện dẫn nhầm sang lý do trời mưa cho đúng ngày đó dù `weather.json` không có mưa ngày này.
Bài học là viết dữ liệu "bẩn" đúng và validator bắt đúng vi phạm (phần của mình) chưa đủ — câu trả lời bằng lời của model vẫn có thể sai dù hành vi xếp lịch đúng, nên cần kiểm cả lý do giải thích chứ không chỉ kiểm lịch trình/số tiền có hợp lệ hay không. Đây là phần Trường cần sửa tiếp ở prompt, nhưng nhắc mình rằng khi thêm loại dữ liệu bẩn mới, nên đề xuất luôn một câu thử kiểm riêng phần "lý do" chứ không chỉ phần "có bắt được vi phạm không".
