# Data card — dữ liệu bản chạy thử dùng

> v2 — CP3 27/11/2026 (bản đầu v1: CP2 27/11/2026). Dữ liệu tự dựng, **không phải bằng chứng pain**
> (bằng chứng pain thật ở `evidence/data-mining.md`, `evidence/summary.md`, `evidence/interviews/`).

## Dataset 1 · Công viên mẫu (park.json + weather.json + travel.csv + closures.json)

| | |
|---|---|
| Dùng để làm gì | nguồn cho 4 công cụ ở `codebase/tools.py` (`tra_diem_choi`, `tra_lich_show`, `tra_thoi_tiet`, `uoc_thoi_gian_di`) · nguồn kiểm ràng buộc ở `codebase/validator.py` · bộ câu thử `eval/benchmark.csv` |
| Từ đâu | nhóm tự sinh, dựa trên cấu trúc khu vui chơi thật (tham khảo bố cục Đầm Sen / Suối Tiên) nhưng mọi tên điểm, giá, giờ đều là **hư cấu** — không lấy số liệu thật của công viên nào. Các ca "bẩn" v2 dựng theo đúng tình huống kể lại trong `evidence/interviews/P1.md`, `P3.md` |
| Xử lý những bước gì | sinh bằng script `data/gen_data.py` (seed=42): 15 điểm cố định tay (tên, giá, giờ, chiều cao tối thiểu) chia 4 khu + 1 khu sân khấu, 4 show; toạ độ mỗi điểm sinh ngẫu nhiên quanh tâm khu (`random.seed(42)`) rồi suy ra thời gian đi bộ giữa mọi cặp điểm (tốc độ 70m/phút) ghi vào `travel.csv`; v2 thêm `closures.json` (điểm đóng bảo trì / show huỷ đột xuất theo ngày, khai tay, không qua random) |
| Số dòng / số đoạn | 15 điểm chơi · 4 show · 1 ngày mưa · 2 ngày có sự cố đóng/huỷ đột xuất (closures.json) · 120 cặp thời gian di chuyển (15 điểm + cổng, mọi cặp) |
| Phiên bản / ngày lấy | **v2** — sinh lại được bất cứ lúc nào bằng `python data/gen_data.py` (seed cố định, kết quả không đổi); v1: CP2 27/11/2026 |
| Nhãn | `synthetic` (tự sinh) |
| Giới hạn | chỉ 1 ngày mưa + 2 ngày sự cố dựng sẵn — các ngày khác coi như trời quang, không có sự cố; giá vé/giờ là ước lượng tham khảo thực tế, không phải giá niêm yết thật; chưa có ca "ngày không thể giải trọn vẹn" (kết hợp nhiều ràng buộc cứng cùng lúc) — cần nếu `eval/benchmark.csv` muốn thêm câu thử loại này |

**Cách sinh:** `data/gen_data.py`, seed=42. 15 điểm + 4 show khai tay trong script (để kiểm soát chieu_cao_min_cm, giờ mở/đóng dùng cho câu thử); toạ độ và thời gian di chuyển sinh bằng `random.seed(42)` nên luôn ra cùng một kết quả. Người kiểm: [B] (Bùi Xuân Thành) — đã chạy `test_validator.py` (12/12 qua) để xác nhận dữ liệu và validator khớp nhau.

### v2 (CP3) — dữ liệu "bẩn" mới thêm

Theo guide 3.3, bổ sung 2 ca sự cố phát sinh riêng cho 1 ngày cụ thể (khác giờ đóng cố định hay huỷ khi mưa đã có sẵn ở v1), ghi trong `data/closures.json`:

| Ngày | Sự cố | Khớp bằng chứng phỏng vấn |
|---|---|---|
| 2026-12-06 | `D09` (Máng trượt cao tốc) đóng bảo trì đột xuất cả ngày | P1: *"đến nơi mới biết bé không đủ chiều cao"* + chung mô-típ "đến nơi mới biết không chơi được" |
| 2026-12-07 | `S03` (Múa rối nước) huỷ vì sự cố kỹ thuật, không liên quan mưa | P3: *"qua tới thủy cung thì show đang diễn rồi"* — lỡ show vì không biết trước lịch thay đổi |

`codebase/validator.py` thêm 2 loại vi phạm mới đọc file này: `diem_dong_dot_xuat`, `show_huy_dot_xuat` (tổng 9 → 11 loại). Agent hiện **không** biết trước các sự cố này qua 4 công cụ (tools.py không đổi hợp đồng) — đúng tinh thần dữ liệu "bẩn": validator là lưới chặn cuối cùng bắt lịch lỡ xếp vào điểm/show đang gặp sự cố, mô phỏng đúng trải nghiệm thật của người được phỏng vấn (không biết trước, chỉ phát hiện khi đã đến nơi). Nếu Trường/Tuấn Anh muốn agent chủ động tránh các ca này khi lập lịch (thay vì chỉ bị validator bắt sau), cần thêm cách đọc `closures.json` vào `ai.py`/`spec.md` §4 — phần này ngoài phạm vi sở hữu file của [B] nên chưa làm, để team bàn thêm.

Ngân sách sát/vượt dự tính (P1: chi 3 triệu so với dự tính 2,5 triệu) không cần dữ liệu mới — đã có sẵn cơ chế `vuot_ngan_sach` trong validator, chỉ cần `eval/benchmark.csv` đặt `ngan_sach` sát với tổng chi thực tế của một lịch mẫu.

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
