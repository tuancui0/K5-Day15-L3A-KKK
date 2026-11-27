# Data card — dữ liệu bản chạy thử dùng

> Bản đầu — CP2 27/11/2026. Dữ liệu tự dựng, **không phải bằng chứng pain**
> (bằng chứng pain thật ở `evidence/data-mining.md`, `evidence/summary.md`).

## Dataset 1 · Công viên mẫu (park.json + weather.json + travel.csv)

| | |
|---|---|
| Dùng để làm gì | nguồn cho 4 công cụ ở `codebase/tools.py` (`tra_diem_choi`, `tra_lich_show`, `tra_thoi_tiet`, `uoc_thoi_gian_di`) · nguồn kiểm ràng buộc ở `codebase/validator.py` · bộ câu thử `eval/benchmark.csv` |
| Từ đâu | nhóm tự sinh, dựa trên cấu trúc khu vui chơi thật (tham khảo bố cục Đầm Sen / Suối Tiên) nhưng mọi tên điểm, giá, giờ đều là **hư cấu** — không lấy số liệu thật của công viên nào |
| Xử lý những bước gì | sinh bằng script `data/gen_data.py` (seed=42): 15 điểm cố định tay (tên, giá, giờ, chiều cao tối thiểu) chia 4 khu + 1 khu sân khấu, 4 show; toạ độ mỗi điểm sinh ngẫu nhiên quanh tâm khu (`random.seed(42)`) rồi suy ra thời gian đi bộ giữa mọi cặp điểm (tốc độ 70m/phút) ghi vào `travel.csv` |
| Số dòng / số đoạn | 15 điểm chơi · 4 show · 1 ngày mưa · 120 cặp thời gian di chuyển (15 điểm + cổng, mọi cặp) |
| Phiên bản / ngày lấy | v1 — sinh lại được bất cứ lúc nào bằng `python data/gen_data.py` (seed cố định, kết quả không đổi) |
| Nhãn | `synthetic` (tự sinh) |
| Giới hạn | chỉ 1 ngày mưa dựng sẵn (2026-12-05) — các ngày khác coi như trời quang; giá vé/giờ là ước lượng tham khảo thực tế, không phải giá niêm yết thật; chưa có dữ liệu "bẩn" (điểm đóng đột xuất, show huỷ ngoài kế hoạch) — sẽ bổ sung trước CP3 theo guide 3.3 |

**Cách sinh:** `data/gen_data.py`, seed=42. 15 điểm + 4 show khai tay trong script (để kiểm soát chieu_cao_min_cm, giờ mở/đóng dùng cho câu thử); toạ độ và thời gian di chuyển sinh bằng `random.seed(42)` nên luôn ra cùng một kết quả. Người kiểm: [B] (Bùi Xuân Thành) — đã chạy `test_validator.py` (10/10 qua) để xác nhận dữ liệu và validator khớp nhau.

## Dataset 2 · Review công khai (đào bằng chứng)

| | |
|---|---|
| Dùng để làm gì | bằng chứng pain — xem chi tiết `evidence/data-mining.md`, `evidence/summary.md` |
| Từ đâu | review công khai trên Google Maps (Công Viên Nước Đầm Sen) |
| Xử lý những bước gì | đọc trực tiếp, trích tối đa 2 câu/review, ẩn danh người viết (mã R1, R2…), ghi link + ngày xem |
| Số dòng / số đoạn | ~24 review đã đọc, 10 trích dẫn đưa vào bằng chứng |
| Phiên bản / ngày lấy | 27/11/2026 |
| Nhãn | thật |
| Giới hạn | 1 địa điểm, chưa đa dạng theo vùng miền/loại hình công viên; nhóm nên đọc thêm ở Suối Tiên hoặc công viên khác trước CP3 để đối chiếu |
