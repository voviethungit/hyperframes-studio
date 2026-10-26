# Pasado en Palitos — tập 01

**¿Sobrevivirías 24 HORAS en la EDAD MEDIA? (Año 1290)**

Bản dựng kỹ thuật dài **21:49,600**, H.264/AAC, 1920×1080, 30 fps. Hoạt hình on twos: 15 tư thế/giây. Bản thu gốc giữ nguyên nội dung, thứ tự và tốc độ; bản mix dùng gain 0,85. Không TTS, không HeyGen.

## Bản thử phong cách v2

Đã dựng lại **82,667 giây mở đầu** theo hướng nét vẽ tay, màu ấm, bối cảnh có phối cảnh và thẻ giải thích nền trắng. Đây là bản thử phong cách; chưa thay bản toàn tập cũ.

- [Video mẫu v2](output/style_v2/preview_style_v2.mp4)
- [Bảng khung hình v2](output/style_v2/contact_sheet.jpg)
- [Phân tích phong cách](output/style_v2/style_notes_vi.md)

Giọng thu gốc được giữ nguyên nội dung và tốc độ. Nguồn dựng: `work/style-v2/`; chạy `python work/style-v2/build.py` để tái tạo. Không đưa hình ảnh hoặc âm thanh của demo3 vào video mới.

## Tải thành phẩm

Các tệp lớn được lưu bằng **Git LFS** trong thư mục `output/`:

- [MP4 toàn tập](output/pasado_en_palitos_01.mp4)
- [Bản thử 75 giây](output/preview_75s.mp4)
- [ZIP mã nguồn, input, mô hình và cache](output/reproducible_project.zip)

Trên GitHub, mở tệp rồi chọn **Download raw file**. Khi clone repository, cần cài Git LFS và chạy `git lfs pull` để tải tệp thực thay vì con trỏ.

## Kiểm tra

- Đủ 39.288 frame; giải mã toàn bộ không lỗi và không phát hiện khung đen theo ngưỡng kiểm tra.
- Phát thử thành công ở đầu, giữa và cuối trong Chromium.
- Tương quan toàn bộ âm thanh giải mã với nguồn: 0,999968.
- 69 ảnh mẫu trải toàn timeline: `output/contact_sheet.jpg`.

## Giới hạn

Đây chưa phải bản đạt trọn brief premium: diễn xuất và tương tác đạo cụ còn đơn giản; phụ đề ASR cần nghe rà soát. Xem `output/production_report.md` và `output/qa_report.json`.

## Chạy lại

Cần Python, Node.js và FFmpeg:

```sh
npm ci
python -m pip install -r requirements.txt
python work/produce-native.py
```

Bộ nhớ đệm ASR đã có sẵn. Để nhận dạng lại, lấy mô hình Whisper base ONNX trong ZIP trong output/, đặt vào `.cache/reference-asr/sherpa-onnx-whisper-base/`, rồi chạy `python work/transcribe_onnx.py`.

Giữ nguyên hai tệp `cuidado_ab.mp3` và `guion_01_es.txt` ở thư mục gốc. Không dùng cache ASR cũ cho bản thu khác.
