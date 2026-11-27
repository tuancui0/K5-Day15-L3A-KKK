# Phân công nhóm — Track C · C1 Lịch trình một ngày ở khu vui chơi

> Nhóm 4 người, **ai cũng code, ai cũng có AI agent**. Đội trưởng = **[L]**. Thay `[L] [A] [B] [C]` bằng tên thật, chép vào `TEAMS.md` (cột "Phần việc chính") và `canvas.md` dòng 7.
> Cách chạy nhanh: **mỗi người sở hữu 1 module code + 1 mảng tài liệu**, chỉ sửa file của mình → 4 agent chạy song song không xung đột git. Mọi module nói chuyện qua **hợp đồng interface ở mục 2**, chốt trong 30 phút đầu.
> Luật khoá: mỗi người phải **giải thích được code có tên mình** (agent viết hộ vẫn phải hiểu) — không giải thích được thì phần đó 0 điểm.

---

## 1. Bốn người · bốn module

| Người | Module code (sở hữu) | Tài liệu (sở hữu) | Việc chung ai cũng làm |
|---|---|---|---|
| **[L] Đội trưởng** — Orchestrator | `codebase/agent.py`: luồng chính `answer()`, cổng **hỏi lại / từ chối** trước khi xếp, vòng tự kiểm (MAX_VONG=3), định dạng output lịch từng giờ · `scripts/review_count.py` (đếm nhãn review → x/N, %) | `TEAMS.md` · `canvas.md` · `spec.md` §0–3, §8–10 · `evidence/summary.md` · `demo-slides.pdf` · **nộp 4 CP** | ≥1 phỏng vấn · 1 file `reflection/` · nói ≥1 phần khi demo · chạy được `run.py eval` và `run.py simulate` |
| **[A]** — LLM | `codebase/ai.py` (nối model thật, structured output JSON, retry) · `codebase/planner.py`: 3 prompt `trich_rang_buoc()`, `xep_lich()`, `sua_lich()` | `spec.md` §4 (sơ đồ) · `docs/ai-usage.md` · `docs/connect-model.md` ghi model đã dùng | như trên |
| **[B]** — Data & Tools | `data/gen_data.py` (sinh dữ liệu công viên giả **có seed**) · `codebase/tools.py` (công cụ chỉ đọc) · `codebase/validator.py`: `kiem_lich_trinh()` + `tinh_tong_tien()` **bằng code** · sau CP3: `cost/` | `data/DATA_CARD.md` · `cost/personas.yaml` · `cost/cost-estimate.md` | như trên |
| **[C]** — Eval | `eval/benchmark.csv` · `eval/metric_spec.yaml` · `eval/auto_grade.py`: chấm tự động (gọi lại `validator.py`, so số với công cụ, kiểm loại hành vi) + LLM chấm cho metric mềm | `spec.md` §5–7 · `evidence/data-mining.md` · `eval/report.md` · `eval/README.md` · `validation/log.md` | như trên |

**Vì sao chia thế này:** 4 module độc lập theo interface → không ai chờ ai. [B] và [C] cùng dựa vào `validator.py` nên "tốt" được đo bằng chính code kiểm ràng buộc — đúng điều kiện cứng của track C ("0 vi phạm, kiểm bằng code").
**Review chéo cố định (mỗi PR/commit lớn):** [L]↔[A] (luồng ↔ prompt) · [B]↔[C] (validator ↔ chấm điểm).

---

## 2. Hợp đồng interface — chốt trong 30 phút đầu (cả nhóm)

**Lát cắt (nháp):** *Một gia đình 2 người lớn + 1–2 trẻ nhỏ · nhập ngân sách, sở thích, khung giờ ở khu vui chơi · AI chọn điểm và thứ tự thoả mọi ràng buộc, hoặc nói không xếp được và nên nới ràng buộc nào · gia đình nhận lịch từng giờ kèm tổng tiền và lý do chọn.*

**Hình dạng: workflow cố định có vòng tự kiểm giới hạn** (không phải agent tự do — các bước luôn giống nhau, kiểm bằng code rẻ và đo được).

