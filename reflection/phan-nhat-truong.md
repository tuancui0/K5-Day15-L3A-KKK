# Reflection — Phan Nhật Trường

## 1. Vai trò và đóng góp

Mình phụ trách phần model và prompt của nhóm KKK. Phần kết nối `cx/gpt-6-luna` nằm trong [ai.py](../codebase/ai.py), còn ba bước trích ràng buộc, xếp lịch và sửa lịch nằm trong [planner.py](../codebase/planner.py).
Ở CP3, mình bổ sung ghi chép [P2](../evidence/interviews/P2.md), cập nhật [sơ đồ kiến trúc ở §4](../spec.md) và quay video chạy hai ca với model thật.
Ở CP4, mình sửa cách planner xử lý số lượng hoạt động bắt buộc (commit `dfe671a`) và chuẩn bị trang Giải pháp cùng video demo dự phòng.

## 2. AI hỗ trợ mình thế nào

Mình dùng Codex để soạn ba prompt, triển khai bước đọc JSON và chuẩn bị ca thử. [Khai báo dùng AI](../docs/ai-usage.md) ghi lại các phần có AI hỗ trợ.
Mình đối chiếu đầu ra CLI với validator và Data v2, đặc biệt ở ca điểm đóng hoặc show bị hủy.
Trong một lượt thử bản sửa CP4, B01 báo chưa xếp được dù khách chỉ nêu sở thích. Mình làm rõ trong prompt rằng số lượng tối thiểu bằng 0 nghĩa là linh hoạt. Khi thử lại, B01 xếp được lịch và ca có mức tối thiểu khả thi vẫn trả đủ số trò và show.

## 3. Một câu thử trượt và bài học

Ở B10, khách yêu cầu ít nhất 8 trò và 2 show trong 150 phút. Lượt 1 chỉ xếp 3 trò và 1 show dù lịch được ghi là không có vi phạm.
Mình bổ sung kiểm tra số lượng riêng cho trò và show. Nếu lịch nháp thiếu mục, planner thử lại một lần khi còn khả thi. Tuấn Anh nối phần giải thích vào luồng chính, và B10 qua ở lượt 2. [Báo cáo đánh giá](../eval/report.md)
Mình rút ra rằng kiểm từng mục trong lịch vẫn chưa đủ. Những yêu cầu bắt buộc của cả lịch cũng cần được trích rõ và kiểm lại bằng code trước khi trả kết quả.
