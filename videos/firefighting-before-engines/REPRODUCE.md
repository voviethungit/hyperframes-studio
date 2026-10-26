# Reproduce this film

The source package contains the complete original 2D animation, 13 generated cartoon backgrounds, the semantic timeline and exact acoustic phrase/word alignment. It contains no standalone narration recording, uploaded reference video or model weights.

Requirements: Node 24+, Chromium, FFmpeg with libx264, Python 3.11+, PyAV, and puppeteer-core. The render source is `film.js`; every frame is a deterministic function of the master audio time.

1. Place the unchanged supplied MP3 at `private/voice.mp3` (create `private` first).
2. Run `python3 scripts/build.py`.
3. Serve the directory at `http://127.0.0.1:3018/` with `python3 -m http.server 3018 --bind 127.0.0.1`.
4. Adjust the puppeteer-core package path in the Node helper scripts if it differs in your machine. Default Chromium path is `/usr/bin/chromium`.
5. Run `node scripts/render.cjs --workers 4` to render 42,436 frames. The final source already contains all connection and motion refinements; it does not require the original production patch workflow.
6. Run `python3 scripts/mux.py`. PyAV copies the original narration packets without audio re-encoding and sets the final video sample to end at 1697.436735 seconds. Use a clean `renders/patches` directory when reproducing directly from final source.
7. Run `node scripts/inspect.cjs`, `node scripts/motion.cjs`, and `python3 scripts/verify.py`.

The original production used a base render plus a small set of I-frame-safe connection refinements. `scripts/finish.py` documents that production workflow; it is unnecessary for a fresh render from the final `film.js`. The GitHub delivery video was fully decoded, checked for black gaps and compared to the source narration at encoded-packet and decoded-PCM levels.

Acoustic alignment was generated with the Russian GigaAM v2 CTC int8 model on a 40 ms grid. The exact alignment files are included so recreating the film does not require downloading or running the speech model. Source narration and source script hashes are recorded in the manifest. No TTS, replacement voice, lip sync, background dialogue, music or SFX are added.
