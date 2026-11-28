# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, chốt trước CP2) và 4.1 (mục 5–6, hoàn thiện trước CP4). Role [C] — Hoàng Đăng Kiên. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

- **Dữ liệu chạy bản chạy thử (`synthetic`, seed=42, v2):** Dữ liệu giả lập "Công viên Mẫu" do Role [B] (Bùi Xuân Thành) sinh bằng `data/gen_data.py` gồm `data/park.json` (15 điểm chơi chia 4 khu + 1 khu sân khấu, 4 show có cờ `huy_khi_mua`, vé cổng 220k NL / 150k trẻ / 0đ trẻ dưới 1m), `data/weather.json` (ngày mưa `2026-12-05` khung **10:00–12:00**; các ngày khác trời quang), `data/travel.csv` (120 cặp thời gian đi bộ), và **v2 `data/closures.json`** (sự cố đột xuất: `2026-12-06` đóng `D09`, `2026-12-07` huỷ show `S03`; `validator.py` kiểm 11 loại vi phạm). Chi tiết nguồn và bước xử lý nằm ở `data/DATA_CARD.md`.
- **Dữ liệu đào bằng chứng & trích tình huống thật:** 60 review công khai liên tiếp mới nhất của VinWonders Phú Quốc trên Google Maps (xem 27/11/2026, `evidence/reviews_labeled.csv`, `evidence/data-mining.md`), kết hợp 4 bài phỏng vấn người thật (`evidence/interviews/P1.md`–`P4.md`) và khảo sát ẩn danh $n = 20$ (`evidence/survey/results.csv`).

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv` **(bản CP3 — chỉ thêm `B16`–`B25`, giữ nguyên `B01`–`B15` đã chốt ở CP2):** **25 câu** (`thuong` 8 · `kho` 13 · `tu_choi` 4, trong đó 2 câu tấn công `B13`, `B14`).
- **Nguồn (`python run.py check` in sẵn):** `nguoi_dung` 7 · `data_that` 6 · `tu_viet` 9 · `sinh_seed` 3 → từ người dùng / data thật **13/25 (52,0%)** *(vượt ngưỡng ≥1/3)*.
- **Độ phủ — lưới input 5 chiều (guide 2.4 bước 5):**
  1. *Thành phần & chiều cao trẻ:* 1 bé (90–145cm, gồm bé <1m miễn vé `B19`) · 2 bé chênh chiều cao (95/128cm · 100/122cm · 102/122cm · 105/122cm · 108/135cm · 115/130cm) · thiếu thông tin trẻ.
  2. *Ngân sách & khung giờ:* thoải mái (1,2–3,5tr) · ngân sách sát vé cổng (`740k` = 0đ trò thu phí `B23`) · bất khả thi ngân sách (`300k` < `740k` `B09`) · đến sớm trước giờ mở (`07:30` `B22`) · điểm đóng sớm `16:30` (`B24`) · về sớm `16:00` (`B04`) · bất khả thi thời gian (`2,5h` cho 8 trò + 2 show `B10`).
  3. *Thời tiết & sự cố đột xuất (Data v2):* ngày nắng (`2026-12-08`, `2026-12-06`) · ngày mưa buổi sáng (`2026-12-05`, mưa 10:00–12:00) · đóng bảo trì đột xuất `D09` (`2026-12-06` `B20`) · huỷ show đột xuất `S03` (`2026-12-07` `B21`).
  4. *Độ hợp lệ dữ kiện:* đủ dữ kiện · thiếu 1 phần hoặc toàn bộ · đòi điểm không tồn tại · ngoài phạm vi (đặt vé/hoàn vé/số tài khoản) · tấn công prompt injection.
  5. *Hành vi mong đợi (`hanh_vi`):* `xep_lich` · `hoi_lai` · `khong_xep_duoc` · `tu_choi`.
- **Câu `kho` & `tu_choi` trỏ về 4 lớp chỗ khó (`spec.md` §5):**
  - Lớp 1 (nguồn sự thật): `B06`
  - Lớp 2 (mơ hồ / thiếu thông tin): `B05`, `B11` *(và `B02` sở thích chung chung)*
  - Lớp 3 (ngoài phạm vi / thẩm quyền + tấn công): `B12`, `B13`, `B14`, `B25`
  - Lớp 4 (đặc thù lĩnh vực — mưa, chiều cao, ngân sách sát/bất khả thi, giờ mở/đóng sớm, sự cố đột xuất v2): `B04`, `B07`, `B08`, `B09`, `B10`, `B15`, `B18`, `B20`, `B21`, `B22`, `B23`

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `rang_buoc_cung` | `code` (`validator.kiem_lich_trinh`) | 100% câu `xep_lich` (0 vi phạm) |
| `so_khop_cong_cu` | `code` (`tools.py` + `validator.tinh_tong_tien`) | 100% câu có giá/giờ/tổng tiền |
| `hanh_vi_dung` | `code` (so nhãn `hanh_vi` + kiểm câu `tu_choi`) | 100% câu `tu_choi`/thiếu thông tin/bất khả thi; ≥85% toàn bộ |
| `co_ly_do` | `llm` (có kiểm tay đối chiếu) | ≥80% câu `xep_lich` & `khong_xep_duoc` |

- **Hiệu chuẩn chấm chéo CP2:** phiếu cho Bùi Xuân Thành chấm độc lập 5 output vẫn để trống kết quả đối chiếu. Ngưỡng yêu cầu là khớp ít nhất 4/5.
- **LLM chấm (`co_ly_do`):** ở lượt 1 (`run-1.csv`), nhóm chưa bật LLM chấm tự động mà kiểm tay trực tiếp **25/25** câu (bắt được 2 lỗi lý do tại `B08` báo sai nguyên nhân và `B22` bịa lý do trời mưa ngày nắng); sẽ đối chiếu chéo thêm nếu bật LLM chấm ở lượt 2.
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
| 1 | `run-1@20261127-234913` | `cx/gpt-6-luna` | `agent.py` + `planner.py` + Data v2 (`53ccde1`), 0 lỗi kỹ thuật | 22/25 | 88,0% | Chưa *(vướng đk cứng #4 ở `B10`)* |
| 2 | Chờ Tuấn Anh chốt mã nguồn ở bước 11 | — | Kiểm lại cải tiến của Trường (`dfe671a`) về số trò và show tối thiểu. Ghi commit thực tế sau khi chốt. | — | — | Chưa chấm |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

- Lượt 1 có 3 lỗi: B08 báo sai nguyên nhân khi không xếp được, B10 bỏ bớt số trò/show bắt buộc rồi vẫn trả lịch, B22 viện dẫn mưa trong ngày trời quang. B10 khiến lượt 1 chưa đạt chuẩn §7 dù 22/25 câu qua.
- Lượt 2 dùng cùng 25 câu và cùng cách chấm. Kiểm xem B10 có báo không xếp được, giải thích giới hạn thời gian và gợi ý nới yêu cầu. Đối chiếu cả B08, B22 và các câu vừa chuyển từ đạt sang trượt. Xem [báo cáo đánh giá](report.md).
