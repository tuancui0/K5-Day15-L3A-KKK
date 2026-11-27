# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2 (Role [C] — Hoàng Đăng Kiên). Cập nhật bản đầu cho **CP2 (19:30 Thứ Sáu 27/11)**; bổ sung thêm nguồn/tập phụ (nếu cần) trước **CP3 (10:00 Thứ Bảy 28/11)**.
> Luật dữ liệu: không lưu tên người viết review · ẩn tên nhân viên trong trích dẫn bằng `[NV]` · trích ≤2 câu mỗi review · ghi rõ link nguồn và ngày xem.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** Review công khai của **VinWonders Phú Quốc** trên **Google Maps**
  - Link nguồn: https://www.google.com/maps/place/VinWonders+Ph%C3%BA+Qu%E1%BB%91c/@10.3407345,103.8514725,17z/data=!4m8!3m7!1s0x31081fff0f370283:0xd36b94f9a85d30cd!8m2!3d10.3407345!4d103.8540474!9m1!1b1!16s%2Fg%2F11r8503s0c
  - *Ghi chú tuyến nguồn:* TripAdvisor (`Attraction_Review-...-VinWonders_Phu_Quoc`) trả về chặn chống bot DataDome (HTTP 403), nhóm không vượt chặn mà dùng nguồn công khai mở là Google Maps.
  - Ngày giờ xem: **27/11/2026 (~16:41–16:42 GMT+7)**. Toàn trang lúc xem: **4,8★ / 19.763 bài đánh giá** (5★: 17.351 · 4★: 1.381 · 3★: 459 · 2★: 194 · 1★: 378 → nhóm 1–3★ chiếm 1.031/19.763 = 5,2%).
- **Đếm gì · trên tập nào · lọc gì:**
  - Sắp xếp theo **Mới nhất (Newest)**, lấy **mọi mức sao** (không lọc từ khoá, không lọc sao), lấy **60 bài đánh giá liên tiếp đầu tiên** (`10 phút trước` → `1 ngày trước`).
  - Đếm số bài thuộc từng nhãn vấn đề / phản hồi (đặc biệt nhóm có tín hiệu lập lịch, chờ đợi, giờ show, chi phí liên quan lát cắt C1).
- **Mẫu số là gì:** **$N = 60$** bài đánh giá liên tiếp (gồm cả 15 bài chỉ bấm sao không có chữ và mọi bài khen). Báo cáo thêm tỉ lệ trên tập có nội dung chữ **$N_{\text{chữ}} = 45$** để đối chiếu trực tiếp với giả thuyết ở `evidence/hypothesis.md`.
- **Script / công thức chạy lại:**
  - Bảng gắn nhãn đã ẩn danh: `evidence/reviews_labeled.csv`
  - Chạy lệnh: `python evidence/count_reviews.py` (chỉ dùng thư viện chuẩn Python, ra đúng bảng mục 3).

## 2. Đọc trước, đếm sau

Đã đọc **30 review đầu (`GM-01` → `GM-30`)** trước khi chốt bộ nhãn. Các *kiểu* nội dung thực sự thấy được:
- Nhiều bài chỉ bấm 5★ không viết chữ, hoặc viết 1 câu khen rất ngắn; đặc biệt có tỷ lệ cao bài khen đích danh nhân viên (trò chơi, nhà hàng, xe buggy).
- Các bài có nội dung chi tiết nhắc tới: công viên rất rộng cần xe điện (buggy) / tải bản đồ xếp lịch / phân bổ thời gian giữa các phân khu · trò chơi tốn nhiều thời gian ngay cả khi ít đông · lưu ý canh giờ show diễn Nàng tiên cá · nghẽn xe VinBus lúc đóng cửa · thẻ giá "Quá đắt".

**Định nghĩa 6 nhãn chính** *(mỗi review gắn đúng 1 nhãn theo thứ tự ưu tiên 1 → 6 để hai người chấm ra cùng kết quả)*:
1. `khong_noi_dung_chu`: Review chỉ chấm sao, không có văn bản (`[Không có nội dung chữ]`).
2. `cho_doi_dong_duc`: Nêu trực tiếp vấn đề chờ đợi/vận hành trò chơi mất nhiều thời gian hoặc đông đúc, chen chúc (vd lúc đóng cửa).
3. `lich_trinh_khuon_vien_rong`: Nêu công viên rất rộng cần xe điện (buggy), cần tải bản đồ để sắp xếp lịch trình, hoặc khuyên phân bổ thời gian giữa các phân khu.
4. `gio_show_chi_phi`: Nhắc lưu ý canh giờ show diễn để không bỏ lỡ và/hoặc gắn thẻ giá "Quá đắt".
5. `khen_nhan_vien`: Không thuộc 1–4, và có khen nhân viên / hướng dẫn viên / phục vụ.
6. `khen_chung`: Còn lại — khen ngắn gọn về công viên, trò chơi, gia đình, ẩm thực, không nêu vướng mắc lập lịch.

## 3. Kết quả

Chạy từ `python evidence/count_reviews.py` trên `evidence/reviews_labeled.csv` ($N = 60$, trong đó 5★: 57/60 = 95,0% · 4★: 3/60 = 5,0% · 1–3★: 0/60 = 0,0%):

