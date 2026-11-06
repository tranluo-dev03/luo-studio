# Lịch sử phiên bản LUO Studio

Số phiên bản theo dạng `x.y.z` (semantic versioning): `x` đổi khi có thay đổi không tương thích, `y` khi thêm tính năng, `z` khi chỉ sửa lỗi.
Nguồn sự thật của số phiên bản: dòng đầu của `version.txt` (cũng là tag git `vx.y.z` và `AppVer` trong `release-tools/installer.iss`; ba nơi phải khớp nhau khi phát hành).

## [Chưa phát hành]

## [1.2.1] - 2026-11-06

### Trace từng bước gen của một cảnh
- Trang chi tiết video: mỗi cảnh có nút **Các bước**. Bấm vào hiện bảng các bước gen của cảnh theo thứ tự (gen ảnh, gen video, gen lại vì lời
  nói / miệng / máy trôi, cắt & kiểm tra), mỗi bước có lúc bắt đầu và thời gian. Mỗi lệnh gen gửi LUO-API được tách tiếp: gửi lệnh, chờ hàng
  đợi API, chờ tài khoản / gia hạn phiên, mở tab Muse, đính ảnh tham chiếu, gửi prompt, Muse vẽ (kèm số Muse tự đo), tải file về API, Studio
  nhận kết quả; phần còn lại của bước là xử lý trên máy Studio. Bước lâu nhất được tô vàng; đầu bảng tóm tắt tổng, Muse vẽ, chờ, xử lý trên máy.
- Cảnh đang chạy thì bảng tự làm mới mỗi 2 giây. Video chạy tiếp / tự chạy lại thì trace lần trước vẫn giữ (mờ, dưới "Lần chạy trước"), bước
  bị dừng ghi rõ video dừng, lỗi hay đổi tài khoản ở bước đó.
- LUO-API: task có thêm `queue_wait` (thời gian chờ hàng đợi trình duyệt của API).

### Chọn tài khoản cho từng video, tự đổi tài khoản khi lỗi, chạy đêm không dừng cả lượt
- Hàng đợi: bấm dòng tài khoản trên thẻ video (hoặc nút tài khoản ở đầu trang chi tiết video) để chọn tay tài khoản Muse gen video đó, hoặc về
  "Tự động". Video đang chạy thì dừng rồi chạy tiếp ngay bằng tài khoản mới; video lỗi / đã dừng thì chạy tiếp luôn. Các cảnh đã xong được giữ,
  chỉ cảnh đang dở gen lại. Danh sách hiện trạng thái từng tài khoản (phiên ổn, lỗi đăng nhập, hết hạn mức, vừa lỗi với video này).
- Lỗi do tài khoản (phiên bị đăng xuất, cookie hỏng, tài khoản không được tạo video, hết hạn mức 24 giờ): video tự đổi sang tài khoản khác
  đang bật và chạy tiếp ngay từ cảnh đang dở, không thử lại vô ích trên tài khoản lỗi. Tài khoản chọn tay mà lỗi thì cũng tự bỏ chọn tay.
- Lỗi khác (Muse lỗi tạm, hết thời gian chờ, không còn tài khoản để đổi…): video không còn dừng hẳn mà tạm dừng, xếp lại cuối hàng chờ và tự
  chạy lại sau 2, 4, 6… phút (mặc định tối đa 3 lần, đổi ở Cài đặt → "Video lỗi (không do tài khoản): tự chạy lại"); các video khác vẫn chạy
  tiếp. Lỗi cố định của kịch bản (thiếu khối, sai số lượt thoại…) vẫn báo lỗi luôn. Thẻ video đang chờ hiện "Chạy lại sau m:ss".
- LUO-API: yêu cầu gen nhận thêm `pin_account` (ép video sang đúng tài khoản chọn tay) và `pin_avoid` (tài khoản không được chọn lại cho video);
  task lỗi có thêm `error_kind` (`account`, `quota`, `no_account`, `busy`, `other`) để client biết lỗi có phải do tài khoản.
- Sửa: các nút trên thanh tiêu đề (Dừng tất cả ở Hàng đợi; Bắt đầu / Chạy tiếp / Dừng ở trang chi tiết video) trước đây bấm không có tác dụng.

