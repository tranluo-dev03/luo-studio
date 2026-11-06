# Hướng dẫn sử dụng LUO Studio

LUO Studio tạo hàng loạt video quảng cáo bằng AI (Muse): bạn chọn **thể loại video**, điền **biến thể** (nhân vật + lời thoại), phần mềm tự gen từng cảnh, nối, cắt, rồi làm **hậu kỳ** ra video hoàn chỉnh.

---

## 1. Cài đặt (làm 1 lần)
1. Giải nén vào thư mục **ngắn, không dấu**, ví dụ `D:\LUO-Studio` (không để trong OneDrive).
2. Mở PowerShell trong thư mục đó, chạy:
   ```
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```
   Có hộp thoại xin quyền thì bấm **Yes**. Script báo cần khởi động lại máy thì khởi động lại.
3. Bấm đúp **`LUO Studio.bat`** để mở.

## 2. Thêm tài khoản Muse (làm 1 lần)
1. Đăng nhập **muse.ai** trên Chrome/Edge → nhấn **F12** → tab **Network** → **F5**.
2. Bấm một dòng bất kỳ → tìm **Cookie** trong Request Headers → copy toàn bộ.
3. Trong LUO Studio: tab **API Muse** → **Thêm tài khoản** → dán cookie → **Lưu** → **Kiểm tra phiên** (báo "Phiên ổn" là xong).

> Góc trên bên phải hiện **"API sẵn sàng"** (chấm xanh) là dùng được.

## 3. Cập nhật bản mới
Đóng LUO Studio → bấm đúp **`Cap nhat.bat`** → mở lại. Dữ liệu của bạn không mất.

---

## 4. Làm video

