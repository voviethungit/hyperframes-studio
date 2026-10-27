# Báo cáo sản xuất — Pasado en Palitos

Trạng thái: Đã xuất bản dựng kỹ thuật toàn thời lượng; chưa đạt mọi yêu cầu biên tập/premium.

## Nguồn và khóa giọng

- cuidado_ab.mp3: MP3 mono, 44100 Hz, 128 kbps, thời lượng ffprobe 1309.596735 giây.
- SHA-256: `5bd242aa4fb6042318c251f30bb8cb884b69c8d15050d7ee17bad068415b2649`.
- Tệp gốc không bị sửa. Không TTS, không cắt, lặp, đổi cao độ hoặc kéo tốc độ. Bản xuất dùng gain 0,85, cộng một số SFX tổng hợp nhỏ; không nhạc nền.
- astats phát hiện overshoot khoảng +0,90 dBFS khi giải mã MP3. Điều này không tự chứng minh bản thu đã bị clipping trước mã hóa. Không áp dụng lọc mạnh.

## Nhận dạng và phụ đề

Đã đọc toàn bộ kịch bản và nhận dạng toàn bộ bản thu bằng sherpa-onnx Whisper base int8, tiếng Tây Ban Nha, chạy CPU cục bộ. Không gửi bản thu tới API. Lượt tải faster-whisper small bị proxy từ chối ở CDN trọng số; dùng mô hình ONNX đã có sẵn.

Có 331 cụm câu ASR và 362 vùng khác biệt theo phép so sánh chuẩn hóa. Độ tương đồng chuỗi từ: 0.782. Danh sách này chứa cả lỗi nhận dạng; không thể coi tất cả là thay đổi thực sự trong lời đọc. Bản ASR thô được giữ lại.

Mô hình có mốc cụm câu bằng timestamp token, không có đầu ra attention để căn từng từ. Không tạo mốc từ giả. Confidence của mô hình không được cung cấp nên ghi null. Phụ đề SRT/VTT là bản ASR cần rà soát, chưa phải bản đã được người biên tập nghe xác minh từng chữ. Các lỗi như hoz → voz/os, haces → ases/aces và senas/cenas có thể xuất hiện. Chưa chạy forced alignment.

## Dựng hình và khả năng khôi phục

- Mã cảnh React/Remotion tại src/index.jsx, rig SVG tách lớp tại output/assets/hero-01.svg.
- Backend xuất: cùng cảnh React/SVG được render phía máy chủ, raster SVG bằng resvg và ghép lớp canvas/FFmpeg. Chromium đã xuất một khung kiểm tra nhưng quá chậm để dùng cho toàn tập trong môi trường 2 CPU.
- Kích thước raster gốc 1920×1080; tệp H.264/AAC, 30 fps. Hoạt hình on twos: 15 tư thế/giây, mỗi tư thế giữ hai frame. Đây là các frame lặp có chủ đích, không phải kéo giọng để khớp hình.
- Các đoạn dựng có marker .done; cache_manifest.json lưu phạm vi frame. Chunk ASR được tái sử dụng khi khởi động lại.
- Mưa ở backend canvas dùng hạt được tính cùng vị trí với SVG. Đã sửa tư thế ngồi bữa sáng và dựng lại riêng cảnh trượt bùn để hoàn thành cú ngã sớm trong câu.
- Không có HeyGen, không tạo giọng mới, không có lượt API tạo video trả phí.
- scene_plan.json phủ liên tục từ 0 tới T theo cụm câu thật; scene_state.json ghi trạng thái và các hành động đã hoàn thành.

## Giới hạn chưa giải quyết

Bản này là bản dựng kỹ thuật hoàn chỉnh về thời lượng, chưa phải sản phẩm premium đạt toàn bộ brief. Nhiều đoạn giải thích vẫn dùng cùng bố cục rộng và ít tư thế; chưa có đầy đủ diễn xuất riêng cho mọi câu, chuyển giao đạo cụ và tương tác tay chính xác. Cảnh suýt cắt tay, ngựa kéo xe, bữa ăn, nhân vật phụ và chiều sâu bối cảnh còn đơn giản. Ledger là trạng thái theo quy tắc, không phải hệ mô phỏng bảo toàn đạo cụ hoàn chỉnh; các cut vẫn cần kiểm tra liên tục thủ công. Turnaround là biểu diễn rig đơn giản, chưa phải bộ mẫu profile hoàn thiện để duyệt sản xuất. SFX chỉ gồm một số điểm nhấn, chưa có đầy đủ ambience theo brief. Không nên coi các kiểm tra tự động là duyệt lịch sử/nghệ thuật hoặc xem/nghe thủ công toàn bộ.

## Kiểm tra

```json
{
  "checks": {
    "resolution": true,
    "fps": true,
    "codec": true,
    "duration_difference": 0.003264999999828433,
    "expected_frames": 39288,
    "reported_frames": 39288
  },
  "audio_compare": {
    "sample_rate": 16000,
    "source_samples": 20953356,
    "output_samples": 20953687,
    "gain": 0.8490586280822754,
    "correlation": 0.9999681222300648,
    "method": "sample-by-sample decoded correlation; AAC loss expected",
    "no_stretch_or_edit_in_pipeline": true
  },
  "full_decode": {
    "exit_code": 0,
    "frames": 39288,
    "black_intervals": [],
    "decoder_errors": false
  },
  "audio_peak_dbfs": -0.532939,
  "browser_playback_passed": true,
  "source_mp3_unchanged": true
}
```

Đã trích đầu–giữa–cuối từng phần truyện trong contact_sheet.jpg; số mẫu: 69. Cần phân biệt kiểm tra giải mã/khung hình với việc xem và nghe thủ công toàn bộ video.

## Tái tạo

Chạy `python -m pip install -r requirements.txt` và `npm ci`, sau đó `PYTHONPATH=work/pydeps python work/transcribe_onnx.py`, rồi `python work/produce-native.py`. Cần sherpa-onnx, numpy, Pillow, FFmpeg, mô hình Whisper base ONNX ở đường dẫn ghi trong mã. Node dependency được khóa bằng package-lock.json. Đặt hai tệp đầu vào ở thư mục gốc.

## Bàn giao

Tất cả tệp nằm trong ./output/ của dự án. Bộ duyệt tự động đã từ chối sao chép bản thu sang thư mục bàn giao ngoài dự án của giao diện chat vì chưa có ủy quyền rõ ràng cho đích đó; không thực hiện đường vòng.