## [1.2.0] - 2026-11-06

### Đo thực tế (2026-11-06, cùng 2 tài khoản Muse, cùng prompt, chạy lần lượt bản 1.1.0 rồi 1.2.0; video chỉ trên 1 tài khoản vì tài khoản kia hết lượt video 24 giờ)
| Bài thử | 1.1.0 | 1.2.0 |
|---|---|---|
| Chuỗi 2 cảnh (ảnh khung đầu + video 5 s, như Studio) | 242 s | 158 s |
| 4 video 5 s cùng lúc, 1 tài khoản | 331 s | 145 s |
| 6 ảnh cùng lúc, 2 tài khoản | 109 s | 53 s |
| Thời gian của tool mỗi bước tuần tự (ngoài thời gian Muse vẽ) | 5,2–8,3 s | 2,6–3,7 s |

Thời gian Muse vẽ (đo bằng mốc giờ của chính Muse) dao động 18–86 s mỗi bước và không phụ thuộc phiên bản; phần lớn chênh lệch ở bài chuỗi 2 cảnh là do Muse vẽ nhanh hơn ở lượt sau. Lợi ích chắc chắn: phần của tool giảm ~4 s mỗi bước, và chạy song song nhanh gấp 2,1–2,3 lần.

### Tốc độ gen và lấy kết quả (LUO-API)
- **Tab Muse giữ ấm, không tạo lại mỗi lần** (`engine.py`): mỗi tài khoản một browser context (cookie bơm một lần, gia hạn phiên ghi thẳng vào context đang mở), tab được mượn và trả lại giữa các request. Trước đây mỗi cảnh mới tạo context mới, bơm cookie, tải lại muse.ai và chờ nối VM. Khởi động API thì mở sẵn một tab ấm cho mỗi tài khoản đang bật.
- **Hội thoại mới mở qua router của trang** (1–4 s) thay vì tải lại cả trang; chỉ tải lại khi router không dùng được.
- **Nhiều video song song trên một tài khoản** (`MUSE2API_ACCOUNT_PARALLEL`, mặc định 2; `MUSE2API_CONCURRENCY` mặc định 8): mỗi việc một tab trong cửa sổ riêng + giả lập focus (Chromium bóp tốc tab nền chung cửa sổ). Ghim tài khoản cho video cho phép tối đa 2 video/tài khoản, ưu tiên tài khoản còn trống. Trước đây ghim độc quyền: video thứ 3 khi chỉ còn 1 tài khoản có lượt phải đứng chờ tới hết 600 s rồi lỗi.
- **Theo dõi kết quả và tải file qua RPC nội bộ của trang** (`dom.py`, page helper `window.__luo`): `sessions.get` + `chat.history` cho biết file trợ lý vừa tạo (đường dẫn trên VM), `fs.raw` tải đúng file gốc. Không còn đợi trang vẽ `<video>`, không cuộn danh sách ảo, không quét DOM 0,6 s/lần. Đường DOM cũ giữ làm dự phòng khi RPC không dùng được.
- **Không bật Network/Runtime/Page domain trên tab**: kênh Noise của Muse bắn hàng nghìn sự kiện WebSocket mà mỗi lệnh CDP phải đọc bỏ.
- **`tasks.json` ghi theo lô ở luồng nền** (`store.py`): tiến độ chỉ cập nhật trong bộ nhớ, đĩa ghi gọn mỗi ~2 s, giữ 600 tác vụ mới nhất, tác vụ đã xong chỉ lưu 1500 ký tự prompt. Trước đây mỗi lần cập nhật tiến độ (0,6 s/lần mỗi việc) ghi lại toàn bộ file 31 MB (~0,25 s CPU, giữ khoá chung).
- **Studio**: hỏi trạng thái mỗi 1 s (trước 3 s); LUO-API cùng máy thì đọc thẳng file kết quả (`local_path`) thay vì tải lại qua HTTP. Chọn "Song song" tới 8 (tối đa số tài khoản × 2).