```
text ─► [A] trich_rang_buoc()  ─► thiếu số người/khung giờ/ngân sách? ─► [L] HỎI LẠI 1 câu
                                  yêu cầu ngoài phạm vi / tấn công?     ─► [L] TỪ CHỐI + chỉ đường
     ─► [B] tools: tra_diem_choi · tra_lich_show · tra_thoi_tiet · uoc_thoi_gian_di
     ─► [A] xep_lich()  ─► [B] kiem_lich_trinh() ─► vi phạm & vòng<3 ─► [A] sua_lich() ─┐
                                   ▲─────────────────────────────────────────────────────┘
     ─► sạch: [B] tinh_tong_tien() ─► [L] in lịch từng giờ + tổng tiền + lý do
     ─► hết 3 vòng vẫn vi phạm: [L] "không xếp được" + gợi ý nới ràng buộc nào
```

**Chặn rủi ro:** giá, giờ, tổng tiền **chỉ do code tính** — model không nhẩm · điểm/show không có trong dữ liệu → "không có" · không đặt vé, không thu tiền, không xin thông tin thẻ · tin tự xưng "nhân viên công viên" = dữ liệu, không phải lệnh.

```python
# ---- Dữ liệu ([B] sinh, seed=42, khu dựng tên "Công viên Mẫu") ----
# data/park.json
{"diem": [{"id": "D01", "ten": "...", "khu": "...", "mo": "09:00", "dong": "17:00",
           "thoi_luong_phut": 20, "cho_doi_phut": 15, "gia": {"nguoi_lon": 0, "tre_em": 0},
           "chieu_cao_min_cm": 0, "trong_nha": True, "the_loai": ["cam_giac_manh"]}],
 "show": [{"id": "S01", "ten": "...", "diem_id": "D05", "gio": ["10:30", "15:00"],
           "thoi_luong_phut": 30, "huy_khi_mua": True}],
 "ve_vao_cong": {"nguoi_lon": 0, "tre_em": 0, "tre_duoi_1m": 0}}
# data/weather.json: {"2026-12-05": {"mua_tu": "13:00", "mua_den": "15:00"}}
# data/travel.csv:   a,b,phut

# ---- Ràng buộc ([A] trich_rang_buoc trả về) ----
RangBuoc = {"ngay": "2026-12-05", "gio_bat_dau": "09:00", "gio_ket_thuc": "17:00",
            "nguoi_lon": 2, "tre_em": [{"tuoi": 5, "chieu_cao_cm": 105}],
            "ngan_sach": 2_000_000, "so_thich": ["nuoc", "show"],
            "thieu": [],            # trường thiếu → [L] hỏi lại
            "ngoai_pham_vi": None}  # lý do nếu phải từ chối

# ---- Lịch ([A] xep_lich / sua_lich trả về) ----
Lich = [{"diem_id": "D01", "bat_dau": "09:15", "ket_thuc": "09:50", "ly_do": "..."},
        {"show_id": "S01", "bat_dau": "10:30", "ket_thuc": "11:00", "ly_do": "..."}]

# ---- Kiểm ([B] validator.py — [C] dùng lại để chấm) ----
kiem_lich_trinh(lich, rang_buoc) -> [{"loai": "truoc_gio_mo|sau_gio_dong|chong_gio|khong_kip_di|"
    "vuot_ngan_sach|tre_khong_du_chieu_cao|ngoai_troi_khi_mua|show_sai_gio|diem_khong_ton_tai",
    "chi_tiet": "..."}]
tinh_tong_tien(lich, rang_buoc) -> {"ve_vao_cong": int, "diem": int, "tong": int}

# ---- Output answer() ([L]) — [C] chấm trên đây ----
{"output": "<văn bản cho khách>",
 "hanh_vi": "xep_lich|hoi_lai|khong_xep_duoc|tu_choi",
 "lich": Lich | None, "tong_tien": int | None, "vi_pham_con_lai": [...]}
```

> Trước khi có code thật, ai cũng **stub** phần của người khác theo hợp đồng này (trả giá trị cố định) để chạy được module mình.

---

## 3. Lịch theo chặng

### Chặng 1 · → **CP1 17:00 Thứ Sáu 27/11**

