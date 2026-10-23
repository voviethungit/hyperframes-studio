# Reproducing this editorial package

This package is not an import format promised by HeyGen. It contains source
planning data and the reproducible local alignment/build scripts. It generates
no replacement voice and has no fake cloud-generation adapter.

Use Python 3.12, FFmpeg/FFprobe, and these Python packages:

```
numpy==2.5.4
soundfile==0.14.0
onnxruntime==1.31.0
kaldi-native-fbank==1.22.4
ctc-segmentation==1.7.5
```

`ctc-segmentation` may need a C compiler during installation. Set `CC=gcc` if
the Python build configuration names an unavailable compiler. Consult the model's
own license before using or redistributing model files; the model is not bundled.

Obtain the official model release linked in `alignment-report.json` and extract
it under `models/` in the package root. Put your unchanged original `voice.mp3`
and `script.txt` in a private local directory. Set these environment variables
to actual local paths, never to a different recording:

```
MEGALITH_AUDIO=/absolute/path/to/voice.mp3
MEGALITH_SCRIPT=/absolute/path/to/script.txt
MEGALITH_MODEL_DIR=/absolute/path/to/sherpa-onnx-nemo-ctc-giga-am-v2-russian-2025-04-19
```

Export those variables in your shell. `MEGALITH_PROJECT_DIR` defaults to the root
above `scripts/`; it can be set if running from a different project layout.

Run, in order:

```
python scripts/align.py
python scripts/build_manifest.py
```

The first step makes a private analysis-only PCM copy and acoustic probability
cache, aligns all supplied text, and writes phrase/word alignment. The second
builds the JSON, CSV, Markdown and review HTML from authored `scripts/scenes.tsv`
and the detailed mechanism cues in `scripts/cues.json`. It validates continuity
of edit boundaries, coverage, source hashes and word preservation. It does not
claim video-generation or rendered-physics validation.

Cache files in `private/` belong only to this exact MP3/model combination. If
working on a different source, create a separate project instead of reusing them.
This project's build intentionally verifies the two supplied file hashes.

The original script is not required just to read the manifest; its exact Russian
excerpts are already included. The original MP3 is not distributed in the package.
