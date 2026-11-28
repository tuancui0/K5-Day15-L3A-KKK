# Tóm tắt mô phỏng simulate-1@20261128-110117

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| xep_mot_lan | 8 | 1 | 2522 | 384 | 2.0 | 3.0 |
| sua_nhieu_lan | 20 | 3 | 6692 | 1031 | 5.5 | 8.1 |
| ngay_mua | 21 | 2 | 4055 | 655 | 3.4 | 5.1 |

Tỉ lệ đạt dùng để tính: 23/25 (92%) — lượt run-2@20261128-104450

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (200 người) | Chi phí / tháng — cơ sở (500 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0024 | $0.0026 | $0.0011 | $0.0576 | $0.1441 | $0.2882 | $0.00029 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0131 | $0.0142 | $0.0063 | $0.3179 | $0.7947 | $1.59 | $0.0016 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.2) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: cx/gpt-6-luna. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 1/50.
