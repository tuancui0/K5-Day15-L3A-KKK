# Reflection — Đỗ Tuấn Anh

## 1. Vai trò và đóng góp

Mình là đội trưởng nhóm KKK, phụ trách luồng chính [agent.py](../codebase/agent.py), `spec.md` §0–3, phần tổng hợp bằng chứng pain, slide và nộp checkpoint.
Ở CP3, mình ẩn danh và tổng hợp khảo sát n = 20 vào [evidence/survey/](../evidence/survey/) (commit `a56966b`), viết [summary.md](../evidence/summary.md) và `spec.md` §0–3 từ phỏng vấn P1–P4 (`0135c0b`), rồi nối `agent.py` với planner, tools, validator thật và bỏ bản giả (`53ccde1`).
Ở CP4, mình thêm kiểm tra số trò / show bắt buộc vào luồng chính để B10 giải thích đúng lý do (`35a6037`), và ghép 8 trang thành [demo-slides.pdf](../demo-slides.pdf) (`152b51a`).

## 2. AI hỗ trợ mình thế nào

Mình dùng Claude Code để soạn nháp `summary.md`, `spec.md` §0–3, ẩn danh khảo sát, sửa nhỏ `agent.py` và dựng slide. Chi tiết trong [khai báo dùng AI](../docs/ai-usage.md).
Mình tự chọn cách đếm khảo sát: chỉ tính 12 người đã đi cùng con nhỏ và ghi x/n, không ghi % vì n nhỏ. Mình đối chiếu từng số với file nguồn trước khi commit.
Chỗ phải sửa lại: lần đầu trung vị thời gian bị tính sai, phải tính lại thành ~35 phút chuẩn bị + ~35 phút vô ích. Bản slide đầu tiên quá nhiều chữ, mình yêu cầu viết lại thành số to và sơ đồ, đồng thời đổi tiêu đề trang chi phí cho đúng ý so sánh với thời gian mất.

## 3. Một câu thử trượt và bài học

Ở B08 lượt 1, bé cao 95 cm và gia đình muốn toàn trò tốc độ cao. Luồng chính trả về câu "không còn trò nào vừa khung giờ" và gợi ý kéo dài giờ, trong khi lý do thật là chiều cao của bé.
Câu đó là câu dự phòng chung mình viết trong `agent.py` cho trường hợp planner trả lịch rỗng, nên nó che mất nguyên nhân thật. B10 cũng bị cùng vấn đề, mình sửa bằng cách lấy lý do cụ thể từ planner (`35a6037`).
Bài học: khi hệ thống từ chối xếp lịch, câu giải thích quan trọng ngang với quyết định. Câu dự phòng chung dễ làm phụ huynh nới sai ràng buộc. Mỗi nhánh "không xếp được" cần mang theo lý do riêng của nó.