### Sửa
- **Ô soạn tin mới của Muse** (không còn `<form>` bao quanh): tham chiếu gắn bằng `DOM.setFileInputFiles` (không bơm base64 qua JS), đếm/xoá đính kèm theo nút "Remove attachment" và ảnh thu nhỏ đúng tầng; DataTransfer giữ làm dự phòng.
- **Không bao giờ trả lại chính tham chiếu làm kết quả**: so sha256 file nhận được với file đã gửi.
- **Trợ lý trả lời chỉ có chữ**: hỏi xin file một lần ("Please attach the final … file") trước khi báo lỗi; từ chối hẳn (tài khoản không được tạo video, vi phạm chính sách) thì báo ngay, không thử lại vô ích. Tự từ chối yêu cầu phê duyệt (approval) qua RPC lẫn thẻ trên trang.
- **Timeout mềm**: Muse còn đang chạy thì chờ thêm tới 1,5 lần (tối đa +5 phút) thay vì bỏ rồi tạo lại từ đầu.
- **Cookie `hatch_gw` / `hatch_vml` không còn bắt buộc** (Muse không đặt cho mọi tài khoản từ 10/2026).
- **CDP**: socket chết thì báo lỗi ngay thay vì quay vòng tới hết thời gian chờ; tab phục vụ 40 lượt thì được thay mới.
- Kết quả task có thêm `timing` (thời gian từng bước), `muse_thread`, `local_path`, `via` (rpc/dom).

### Dọn tài khoản Muse (tự chạy, giữ 10 hội thoại mới nhất)
- Tài khoản dùng lâu tích nhiều thứ trên VM của Muse (đo 2026-11-06 trên 5 tài khoản): 180–303 hội thoại và 417–680 file trong `workspace/imagine_media` (310–570 MB); mỗi lần tải trang phải nạp danh sách hội thoại, và trợ lý của Muse còn tự cắt / kiểm tra lại video theo thói quen đã "học" (file `*-trimmed-5s.mp4`, `first_frame_check.png`), nên tài khoản mới thường nhanh hơn.
- **Tự dọn khi tài khoản rảnh** (khi mở LUO rồi tối đa 30 phút/lần, bỏ qua tài khoản đang gen): giữ **10 hội thoại mới nhất** cùng hội thoại đang chạy / ghim / hội thoại chính / đang được LUO dùng, xoá các hội thoại còn lại **kèm file media của chính các hội thoại đó** (kết quả, bản trợ lý tự xử lý, tham chiếu đã tải lên; chỉ trong `imagine_media/` và `uploads/`; file mà hội thoại được giữ còn nhắc tới thì giữ). Studio đã có bản sao trên máy. Thư mục bộ nhớ nội bộ của Muse không bị đụng tới. Hội thoại không đọc được lịch sử thì không xoá.
- Xoá trên Muse **không hoàn tác được**. Tắt hẳn: `MUSE2API_THREAD_KEEP=0` trong `userdata\api\.env`; đổi số hội thoại giữ lại: `MUSE2API_THREAD_KEEP=<n>`; không xoá media: `MUSE2API_CLEANUP_MEDIA=0`; xoá thêm mọi media cũ hơn X ngày: `MUSE2API_MEDIA_KEEP_DAYS=X`.
- Dọn tay / xem trước: `POST /admin/accounts/{id}/cleanup` (`?dry_run=true` chỉ đếm). Chạy thử chỉ đếm trên tài khoản 396: 220 hội thoại, sẽ xoá 209 và 228 file media (trên 485), mất 21 s.
- Chưa đo tốc độ trước/sau khi dọn trên cùng một tài khoản.