### Bước 1: Chọn thể loại
Mỗi thể loại là một thư mục trong `SAMPLE\` (kịch bản + biến thể mẫu + hướng dẫn riêng):

| Thư mục | Thể loại |
|---|---|
| `talka-bang-tu-vung` | Robot dạy từ vựng trước tờ giấy, bút chỉ chữ, cuối quảng cáo app |
| `ai-tutor-ngoi-doc` | Robot ngồi đọc cặp câu, bảng phía trên hiện câu + phiên âm (đổi được robot, nền, cờ, từ, ngôn ngữ) |
| `xe-tai` | Tài xế xe tải nói chuyện với gia sư AI |
| `canh-sat-nu` | Cảnh sát nữ và tài xế |
| `ghep-hai-lop` | Hai nhân vật ở hai khung riêng (không bao giờ nói chồng) |
| `lam-vuon` | Người học làm vườn + gia sư AI trên điện thoại (dùng loại có sẵn **"Điện thoại + người học"**, bỏ qua Bước 2) |

### Bước 2: Nhập kịch bản (mỗi thể loại 1 lần)
Tab **Loại dự án** → **Loại mới** → chọn file `KICH-BAN-*.txt` trong thư mục thể loại → **Tạo** (đặt tên loại tuỳ ý).

### Bước 3: Tạo dự án
**Dự án mới** → chọn loại vừa nhập → chọn file biến thể `BIEN-THE-*.json` trong thư mục thể loại.
Mỗi biến thể = một video.

### Bước 4: Gen
1. Tick các biến thể → **Thêm vào hàng đợi**.
2. Tab **Hàng đợi** → chọn **Song song** (tối đa **số tài khoản Muse × 2**: từ bản 1.2.0 mỗi tài khoản chạy được 2 video cùng lúc) → **Bắt đầu**.
3. Bấm vào thẻ video để xem từng cảnh. Cảnh nào sai → bấm **gen lại cảnh** (mũi tên vòng), có thể ghi yêu cầu sửa.
   Cảnh chạy lâu → bấm **Các bước** trên cảnh đó để xem bảng từng bước và thời gian (Muse vẽ, chờ tài khoản, xử lý trên máy…), bước lâu nhất tô vàng.
4. Muốn gen video bằng tài khoản khác: bấm dòng tài khoản trên thẻ video (hoặc nút tài khoản ở đầu trang video) → chọn tài khoản, hoặc **Tự động**.
   Video đang chạy sẽ chạy tiếp ngay bằng tài khoản mới, giữ các cảnh đã xong.

> Tài khoản lỗi (cookie hỏng, hết hạn mức) thì video **tự đổi sang tài khoản khác** đang bật. Lỗi khác thì video tự xếp lại hàng chờ và chạy lại sau vài phút, các video khác vẫn chạy tiếp, nên để chạy qua đêm được.

> **Chạy thử 1 biến thể trước**, ưng rồi mới chạy cả nhóm (tiết kiệm lượt Muse).

### Bước 5: Hậu kỳ và lấy video
Hậu kỳ **tự chạy** ngay khi gen xong và ghép xong clip (không cần bấm). Xong thì xem ở tab **Kết quả**; nếu hậu kỳ lỗi thì bấm **Hậu kỳ lại**. Video hoàn chỉnh nằm ở `userdata\studio\exports\<dự án>\` (nút **Mở thư mục**).

**Logo & Outro của dự án:** trong trang dự án, thẻ **Logo & Outro của dự án** cho chọn 4 file: logo bay (.mov/.webm nền trong suốt, lặp đến hết video), logo cố định (.png, kèm chữ tên app, chọn góc và cỡ), video giới thiệu app (.mp4) và video outro (.mp4). Bật công tắc thì mọi video của dự án sau hậu kỳ được gắn logo rồi nối **video gen + video giới thiệu + outro**. Video giới thiệu và outro nối nguyên bản, không phủ logo. Dự án bật mục này thì không dùng logo / end card mặc định ở Cài đặt.

---

## 5. Tạo biến thể mới bằng AI

**Có video mẫu mới?** Mở Claude Code trong thư mục LUO Studio, đưa file video và nói "làm video này": Claude tự phân tích, chọn thể loại, viết kịch bản + biến thể, kiểm tra và nhập thẳng vào Studio rồi chạy thử một biến thể (quy trình: `SAMPLE\_chung\SO-TAY-KY-THUAT.md`, công cụ `SAMPLE\_chung\video-moi.py`). Studio phải đang mở.

**Chỉ cần thêm biến thể cho thể loại đã có:**
1. Mở **Claude** hoặc **ChatGPT**, đính kèm file **biến thể mẫu** của thể loại (`BIEN-THE-*.json`).
2. Dán prompt của thể loại đó, sửa phần trong `[ ]`:
   - thể loại Talka: prompt trong `SAMPLE\talka-bang-tu-vung\HUONG-DAN-NHANH.md`;
   - các thể loại khác: `PROMPT-CHO-AGENT.txt` trong thư mục thể loại.
3. Lưu kết quả thành file `.json` → **Dự án mới** chọn file này (hoặc trong dự án bấm nút **mũi tên lên** dưới danh sách biến thể) → chạy thử 1 biến thể.

---

## 6. Lỗi thường gặp

| Lỗi | Cách xử lý |
|---|---|
| Chấm đỏ "API chưa kết nối" | Đóng hẳn LUO Studio, mở lại. Vẫn lỗi: chạy `Chan doan.bat`, gửi file `userdata\logs\chan-doan.txt` |
| "Chưa có tài khoản Muse" | Làm mục 2 |
| Thẻ tài khoản báo "Lỗi đăng nhập" | Cookie hết hạn: đăng nhập lại muse.ai, lấy cookie mới, bấm **Cập nhật cookie** |
| "Hết hạn mức" | Video tự đổi sang tài khoản khác đang bật. Hết tài khoản thì đợi ngày reset (xem thẻ tài khoản) |
| Video đứng "Đang chờ" lâu | Không còn tài khoản dùng được, hoặc Song song lớn hơn số tài khoản × 2 |
| "Hết thời gian chờ" | Muse chậm: tăng "Chờ tối đa mỗi bước" trong **Cài đặt**, giảm Song song |
| Nhân vật nói sai lời / hai người cùng nói | Gen lại cảnh đó (kèm yêu cầu sửa) |
| Hậu kỳ lần đầu lâu | Máy đang tải mô hình nhận dạng giọng, đợi vài phút |
| `LUO Studio.bat` báo "Chưa cài đặt" | Chạy lại bước cài đặt ở mục 1 |

---

**Dữ liệu** (dự án, video, tài khoản) nằm trong thư mục `userdata\`. Sao lưu: chép cả thư mục này. Đừng gửi `userdata\api` cho người khác (có cookie đăng nhập).
