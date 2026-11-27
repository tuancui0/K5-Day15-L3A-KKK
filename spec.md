# AI SPEC — Lịch trình một ngày ở khu vui chơi cho gia đình có trẻ nhỏ · Nhóm KKK · Phòng ____ · Zone ____

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [ ] A · [ ] B · [x] C · [ ] D · [ ] E — bài toán: C1 · Lịch trình một ngày ở khu vui chơi (đề gợi ý trong `tracks/track-c-travel.md`), thu hẹp về gia đình có trẻ nhỏ
Data BTC cấp đã dùng (nếu có — không commit nguyên file): không dùng (track C không có data BTC). Bằng chứng: review công khai + phỏng vấn. Dữ liệu chạy thử: tự dựng có seed (`data/DATA_CARD.md`).

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại (theo trải nghiệm của nhóm; bước 1–2 đã đối chiếu với web chính thức VinWonders và Sun World ngày 27/11/2026, ảnh trong `evidence/screenshots/`; bước 3–5 **chưa kiểm**, kiểm bằng phỏng vấn):
  1. Tối hôm trước hoặc tại cổng: mua vé trên web. Ô tìm vé chỉ hỏi điểm đến, ngày (Sun World thêm số người) — không hỏi tuổi / chiều cao trẻ hay sở thích (`vinwonders-home.png`, `sunworld-home.png`).
  2. Xem giờ show trên trang của từng công viên: VinWonders Phú Quốc liệt kê 4 show kèm giờ và khu (vd Sắc Màu Đại Dương 14:00–14:20 & 15:30–15:50 ở Cung Điện Hải Vương, Diễu hành Carnival 17:00–17:30, Once Show 18:45–19:05 ở Đại Lộ Châu Âu) (`vinwonders-phuquoc.png`). Giá vé và quy định chiều cao lại nằm ở trang "Nội quy & giá vé" riêng: giá chia theo chiều cao (<100 cm miễn phí, 100–<140 cm vé trẻ em, ≥140 cm vé người lớn), trẻ dưới 140 cm phải có người lớn đi kèm (`vinwonders-phuquoc-noiquy-giave.png`). Trang "Show diễn - Sự kiện" của Sun World là danh sách bài tin tức, không phải bảng giờ show (`sunworld-show.png`). Khách tự ghép giờ show, giá và chiều cao từ các trang này.
  3. Đến từng trò mới biết giới hạn chiều cao, thời gian chờ, trò có thu phí riêng không.
  4. Trong ngày tự quyết đi đâu tiếp theo dựa vào bản đồ; mưa hoặc show huỷ thì tự xếp lại.
  5. Cuối ngày mới biết tổng chi (vé cổng + trò thu phí riêng + ăn uống).
- Công cụ / AI đang được dùng: web chính thức của khu vui chơi (giờ show, giá vé, nội quy) — trên các trang web đã xem của VinWonders và Sun World **không thấy** tính năng gợi ý / xếp lịch trình (chưa kiểm app di động) · chatbot chung (ChatGPT, Gemini) để hỏi "nên chơi gì" — **chưa kiểm**, không có dữ liệu giờ mở cửa / giá của ngày đi.

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): bố hoặc mẹ đưa 1–2 con nhỏ (3–10 tuổi) đi khu vui chơi lớn một ngày, là người tự lên kế hoạch và cầm ngân sách.
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI): **xếp thứ tự trò chơi và show cho cả nhà trong một ngày ở khu vui chơi, vừa ngân sách và hợp với con nhỏ.**
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: tự xem bản đồ + lịch show + bảng giá rời nhau, đi tới đâu tính tới đó; hỏi người quen đã đi; hỏi chatbot chung. Hỏng ở chỗ các ràng buộc (giờ mở, giờ show, chiều cao trẻ, đi bộ, chờ hàng, mưa) không nằm cùng một chỗ nên dễ chồng giờ, lỡ show; chatbot chung không có dữ liệu ngày đi nên có thể nói sai giờ / giá. Chưa bỏ vì không có cách nào khác gom đủ thông tin, và mỗi gia đình chỉ đi vài lần một năm nên chấp nhận "đi rồi tính" *(giả thuyết — kiểm bằng phỏng vấn)*.
- Pain (KHÔNG chữ AI): phụ huynh đi khu vui chơi với con nhỏ đang tự xếp thứ tự các trò và giờ show từ bản đồ, bảng giờ và bảng giá riêng lẻ, vướng ở chỗ giờ show, giờ mở cửa, giới hạn chiều cao của trẻ, thời gian đi bộ và mưa giữa ngày chồng chéo nhau → lỡ show con muốn xem, đến trò trẻ không được chơi, đi vòng vèo, chơi không hết mà tốn tiền hơn dự kiến.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): **đang thu (CP2).** Giả thuyết và ngưỡng đúng/sai đã viết trước ở `evidence/hypothesis.md`. Nguồn chính: đào 60–100 review Google Maps / Tripadvisor của 2–3 khu vui chơi (`evidence/data-mining.md`, Kiên). Nguồn kiểm lại: phỏng vấn ≥4 phụ huynh / người đã đi gần đây (`evidence/interviews/P1.md`…, mỗi thành viên 1 người). Số chính + ≥5 trích dẫn: điền trước CP3.

## §2. Impact & quyết định chọn *(guide 1.3)*