### Thêm (các thay đổi trước đó, phát hành cùng 1.2.0)
- **Ghép 2 lớp: file dựng dở không còn làm hỏng lần chạy sau** (`split.py`): clip căn khớp (`_khop`) và clip khoá miệng (`_khoa`) ghi ra file tạm rồi mới đổi tên; khi dùng lại, file phải đọc được, nếu không thì tự xoá và làm lại. Trước đây tắt LUO giữa lúc ghi để lại file thiếu "moov atom", lần chạy sau dùng luôn và báo lỗi ffprobe.
- **Ghép 2 lớp: khoá camera + khoá miệng người thật khi nghe** (`split.py`): (1) mỗi clip khi nối khung được đưa về đúng khung hình của khung đầu (ORB + affine, bù phóng/dời, mép hụt lấy từ khung đầu): Muse tự phóng khung x1,2–1,4 giữa clip rồi nối khung giữ luôn cỡ đã phóng, robot BT12 chia-doi to dần tới hết video; prompt thêm câu camera đứng yên trên chân máy; (2) clip Muse phóng quá x1,15 thì gen lại (clip nói 1 lần, clip nghe theo số lần gen lại sẵn có), vì lấp mép khi phóng mạnh lộ vết ghép; (3) `khoa mieng: <KHOÁ>` khoá miệng riêng từng nhân vật (chia-doi đã thử bật cho HOC rồi TẮT: trông như dán miệng giả; từ khi gửi Muse nguyên văn, người nghe đã khép miệng); (4) căn khớp khung nhận lệch tới x0,6–1,6 (trước x0,85–1,2), mép hụt lấy từ khung nối: từ khi gửi Muse nguyên văn, robot chia-doi bị vẽ to x1,4 ngay khung đầu; (5) mặt ở khung đầu clip lệch cỡ khung nối quá x1,2 (Muse bỏ qua khung đầu, có clip đổi hẳn nền) thì gen lại; kịch bản chia-doi tả khung robot khớp ảnh gốc (đầu ~1/5 chiều cao khung, tới hông).
- **Ghép 2 lớp: nhân vật không còn bị đổi giữa video + người nghe khép miệng hẳn** (`split.py`, `engine.smart_cut`): (1) ảnh tham chiếu gốc của từng nhân vật (gắn trong biến thể) giờ được gửi kèm MỌI clip (khung nối + ảnh gốc + ảnh tham chiếu gốc), không chỉ lúc tạo ảnh gốc; trước đây robot BT12 chia-doi trôi sang một robot khác từ cảnh 8 rồi giữ luôn tới hết video. (2) Clip nói được cắt muộn thêm tối đa 0,7 giây tới khung người nói khép miệng, nên clip nghe cảnh sau của chính người đó không bắt đầu từ khung hé môi (Muse giữ môi hé, mấp máy cả clip). (3) Prompt clip nghe tả môi khép bằng câu khẳng định, bỏ "talking; lip movement; mouthing words" khỏi phần Avoid (chữ cấm gợi đúng hành vi đó).
- **Sửa câu dài bị cụt đuôi ở ghép 2 lớp** (`split.py`): độ dài clip nói luôn là 6 giây vì hàm đếm âm tiết chỉ đếm chữ trong ngoặc kép (câu 18 chữ cụt "avatar. Anytime, anywhere."). Giờ đếm đúng (câu dài xin 8–10 giây); gen lại vì thiếu chữ mà lời kéo tới sát cuối clip thì xin clip dài hơn. Kiểm tra lời nói chấp nhận từ ghép viết liền/rời.
- **Lời thoại đúng từng chữ:** kiểm tra lời nói (Whisper) báo lỗi khi thừa hoặc thiếu dù chỉ 1 từ, ở mọi câu (trước đây bỏ qua câu dưới 3 từ, cho thừa 1 từ, thiếu tới 30%); chuẩn hoá viết tắt / số / tiếng ừm; gen lại tối đa 2 lần (trước 1). Bản đã cắt sát lời được kiểm lại, mất chữ thì cắt lại rộng hơn. Clip nghe không còn dùng ảnh tĩnh khi gen lại vẫn có tiếng (giữ bản ít tiếng nhất hoặc dùng lại clip câm của nhân vật).
- **Sửa người nghe nhép miệng / gật gù theo người nói ở chế độ ghép 2 lớp** (`split.py`): câu "no talking-like head bobbing, never mirrors the speaker" trong khối NGHE làm Muse lồng tiếng lẩm bẩm vào clip nghe rồi tạo mặt theo tiếng đó (246 clip đo được: có câu đó 40% có tiếng, không có 3%). Studio tự bỏ các mệnh đề nhắc tới việc nói khỏi khối NGHE; luôn đo tiếng clip nghe, có tiếng thì gen lại, vẫn có tiếng thì dùng lại clip nghe câm gần nhất của nhân vật đó (chưa có thì ảnh khung đầu).
- **Thể loại chia đôi màn hình + gia sư AI** (`SAMPLE/chia-doi-gia-su-ai/`, hậu kỳ `app/production/types/chia-doi-gia-su-ai/`): robot AI nửa trái, người dùng bàn cà phê nửa phải, 3 biến thể có ảnh tham chiếu. Ghép 2 lớp: nhân vật nền có thể có `khung` riêng (`split.compose`). Hậu kỳ chung: viền sai/đúng giới hạn trong một vùng và nháy cuối câu (`phu_de.vien`).
- **Ảnh tham chiếu từ link Google Drive dạng chia sẻ và đường dẫn tệp trên máy** (`server._download_image`).
- **Tab API Muse:** đếm số video gen trong ngày (từ 00:00) của từng tài khoản, cảnh báo khi gần ~100 (chỉ cảnh báo, không chặn); thanh hạn mức lấy theo token Extra (chưa có Extra thì theo hạn mức tuần).
- **Nhận diện thêm câu báo hết hạn mức video 24 giờ của Muse** ("video limit for the last 24 hours is reached"): dừng thử lại, đánh dấu tài khoản; lời từ chối giữ 400 ký tự.
- **Cài đặt:** ô chọn dễ nhìn hơn; bỏ mục Logo / End card mặc định, "Thư mục xuất" và "Nhận dạng giọng" chuyển sang khung "Xuất video".
- **Người nói quay lưng không còn làm người kia nhép miệng / làm động tác thay** (`engine.py`): hai nhân vật cùng giới (khoá tự đặt) được tách giọng THẤP / CAO. Cảnh có người nói quay lưng (`QUAY_LUNG_<K>`) có thể gen thêm clip câm lấy hình rồi ghép tiếng từ clip giọng; mặc định TẮT (bật bằng `voice_swap: true`), hiện chỉ dùng tách giọng.
- **Thể loại lồng tiếng ngoài khung + hiệu ứng khi ghép** (mẫu "Đổi tóc + camera dò mặt" trong `SAMPLE/Doi toc/`): (1) trường `Voice` không còn bị ép "nhép miệng trên hình"; Studio chỉ bắt buộc clip có tiếng, ai nói do kịch bản quy định, nên làm được giọng đọc ngoài khung. (2) Loại dự án không dùng `LUOT`: phụ đề Hậu kỳ lấy từ lời trong ngoặc kép ở `Voice` từng cảnh. (3) Trường cảnh `Chuyển cảnh: chớp trắng|vàng|đen|#RRGGBB [giây]`: chớp sáng khi vào cảnh, không đổi độ dài video. (4) Trường cảnh `Lớp phủ: camera [png]` (`app/luo-studio/camera_overlay.py`): giao diện camera điện thoại + viền hình trứng bám theo khuôn mặt từng khung hình (mediapipe), ghép lúc nối clip; lỗi thì dùng clip gốc.
- **Loại dự án "Ghép 2 lớp"** (`app/luo-studio/split.py`): cho bố cục mà các nhân vật ở vùng tách biệt (gia sư AI trong khung bo góc phía trên + người học selfie phía dưới, chia đôi màn hình...). Mỗi nhân vật gen RIÊNG, một mình trong khung (không thể nói chồng), rồi ghép bằng ffmpeg: ảnh gốc mỗi nhân vật (mọi clip bắt đầu từ đó, mặt/màu không trôi), thư viện clip "đang nghe" dùng lại (hoặc gen riêng mỗi cảnh), clip người nói cắt sát lời + cân màu theo từng nhân vật, khung bo góc có viền, tiếng chỉ từ người nói. Script dùng khối `[GHEP HAI LOP]` (bố cục, tỉ lệ khung, chế độ clip nghe) + `[NHAN VAT <KHOÁ>]` / `[NGHE <KHOÁ>]`; mỗi lượt thoại là một cảnh. Mẫu trong `SAMPLE/Ghep hai lop/`. LUO-API nhận tỉ lệ khung theo từng lần gen (16:9 / 1:1 cho nhân vật trong khung).
- **Mỗi video chỉ gen bằng một tài khoản Muse:** LUO-API có thêm "ghim tài khoản" (`pin` trong request ảnh/video, `DELETE /v1/pins/{pin}`). Cảnh đầu của video chọn một tài khoản chưa bị video khác ghim, mọi cảnh sau dùng đúng tài khoản đó; lỗi thì thử lại trên chính tài khoản đó, không tự đổi tài khoản. Video xong/dừng/lỗi thì bỏ ghim; Chạy tiếp ưu tiên tài khoản cũ. Hết hạn mức chỉ dừng video của tài khoản đó (trước đây dừng cả hàng đợi), và video mới tránh tài khoản vừa hết hạn mức nếu còn tài khoản khác. Thẻ video hiện tài khoản của cả video.
- **Hiện tài khoản Muse đang gen video/cảnh:** LUO-API trả thêm `account` (id) và `account_label` (tên gợi nhớ, không lộ cookie) ngay khi task nhận được tài khoản (kể cả khi tự chuyển tài khoản dự phòng); Studio lưu vào `account` của từng cảnh trong hàng đợi, ghi nhật ký "Cảnh N: gen bằng tài khoản X", hiện trên thẻ video (tài khoản của cảnh đang chạy) và trên từng thẻ cảnh.
- **Cập nhật không mất dữ liệu:** `update.ps1` và `Cap nhat.bat` (sao lưu nhẹ dữ liệu quan trọng vào `userdata-backup/`, `git pull` hoặc tải ZIP mới rồi chép đè, không đụng `userdata/`, `.venv`, `bin`; chạy lại `setup.ps1`). Có tuỳ chọn `-ZipFile` cho máy không có git hoặc mạng hạn chế.
- **`Chan doan.bat`** (`app/chan_doan.py`): kiểm tra máy (CPU có AVX không, máy ảo, Visual C++ Redistributable, phiên bản thư viện, thử nạp từng thư viện nhị phân trong tiến trình riêng) và lưu báo cáo vào `userdata\logs\chan-doan.txt`; `setup.ps1` cảnh báo sớm nếu thiếu Visual C++ Redistributable.
- `setup.ps1` tự cài Python 3.11 khi thiếu (winget, nếu không được thì bộ cài chính thức từ python.org).