| Đếm gì (`nhan_chinh`) | x / 60 | % (trên 60) | % (trên 45 có chữ) | Ghi chú (mã dòng) |
|---|---:|---:|---:|---|
| `lich_trinh_khuon_vien_rong` *(nhóm C1)* | 3 / 60 | 5,0% | 6,7% | `GM-05`, `GM-14`, `GM-34` |
| `cho_doi_dong_duc` *(nhóm C1)* | 2 / 60 | 3,3% | 4,4% | `GM-25`, `GM-27` |
| `gio_show_chi_phi` *(nhóm C1)* | 2 / 60 | 3,3% | 4,4% | `GM-26`, `GM-29` |
| **Tổng nhóm có tín hiệu lập lịch / vận hành / chi phí (C1)** | **7 / 60** | **11,7%** | **15,6%** | **`GM-05, GM-14, GM-25, GM-26, GM-27, GM-29, GM-34`** |
| `khen_nhan_vien` | 13 / 60 | 21,7% | 28,9% | Nếu tính cả `GM-05`: 14/60 (23,3%); 9/60 gọi đích danh tên NV |
| `khen_chung` | 25 / 60 | 41,7% | 55,6% | Khen ngắn gọn, không nêu vướng mắc |
| `khong_noi_dung_chu` | 15 / 60 | 25,0% | — | Chỉ chấm sao (5★) |
| **Tổng** | **60 / 60** | **100,0%** | **100,0%** | Khớp 100% với `evidence/reviews_labeled.csv` |

**Đối chiếu sơ bộ với `evidence/hypothesis.md`:** Tỉ lệ trên mẫu review mới nhất có nội dung chữ là **7/45 (15,6%)** — thấp hơn ngưỡng giả thuyết ban đầu (`≥20%`), một phần lớn do độ lệch mẫu 95% là 5★ khen nhân viên tại điểm (xem mục 5).

## 4. ≥5 ví dụ cụ thể (mã dòng đã ẩn danh, trích ≤2 câu, nguồn Google Maps xem 27/11/2026)

1. **`GM-34` (5★ · 23 giờ trước):** *"Công viên có quy mô cực kỳ rộng lớn, được chia thành nhiều phân khu theo chủ đề rõ ràng từ khu trò chơi cảm giác mạnh, công viên nước cho đến cung điện Hải Vương. Lưu ý nhỏ là khuôn viên rất rộng nên bạn nhớ mang giày thể thao êm chân, bôi kem chống nắng kỹ và tải sẵn bản đồ công viên để sắp xếp lịch trình hợp lý."*
2. **`GM-25` (4★ · 12 giờ trước):** *"Good theme park. Rides take a lot of time even though crowds are less."*
3. **`GM-29` (5★ · 22 giờ trước):** *"Chú ý đến giờ show diễn nàng tiên cá. Xem rất hay, không nên bỏ lỡ."*
4. **`GM-26` (4★ · 16 giờ trước):** *"Mermaid show is must watch."* *(kèm thẻ Google Maps: "Quá đắt", chờ 10–30 phút).*
5. **`GM-05` (5★ · 44 phút trước):** *"Had a great experience at vinwonders especially when taken buggy with my friend [NV] who drove me to to different location in the park which is very big so it was useful to take buggy add on."*
6. **`GM-27` (5★ · 17 giờ trước):** *"Travel to/from on Vinbus is free if you pre-book your tickets and have a QR code but ... Be prepared to fight for space on the bus if you're leaving when it closes!! People can be SO rude!!!"*
7. **`GM-14` (5★ · 3 giờ trước):** *"Had a great experience; do spend more time in adventure and aqua park."*

## 5. Giới hạn của data

- **Lệch mẫu mạnh về phía 5★ trên luồng "Mới nhất":** 57/60 (95,0%) bài mới nhất là 5★ và 14/60 (23,3%) nhắc khen nhân viên (trong đó 9/60 gọi đích danh tên), cho thấy nhân viên tại công viên có khả năng khuyến khích khách đánh giá 5★ tại chỗ. Do đó tập 60 bài mới nhất không bắt được bài 1–3★ nào dù toàn trang có 1.031 bài 1–3★ (5,2%), khiến các ca nặng (mưa huỷ show, trẻ dưới chiều cao, đóng cửa bảo trì) chưa lộ rõ.
- **Mới phủ 1 khu vui chơi (VinWonders Phú Quốc)** và 6 bài (`GM-09, GM-32, GM-44, GM-46, GM-50, GM-53`) là bản dịch tự động của giao diện Google Maps.
- **Data chỉ cho biết khách nói gì, chưa cho biết mất bao nhiêu phút để tự xếp lịch hay vì sao họ gặp khó.**
- → **Kiểm lại bằng:** (1) **≥4 cuộc phỏng vấn trực tiếp** với phụ huynh / khách đi khu vui chơi (`evidence/interviews/P1.md`…P4.md) để kiểm chứng *vì sao* và đo thời gian tốn; (2) trước **CP3**, bổ sung thêm 1 tập phụ (lọc riêng 1–3★ có ghi rõ cách lọc) hoặc thêm 1–2 khu vui chơi khác (VinWonders Nha Trang / Sun World Ba Na Hills) để kiểm chéo các ca vỡ lịch nặng.