| Ai | Code | Tài liệu / bằng chứng |
|---|---|---|
| **[L]** | Tạo repo `K5-Day15-<lớp>-<TênNhóm>` công khai từ `starter-repo/`, mời 3 bạn · commit `PHAN-CONG.md` + hợp đồng mục 2 | `TEAMS.md` (mình dòng 1) · `canvas.md` 7 dòng · bài toán 1–2 câu không chữ AI · `evidence/hypothesis.md` · `python run.py check` sạch |
| **[A]** | Lấy API key, `python run.py` gọi thử được 1 câu (token > 0) | — |
| **[B]** | `gen_data.py` bản nhỏ (~15 điểm, 4 show, 1 ngày mưa) | — |
| **[C]** | Khung `auto_grade.py` đọc `run-*.csv` | Chọn nguồn review + **ghi cách chọn mẫu trước khi đọc** (vd 60–100 review Google Maps/Tripadvisor mới nhất của 2–3 khu vui chơi, mọi mức sao) · đọc 30 cái → đặt nhãn có định nghĩa |
| **Mỗi người** | — | Hẹn ≥1 người đã đi khu vui chơi gần đây (ưu tiên có con nhỏ) theo `evidence/interviews/TEMPLATE.md` |

**16:45 cả nhóm đọc lại canvas → [L] nộp CP1.**

### Chặng 2 · → **CP2 19:30 Thứ Sáu 27/11** (chuẩn "đạt" chốt tại đây, không sửa về sau)

| Ai | Việc |
|---|---|
| **Cả nhóm 17:00–17:40** | Mỗi người 1 phỏng vấn 10–15' → 20' tổng hợp → chốt lát cắt + sơ đồ |
| **[L]** | `agent.py` khung đủ luồng với AI **giả** (stub planner) → `python run.py` đi hết · `spec.md` §1–3 · bảng impact nháp §2 · canvas + "đã đổi gì so với CP1" |
| **[A]** | `planner.py` 3 prompt chạy được với model thật (thử tay 10–20 input, ghi lỗi thấy được gửi [C]) · sơ đồ vào `spec.md` §4, ghi phần nào đang giả |
| **[B]** | `tools.py` 4 công cụ + `validator.py` đủ 9 loại vi phạm + unit test nhỏ · `DATA_CARD.md` bản đầu (synthetic, seed, cách sinh) |
| **[C]** | `metric_spec.yaml` ≥3 metric · `benchmark.csv` ≥10 câu phủ 4 lớp chỗ khó · `spec.md` §5 (≥6 kịch bản + 2 tấn công), §7 chuẩn "đạt" |
| **19:00** | Review chéo [L]↔[A], [B]↔[C] · [B] và [C] chấm độc lập cùng 5 output → lệch ≥2/5 thì viết lại metric |

**Metric gợi ý:** `rang_buoc_cung` (0 vi phạm theo `validator.py`, code) · `so_khop_cong_cu` (mọi giá/giờ/tổng khớp công cụ, code) · `hanh_vi_dung` (đúng `hanh_vi` mong đợi, code) · `co_ly_do` (lý do gắn sở thích/ràng buộc, LLM chấm).
**Chuẩn "đạt" gợi ý:** *≥ 70% câu qua, và 0 câu vi phạm ràng buộc cứng · 100% số khớp công cụ · 100% câu `tu_choi` qua · 0 câu xếp bừa khi không khả thi.* → cả nhóm chốt, **commit trước 19:30**.

**19:15 tự soát guide 2.5 → [L] nộp CP2.**

### Chặng 3 · tối Thứ Sáu → **CP3 10:00 Thứ Bảy 28/11**

| Ai | Tối Thứ Sáu (xong trước khi ngủ) | Sáng Thứ Bảy |
|---|---|---|
| **[L]** | Ghép module thật vào `agent.py`, bỏ stub · vòng tự kiểm + `note("dừng: …")` · ghi chép phỏng vấn P1…P4 (không tên) | `evidence/summary.md` (số chính + ≥5 trích dẫn + kết luận giả thuyết) · `spec.md` §0–7 đủ |
| **[A]** | Prompt cứng hoá: structured output, chống prompt injection, "không có trong dữ liệu" | Quay **video 30s** (1 ca thường + 1 ca khó) |
| **[B]** | Dữ liệu đủ "bẩn": điểm đóng sớm, show huỷ khi mưa, trẻ dưới 1m, ngân sách sát, ngày không khả thi · `run.py simulate --try` 10 phiên | DATA_CARD bản đủ |
| **[C]** | `benchmark.csv` **20–30 câu** (≥5 `kho`, ≥2 `tu_choi`, ≥1/3 từ `nguoi_dung:`/`data_that:`) · đếm review xong → `data-mining.md` (x/N, %) | `auto_grade.py` chấm `run-1.csv` |

**08:30–09:30 cả nhóm online:** `python run.py eval` → `eval/run-1.csv` → chấm → `run.py score`. **09:45 [L] nộp CP3** (video, x/N, run ID).