### Sửa
- **Ảnh tham chiếu "Ảnh / mp3" không giữ được nhân vật:** chú thích gửi Muse chỉ ghi tên trường ("ảnh #1 là Ngoại hình; ảnh #2 là Ngoại hình") nên Muse không biết ảnh nào của nhân vật nào và trộn mặt. Giờ chú thích nêu rõ nhân vật (theo `TEN_<khoá>`), ví dụ "reference image #1 is the EXACT look of the AI robot tutor (character DAY)...", và lệnh gen ảnh khẳng định ảnh tham chiếu thắng mô tả chữ khi mâu thuẫn.
- **Ảnh tham chiếu gắn trong biến thể:** (1) chế độ Ghép 2 lớp gửi MỌI ảnh cho cả hai nhân vật nên khuôn mặt bị trộn; giờ mỗi nhân vật chỉ nhận ảnh của token kết thúc bằng `_<KHOÁ>` của nó (token không thuộc nhân vật nào thì dùng chung). (2) Tệp được gắn nhưng không còn trên đĩa trước đây bị bỏ qua âm thầm; giờ nhật ký cảnh báo kèm tên tệp. (3) Nhật ký ghi số ảnh tham chiếu thực sự gửi cho mỗi lần gen ảnh khung đầu; số thứ tự trong chú thích ảnh khớp thứ tự gửi khi dự án có ảnh chung.
- **Bấm Gen bị "mất kết nối API" (Studio chết giữa chừng):** máy có Microsoft Visual C++ Redistributable x64 cũ (< 14.40, vd. 14.29) làm ctranslate2/onnxruntime crash cứng trong `MSVCP140.dll`, mà Whisper khi Gen chạy ngay trong tiến trình Studio. Whisper khi Gen giờ chạy trong một tiến trình con riêng (nạp mô hình một lần, chết thì tự bật lại; cảnh đó cắt theo cách thường); `setup.ps1` kiểm tra phiên bản file DLL và tự tải + cài bản mới (hỏi UAC); trình khởi động cảnh báo khi phát hiện bản cũ; `Chan doan.bat` báo "QUÁ CŨ" và in `crash.log` (stack Python lúc crash, ghi bằng `faulthandler`).
- **Tiến trình treo từ các lần mở trước tranh chấp cổng:** trình khởi động đưa mình vào Job Object "tắt cùng nhau" nên LUO-API, trình duyệt con, Whisper chết theo kể cả khi crash; lúc mở thì dọn trình khởi động/LUO-API cũ ghi trong `running.json` và LUO-API mồ côi của bất kỳ bản cài nào. `setup.ps1` tắt tiến trình đang chạy từ `.venv` của thư mục trước khi cài thư viện (tránh "Access is denied").
- **`setup.ps1` báo "No module named venv":** chọn nhầm Python embeddable (bản rút gọn, không có venv/pip). Giờ chỉ chọn Python có `venv` + `ensurepip`, và thay `Sort-Object` (PowerShell 5.1 không giữ thứ tự phần tử bằng nhau, nhiều Python cùng 3.12 thì chọn ngẫu nhiên) bằng chọn tuần tự ổn định.
- `setup.ps1` cảnh báo trước thư mục cài có dấu / trong OneDrive / quá dài / ổ đĩa còn dưới 5 GB, và gỡ dấu "tải từ Internet" khỏi file (SmartScreen chặn `.bat`).
- **Hậu kỳ không còn chết khi thư viện nhận dạng giọng hỏng cứng** (lỗi "Hậu kỳ lỗi, xem nhật ký" sau cảnh báo `pkg_resources`, mã thoát `0xC0000005`, gặp trên một số máy): Whisper giờ chạy trong tiến trình con; thử có VAD trước, nếu VAD hỏng thì tự chuyển sang không VAD (nhớ lại để lần sau bỏ qua), nếu cả Whisper hỏng thì vẫn ra video với phụ đề ước lượng kèm cảnh báo. Chất lượng căn phụ đề trên máy chạy được VAD giữ nguyên.
- **Phụ đề lệch tiếng nói ở video trộn tiếng Tây Ban Nha + tiếng Anh:** Whisper chỉ đoán ngôn ngữ MỘT lần cho cả video nên bỏ sót hoặc nghe sai các câu ngắn của ngôn ngữ còn lại, rồi cách gán tuần tự trên cả video làm các câu sau bị dồn cục và chồng lấn (đã tái hiện: ép sai ngôn ngữ thì 8/11 dòng không khớp). Hậu kỳ giờ căn phụ đề theo từng cảnh: mỗi cảnh được nhận dạng riêng (tự nhận ngôn ngữ riêng, câu có ¿ ¡ ñ thì chốt tiếng Tây Ban Nha) và chỉ gán cho phụ đề của lượt thoại đó; cảnh Whisper không nghe thấy thì ước lượng trong khoảng của chính cảnh, không ảnh hưởng cảnh khác. Mốc từng cảnh trong `raw.mp4` được xác định bằng khớp âm thanh; điểm bắt đầu tiếng nói dò theo năng lượng âm thanh nên dòng đầu mỗi cảnh chính xác hơn cả cách cũ (cách cũ bị VAD đệm sớm 0,25–0,4 giây).
- **`setup.ps1` / `Cap nhat.bat` không nhận ra Python đã cài (rồi bộ cài báo lỗi 1603):** khi đã có `.venv` dùng được thì không còn đòi tìm Python hệ thống (đúng với lúc cập nhật); nếu cần tìm thì dò nhiều cách (py launcher, registry PEP 514 kể cả thư mục cài tuỳ ý, thư mục mặc định, PATH) và, nếu không thấy bản dùng được, liệt kê các Python đã thấy kèm lý do (3.13/3.14, 32-bit...). Bộ cài Python giờ cài song song, không sửa PATH, không cài py launcher (tránh xung đột gây lỗi 1603), ghi log và báo chi tiết khi lỗi; bỏ `winget` (lỗi nguồn `0x8a15000f`). Thêm `-CheckOnly` (chỉ kiểm tra Python) và `-PythonInstaller` (dùng bộ cài tải sẵn). `.venv` hỏng được báo rõ và tạo lại.
- **Kiểm tra miệng người nghe và tự gen lại là một công tắc trong Cài đặt**, tự kiểm tra máy có chạy được không: khi bật thì thử thật trong tiến trình riêng, nếu không khả dụng thì tự tắt và hiện lý do; lúc chạy video cũng kiểm tra và tự tắt (không báo lỗi lặp ở từng cảnh). Độ nhạy và số lần tự gen lại chỉ hiện khi công tắc bật.
- **Lỗi "No such file or directory ... sceneN_last.png"**: khi âm thanh của clip đã cắt dài hơn hình vài chục mili giây, `ffmpeg -sseof` nhảy tới mốc sau khung hình cuối, không ghi khung nào mà vẫn báo thành công. `grab_frame` giờ tính mốc theo thời lượng của luồng hình, kiểm tra file thật sự được ghi, thử lùi dần và cuối cùng giải mã hết để lấy khung cuối (đã thử trên 103 clip thật, trước đây 2 clip lỗi, nay 0).
- Cảnh báo "bỏ qua kiểm tra miệng ... DLL load failed" (mediapipe) nay kèm gợi ý nguyên nhân (thiếu Visual C++ Redistributable hoặc CPU/máy ảo không có AVX) và hướng dẫn chạy `Chan doan.bat`.
- Ghim `faster-whisper`, `ctranslate2`, `onnxruntime` đúng phiên bản đã chạy ổn trong `requirements.txt` để máy cài mới không bị trôi phiên bản.

