# Gói sản xuất cho video hoàn chỉnh

Video MP4 đầy đủ nằm ở thư mục cha: `megalith-stones-complete.mp4`. Xem README ở thư mục cha để tải video.

Gói này gồm manifest 234 cảnh, căn câu/từ, continuity, cue cơ học, khóa phong cách và báo cáo kiểm tra. `review-manifest.html` là trang đối chiếu timeline bằng MP3 cục bộ, không phải phim.

Video được dựng cục bộ bằng Canvas 2D / FFmpeg / PyAV. HeyGen không được sử dụng, nên các HeyGen asset ID để trống. Căn âm học có lưới 40 ms và bốn vị trí cần rà soát; bản thu không bị sửa.

`final-video-check.json` xác minh đúng 30:25.410612, 1920×1080, 45.636 khung hình, giải mã toàn bộ file không lỗi và âm thanh nén/giải mã trùng bản gốc. `browser-playback-check.json` ghi nhận phát và tua thành công ở đầu, giữa, cuối phim.