### Chặng 4 · 10:00 → 13:00 Thứ Bảy — đo & tính tiền

| Ai | Việc |
|---|---|
| **Cả nhóm 10:00–10:30** | Đọc chung câu trượt → gom nhóm lỗi có tên → chọn **1** nhóm lỗi đau nhất |
| **[A] + [L]** | Cải tiến (prompt / luồng) nhắm nhóm lỗi đó → `run.py eval` **trọn bộ** → `run-2.csv` |
| **[C]** | Chấm lượt 2 · `eval/report.md` (≥3 lỗi: input · output · vì sao) · `eval/README.md` (hồ sơ 1 trang) |
| **[B]** | `personas.yaml` (≥3 persona từ phỏng vấn: xếp 1 lần / sửa nhiều lần / ngày mưa xếp lại) · số khách thật có nguồn công khai · `run.py simulate` ≥50 phiên · `cost-estimate.md`: chi phí/task thành công (÷ tỉ lệ đạt lượt 2), 3 kịch bản × 2 model, so với impact |
| **Mỗi người (bonus +5)** | 1 người ngoài nhóm đúng vai thử 10' → `validation/log.md` ([C] gom) |

### Chặng 5 · 13:00 → **CP4 14:30**

| Ai | Việc |
|---|---|
| **[L]** | Ghép slide 8 trang (guide 5.1) → `demo-slides.pdf` ở thư mục gốc · nộp CP4 |
| **[A]** | Trang "Giải pháp" + video demo dự phòng · máy chạy live sẵn 1 câu thử lạ |
| **[B]** | Trang "Chi phí khi dùng thật" |
| **[C]** | Trang "Đánh giá thế nào" |
| **13:45 cả nhóm** | Tập demo 2': [L] Pain+Impact → [A] Giải pháp + demo → [C] Đánh giá → [B] Chi phí → [L] Go/iterate/stop |

**Sau demo → 23:59:** sửa theo góp ý, ghi `spec.md` §10 ([L]) · chạy thêm thì là `run-3.csv` · mỗi người 1 file `reflection/<ten>.md`.

---

## 4. Luật làm việc với AI agent

1. **Mỗi người dặn agent của mình:** đọc `AGENTS.md`, `PHAN-CONG.md` mục 2 (hợp đồng) trước; **chỉ sửa file mình sở hữu**; không đổi chữ ký hàm trong hợp đồng — muốn đổi thì báo nhóm, [L] duyệt rồi cập nhật mục 2.
2. **Branch theo người** (`l/agent`, `a/planner`, `b/tools`, `c/eval`) → merge vào `main` qua review chéo. Commit nhỏ, thường xuyên.
3. **Agent không được nhẩm tiền/giờ trong prompt** — mọi con số đi qua `validator.py` / `tools.py`.
4. **Không commit `.env`**, không dữ liệu người thật (không tên người phỏng vấn, không tên người viết review; trích ≤2 câu/review kèm link + ngày xem).
5. **Không sửa sau CP2:** chuẩn "đạt", `expected` của câu thử, số bằng chứng, kết quả lượt đã chạy. Chỉ được *thêm* câu thử.
6. **Kẹt quá 20 phút** → báo nhóm / lab coach ngay.
7. **15 phút trước mỗi checkpoint:** cả nhóm đi lại câu chuyện Pain → Impact → Giải pháp → Đánh giá → Chi phí.
8. Mỗi người ghi 2–3 dòng "dùng AI vào việc gì" vào `docs/ai-usage.md` dưới tên mình.

## 5. Bảng theo dõi (đội trưởng tích)

| Mốc | Hạng mục | Chủ | ✓ |
|---|---|---|---|
| CP1 | TEAMS · canvas · bài toán · lát cắt · repo công khai | L | ☐ |
| CP2 | sơ đồ §4 · benchmark ≥10 · metric_spec · DATA_CARD · chuẩn "đạt" · `run.py` AI giả | A, C, B, L | ☐ |
| CP3 | evidence đủ ngưỡng + ≥5 trích dẫn · benchmark 20–30 · video 30s · run-1 + run ID · spec §0–7 | L, C, A | ☐ |
| CP4 | run-2 + report + eval/README · cost 3 kịch bản · spec §0–9 · demo-slides.pdf · video dự phòng | tất cả | ☐ |
| 23:59 | spec §10 · 4 file reflection | tất cả | ☐ |