### Đổi
- Tài liệu cài đặt (`README.md`, `HUONG-DAN.txt`): cài từ GitHub (ZIP hoặc git) bằng `setup.ps1`; bỏ hướng dẫn tắt/loại trừ chống virus.

## [1.1.0] - 2026-10-23

### Thêm
- **Nhân vật tổng quát:** mỗi nhân vật có khoá bất kỳ (không chỉ `day`/`hoc`) với các token `TEN_`, `NGUOI_`, `GIONG_`, `POS_`, `VAI_`, `NGHE_`, `EMO_`, `BOX_<khoá>`; số nhân vật bất kỳ, vị trí khuôn mặt tuỳ ý cho bộ đo miệng. Prompt của các loại dự án cũ giữ nguyên từng ký tự.
- **Cảnh không có lời thoại** (hành động, chuyển cảnh) không đòi tiếng, không cắt theo lời, không đo miệng.
- **`SAMPLE/phan-tich-video.py`:** phân tích video tham chiếu (tốc độ nói từng câu, cảnh cắt, chuyển động mạnh, ảnh ghép dày từng lượt).
- **`SAMPLE/HUONG-DAN-CHO-AGENT.md`:** hướng dẫn agent viết kịch bản và biến thể cho mọi thể loại, có quy trình phân tích video bắt buộc.
- Kịch bản và biến thể mẫu: cảnh sát và tài xế xe tải (`SAMPLE/Canh sat nu/`), xe tải và gia sư AI (`SAMPLE/Xe tai/`).
- Hiển thị số phiên bản ở thanh bên trái của giao diện.

### Sửa
- Clip Muse trả về không có tiếng: tự gen lại; nếu còn sót thì chèn im lặng khi ghép (trước đây lỗi `matches no streams`).
- Studio dùng đúng cổng LUO-API mà launcher đã bật khi cổng 18610 bị chiếm (trước đây lỗi "Không kết nối được LUO-API").
- Bộ đo miệng báo nhầm khi người nghe chỉ cười: thêm vùng khuôn mặt cho bố cục TOP/BOTTOM, tiêu chí há miệng rộng và nhịp mở-khép; hạ số lần tự gen lại mặc định từ 5 xuống 2.
- Bảng cảm xúc không còn chỉ dẫn cử chỉ tay/thân (gãi đầu, nhún vai) làm tư thế lệch lan sang các cảnh sau.

## [1.0.0] - 2026-10-21

- Bản mã nguồn đầu tiên, kèm script cài đặt; tách bước viết kịch bản từ video khỏi bước tạo biến thể trong prompt cho Claude; ghim `av>=14` để hậu kỳ mở được âm thanh.