> **Bản nháp CP2** — mọi số đang là *(tự ước tính)*, thay bằng số từ review / phỏng vấn / nguồn công khai trước CP3. Không có nguồn thì giữ nhãn *(tự ước tính)*.

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| **H1 · Xếp lịch một ngày cho gia đình có trẻ nhỏ** (trước ngày đi / tại cổng) | gia đình có trẻ nhỏ trong số khách khu vui chơi — __ *(cần nguồn: lượt khách/năm công khai × tỉ lệ khách đi cùng trẻ, tự ước tính)* | ~1 chuyến / gia đình, mỗi chuyến xếp 1 lần + sửa 1–3 lần *(tự ước tính, kiểm bằng phỏng vấn)* | ~30–60 phút tự lên kế hoạch + lỡ ≥1 trò / show định chơi + tiền vé trò không dùng được *(tự ước tính, kiểm bằng phỏng vấn + review)* | __ gia đình × 1 × ~45 phút | **Kịp**: dữ liệu tự dựng được, kiểm ràng buộc bằng code, đo được bằng câu thử | **✓ Chọn** |
| H2 · Xếp lại phần còn lại của ngày khi mưa / show huỷ | chỉ các gia đình gặp mưa / huỷ show — ít hơn H1 *(tự ước tính)* | phụ thuộc mùa mưa *(tự ước tính)* | mất phần còn lại của ngày | nhỏ hơn H1 | Kịp, nhưng cần H1 chạy trước | Gộp vào H1 như **câu thử khó** (mưa giữa ngày), không làm riêng |
| H3 · Dự đoán thời gian chờ hàng, gợi ý giờ vắng | mọi khách *(tự ước tính)* | mỗi lần đi | 15–60 phút chờ mỗi trò *(tự ước tính)* | có thể lớn | **Không kịp**: cần dữ liệu thời gian chờ thật, nhóm không có và không được nối hệ thống thật | ✗ Loại |

- **Impact / tháng** của hướng chọn = __ gia đình / tháng × 1 lần × ~45 phút = __ giờ / tháng + __ trò / show bị lỡ — nguồn từng thừa số: số gia đình: __ *(nguồn công khai, Thành tìm ở chặng 4)* · 45 phút và số trò bị lỡ: *(tự ước tính — thay bằng số từ phỏng vấn P1–P4)*
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá): **H3** loại vì cần dữ liệu thời gian chờ thật và nối vào hệ thống của khu vui chơi (trái ràng buộc chung số 2). **H2** không làm riêng, giữ làm tình huống khó trong bộ câu thử của H1.
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8) *(tự ước tính, thay bằng số phỏng vấn)*: **xep_mot_lan** — xếp 1 lần rồi đi · **sua_nhieu_lan** — xếp rồi sửa 2–4 lần trước ngày đi (đổi giờ, bớt trò, đổi ngân sách) · **ngay_mua** — xếp lại giữa ngày vì mưa / show huỷ, mỗi lần xếp thêm các vòng tự kiểm.

## §3. Giải pháp tương tự *(guide 2.1)*
- **Web chính thức của khu vui chơi** (VinWonders, Sun World — đã xem web ngày 27/11/2026, ảnh trong `evidence/screenshots/`; chưa kiểm app di động): đáng học · dữ liệu chính thức, là nguồn sự thật; VinWonders ghi giờ show và khu ngay trên trang công viên · đáng né · giờ show, giá vé và quy định chiều cao nằm ở các trang khác nhau, ô tìm vé không hỏi tuổi / chiều cao trẻ, không có tính năng xếp lịch — khách tự ghép · mình khác · gom các ràng buộc lại và xếp sẵn thành lịch từng giờ.
- **Disney Genie** trong app My Disney Experience (công viên Disney ở Mỹ, gợi ý lịch trình theo sở thích) — *theo trang chính thức của Disney, chưa kiểm lại trong hackathon (web Disney chặn trình duyệt tự động, chưa chụp được — cần một người mở tay và chụp)*: đáng học · hỏi sở thích rồi gợi ý thứ tự, cập nhật trong ngày · đáng né · gắn với dịch vụ trả phí và dữ liệu chờ hàng thật mà nhóm không có · mình khác · làm cho một gia đình có trẻ nhỏ, chú trọng chiều cao / tuổi và ngân sách, nói rõ khi không xếp được.
- **Chatbot chung (ChatGPT, Gemini)** hỏi "đi khu vui chơi X nên chơi gì": đáng học · nhập bằng câu tự nhiên, không cần form · đáng né · tự nhẩm giờ / giá, có thể nói sai giờ mở cửa, không kiểm chồng giờ · mình khác · giờ, giá, tổng tiền chỉ lấy từ dữ liệu và được **kiểm bằng code** trước khi đưa cho khách.

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả):
- Không làm (≥3 điều):
- **Sơ đồ** (ảnh / Mermaid / draw.io): [chèn ở đây]
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [ ] nhiều agent — 2 dòng lý do, và vì sao **không** chọn hình dạng phức tạp hơn:
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  |  |  |  |  |

- **Mức tự động:** [ ] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do (sai thì ai chịu gì, sửa đắt hay rẻ):
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì):
- **Chỗ người duyệt** (việc AI không được tự làm):
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc |  |
  |  |  |
  |  |  |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): **Đỗ Tuấn Anh** (đội trưởng) — `codebase/agent.py`, §0–3, bằng chứng pain, slide, nộp checkpoint · **Phan Nhật Trường** — `codebase/ai.py`, `codebase/planner.py`, §4 · **Bùi Xuân Thành** — `data/`, `codebase/tools.py`, `codebase/validator.py`, `cost/` · **Hoàng Đăng Kiên** — `eval/`, §5–7, `evidence/data-mining.md`. Review chéo: Tuấn Anh ↔ Trường, Thành ↔ Kiên. Chi tiết theo chặng: `PHAN-CONG.md`.
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
