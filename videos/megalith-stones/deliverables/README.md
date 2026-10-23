# История в Палочках — manifest đầy đủ cho video 30 phút

Đã khôi phục môi trường, tải cả hai tệp và phân tích toàn bộ bản thu tiếng Nga.
Đã hoàn thành **234 cảnh**, căn theo **522 cụm câu / 3.982 từ**, từ `00:00.000`
đến **`30:25.410612`**. Đây là gói sản xuất đầy đủ theo phương án dự phòng bạn
yêu cầu; **chưa có video hoặc clip HeyGen được tạo**.

Điểm chặn duy nhất ở bước tạo hình cuối: **phiên này thiếu công cụ tạo clip hình
ảnh HeyGen đã xác thực**. HyperFrames và FFmpeg có thể dựng/chỉnh sửa cục bộ,
nhưng không thay thế được khả năng HeyGen mà yêu cầu của bạn chỉ định.

## Mở và kiểm tra

- `review-manifest.html`: tải xuống rồi mở bằng trình duyệt. Có tìm kiếm cảnh,
  nội dung tiếng Nga, hành động tiếng Anh và trạng thái nối cảnh. Bạn có thể chọn
  MP3 gốc từ máy mình để phát/nhảy đến từng cảnh; trang không tải MP3 lên đâu cả.
- `scene-manifest.csv`: mở bằng Excel/Google Sheets; UTF-8 có BOM, đủ 234 cảnh.
- `scene-manifest.json`: đầy đủ dữ liệu và các cue câu theo thời gian để dựng.
- `scene-manifest.md`: bản đọc tuần tự toàn bộ cảnh, lời Nga, hành động và continuity.
- `phrase-alignment.json` / `word-alignment.json`: thời điểm căn cụm câu/từ.
- `alignment-report.json`: kiểm tra phủ timeline, thời lượng, SHA-256 và vị trí cần rà soát.
- `PRODUCTION.md`: khóa phong cách, nhân vật, cơ học, bối cảnh lịch sử, trạng thái
  tích hợp HeyGen và quy trình hoàn thiện khi có công cụ tạo clip thật.

Các tệp chữ trong gói là tài liệu sản xuất/kiểm tra; chúng **không** phải phụ đề
tự động sẽ xuất hiện trong video. Mã asset HeyGen để trống vì chưa tạo asset thật.

## Độ chính xác và bảo toàn bản thu

Mốc thời gian được căn bằng xác suất âm học CTC tiếng Nga trên lưới **40 ms**,
không phân bổ theo số chữ hay chia đều 15 giây. Đó là ước lượng bằng mô hình,
chưa phải nghe kiểm thủ công từng âm. Bốn vị trí được đánh dấu để kiểm lại,
trong đó có từ tiếng Anh `fascinates` trong kịch bản Nga. Không sửa từ này và
không sửa bản thu.

MP3 gốc không bị cắt, tăng/giảm tốc, tạo lại hoặc thay giọng. Thời lượng container
đo được là `1825.410612` giây, dài hơn mốc làm tròn bạn cung cấp `0.000612` giây.
Timeline bám đúng thời lượng gốc này. SHA-256 được lưu để xác minh.

Các kiểm tra cấu trúc đã đạt: timeline liên tục; không khoảng trống; mọi từ được
gán đúng một lần; mọi câu được phủ; timestamp tăng liên tục; cue nằm trong cảnh;
giữ nguyên toàn bộ từ trong kịch bản; không bịa asset ID. Kiểm tra hình thể,
chuyển động và xem toàn bộ phim vẫn phải thực hiện sau khi có footage thật.

Gói tải không chứa MP3 gốc, bản WAV phân tích, mô hình nhận dạng hoặc video mẫu
của bạn. File audio gốc được giữ riêng trong môi trường làm việc.
