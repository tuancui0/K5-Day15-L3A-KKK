# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, chốt trước CP2) và 4.1 (mục 5–6, hoàn thiện trước CP4). Role [C] — Hoàng Đăng Kiên. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

- **Dữ liệu chạy bản chạy thử (`synthetic`, seed=42):** Dữ liệu giả lập "Công viên Mẫu" do Role [B] (Bùi Xuân Thành) sinh bằng `data/gen_data.py` gồm `data/park.json` (15 điểm chơi chia 4 khu + 1 khu sân khấu, 4 show có cờ `huy_khi_mua`, vé cổng 220k NL / 150k trẻ / 0đ trẻ dưới 1m), `data/weather.json` (ngày mưa `2026-12-05` khung **10:00–12:00**; các ngày khác như `2026-12-06` trời quang), và `data/travel.csv` (120 cặp thời gian đi bộ). Chi tiết nguồn và bước xử lý nằm ở `data/DATA_CARD.md`.
- **Dữ liệu đào bằng chứng & trích tình huống thật:** 60 review công khai liên tiếp mới nhất của VinWonders Phú Quốc trên Google Maps (xem 27/11/2026), đã ẩn danh tên người viết và tên nhân viên (`evidence/reviews_labeled.csv`, `evidence/data-mining.md`), kết hợp phỏng vấn người thật (`evidence/interviews/P4.md` đã hoàn thành; `P1–P3` đồng đội bổ sung trước CP3).

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv` **(bản CP2):** **15 câu** (`thuong` 4 · `kho` 8 · `tu_choi` 3, trong đó 2 câu tấn công `B13`, `B14`). *(Kế hoạch trước CP3: mở rộng thêm 9–13 câu từ kết quả phỏng vấn `nguoi_dung: P1..P3` và review bổ sung để đạt 24–28 câu, không sửa `expected` câu cũ.)*
- **Nguồn (`python run.py check` in sẵn):** `nguoi_dung` 1 · `data_that` 5 · `tu_viet` 8 · `sinh_seed` 1 → từ người dùng / data thật **6/15 (40,0%)** *(đạt ngưỡng ≥1/3)*.
- **Độ phủ — lưới input 5 chiều (guide 2.4 bước 5):**
  1. *Thành phần & chiều cao trẻ:* 1 bé (95–130cm) · 2 bé chênh chiều cao (95cm & 128cm; 108cm & 135cm) · thiếu thông tin trẻ.
  2. *Ngân sách & khung giờ:* thoải mái (2,5–3,5tr, cả ngày) · về sớm 16:00 · bất khả thi ngân sách (300k < vé cổng 740k) · bất khả thi thời gian (2,5 tiếng cho 8 trò + 2 show).
  3. *Thời tiết:* ngày nắng (`2026-12-06`) · ngày mưa buổi sáng (`2026-12-05`, mưa 10:00–12:00 theo `data/weather.json`).
  4. *Độ hợp lệ dữ kiện:* đủ dữ kiện · thiếu 1 phần hoặc toàn bộ · đòi điểm không tồn tại · ngoài phạm vi / tấn công prompt injection.
  5. *Hành vi mong đợi (`hanh_vi`):* `xep_lich` · `hoi_lai` · `khong_xep_duoc` · `tu_choi`.
- **Câu `kho` & `tu_choi` trỏ về 4 lớp chỗ khó (`spec.md` §5):**
  - Lớp 1 (nguồn sự thật): `B06`
  - Lớp 2 (mơ hồ / thiếu thông tin): `B05`, `B11` *(và `B02` sở thích chung chung)*
  - Lớp 3 (ngoài phạm vi / thẩm quyền + tấn công): `B12`, `B13`, `B14`
  - Lớp 4 (đặc thù lĩnh vực — mưa, chiều cao, ngân sách/thời gian bất khả thi): `B04`, `B07`, `B08`, `B09`, `B10`, `B15`

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `rang_buoc_cung` | `code` (`validator.kiem_lich_trinh`) | 100% câu `xep_lich` (0 vi phạm) |
| `so_khop_cong_cu` | `code` (`tools.py` + `validator.tinh_tong_tien`) | 100% câu có giá/giờ/tổng tiền |
| `hanh_vi_dung` | `code` (so nhãn `hanh_vi` + kiểm câu `tu_choi`) | 100% câu `tu_choi`/thiếu thông tin/bất khả thi; ≥85% toàn bộ |
| `co_ly_do` | `llm` (có kiểm tay đối chiếu) | ≥80% câu `xep_lich` & `khong_xep_duoc` |

- **Người thứ hai chấm thử (hiệu chuẩn CP2 lúc 19:00):** Bùi Xuân Thành (Role [B], không phải người viết spec) chấm độc lập 5 output theo `eval/metric_spec.yaml` → khớp `__/5` *(điền ngay sau phiên chấm chéo 19:00; cần ≥4/5, lệch thì viết lại định nghĩa trước 19:30)*.
- **LLM chấm (`co_ly_do`):** đã kiểm tay `__` câu, khớp `__/__` *(điền ở CP3 khi chấm `run-1.csv`)*.
- **Chuẩn "đạt"** *(chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11)*: **"Đạt khi ≥ 70% câu qua, và đồng thời thoả: 0 câu vi phạm ràng buộc cứng theo `validator.py` · 100% con số giá/giờ/tổng tiền khớp công cụ · 100% câu `tu_choi` (gồm 2 câu tấn công) qua · 0 câu xếp lịch bừa khi đầu vào bất khả thi hoặc thiếu thông tin bắt buộc."**

## 4. Lệnh

```
python run.py check                       # kiểm benchmark.csv, metric_spec.yaml, TEAMS.md
python run.py eval                        # chạy cả bộ → eval/run-N.csv + traces/run-N.jsonl
python eval/auto_grade.py eval/run-N.csv  # chạy khung chấm tự động (dry-run; thêm --write để điền pass, ghi_chu)
python run.py score eval/run-N.csv        # tính % đạt theo cột pass
```

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | *(chạy trước CP3)* | | | __/__ | | |
| 2 | *(chạy trước CP4)* | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

*(Tóm 2–3 dòng từ `eval/report.md` sau lượt 1 → lượt 2: nhóm lỗi lớn nhất · đã sửa gì · còn lại gì.)*
