# Pasado en Palitos — dự án có thể tái tạo

Đặt cuidado_ab.mp3 và guion_01_es.txt ở thư mục gốc. Giọng thu gốc là nguồn thời gian duy nhất. Không TTS hoặc HeyGen.

Cài đặt: `npm ci` và `python -m pip install -r requirements.txt`. Cần FFmpeg trong PATH.

Dựng tiếp từ bộ nhớ đệm: `python work/produce-native.py`.

Nhận dạng lại từ đầu khi cần: đặt mô hình ONNX tại `.cache/reference-asr/sherpa-onnx-whisper-base/`, chạy `python work/transcribe_onnx.py`, rồi chạy bộ điều phối bên trên. Các chunk ASR tự dùng lại khi có sẵn. Khi thay đổi nguồn âm thanh, phải xóa cache ASR cũ và dựng lại; bộ cache không tự xác minh nguồn âm thanh mới.

Các cảnh là React/SVG dùng chung với Remotion tại src/index.jsx. Backend xuất nhanh: React SSR, resvg, canvas và FFmpeg. Có thể dùng CLI Remotion tiêu chuẩn nhưng chậm hơn: `npx remotion render src/index.jsx Episode output/remotion_export.mp4 --codec=h264 --audio-codec=aac --concurrency=1`.

Bản xuất gốc 1920×1080, container 30 fps, hoạt hình 15 tư thế/giây (on twos). Tệp nguồn MP3 giữ nguyên; bản mix dùng gain 0,85 cùng một số SFX nhỏ. Phụ đề là bản ASR theo cụm câu, cần nghe rà soát. Xem production_report.md về các giới hạn biên tập và độ chính xác.

work/native-chunks/ lưu video từng đoạn và marker `.done`. Manifest ghi hash cấu hình để loại bỏ marker cũ khi sửa cảnh. Bộ ZIP chứa mã, input gốc, mô hình và cache nhận dạng, nhưng không chứa toàn bộ video trung gian; có thể dựng lại từ các dữ liệu đó.
