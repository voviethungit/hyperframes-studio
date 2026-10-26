# QA report — История в Палочках

Video: Как люди тушили пожары до пожарных машин?

| Check | Result |
|---|---|
| Source narration | 1697.436735 s |
| Final video | 1697.436735 s — 28:17.436735 |
| Resolution / ratio | 1920×1080 / 16:9 |
| Nominal frame rate | 25 fps; 42,436 frames |
| Final presentation interval | 36.735 ms, to meet the original MP3 endpoint |
| Semantic scenes | 256 |
| Narration unchanged | PASS — encoded MP3 packet payload and decoded PCM both identical |
| Narration re-encoded, replaced or stretched | No |
| Missing timeline coverage | None |
| Black gaps | None found by all-frame black detection |
| Full video and audio decode | PASS |
| Scene composition inspection | 256 scenes, zero JavaScript errors |
| Continuity | PASS within the review scope below |
| Style lock | PASS within the review scope below |
| Export | PASS |
| HeyGen generation | Not used; authenticated HeyGen capability unavailable |

## Review scope

The entire narration has acoustically aligned semantic coverage. Every scene midpoint was visually inspected. Motion was sampled at 20%, 50%, and 80% of each scene. Key bucket, pump, ladder, hose, rescue and demolition actions received additional phase checks. The complete exported file was decoded and checked for black intervals.

Continuity uses deterministic sequence time, fixed role colors, consistent geography and stable mechanism positions. Style uses 13 generated cartoon environment assets and original solid-body 2D character animation. This is a locally animated finished film, not a HeyGen-generated film. A continuous real-time human viewing of all 28 minutes was not performed; sampled inspection cannot guarantee every intermediate pose. Acoustic alignment is model-derived on a 40 ms grid, not sample-accurate human phonetic annotation. Historical statements follow the supplied script and simplified illustrative reconstructions.

## Integrity

- Original MP3 SHA256: `ace6676768923dc3d6727f14787a1a8ce8d840796122b89abc802f346a227050`
- Final MP4 SHA256: `2ab462f1d5c38f7278a757b5a9e32eea9cdbbc7a9bcfab6dedf9aecf4e3d57a0`
- Encoded narration payload SHA256: `5b404dc8dad77c08de809b5f1354188277d98f6a71cce07143f7e922bf8f7d24`
- File size: 102,431,462 bytes.

## Browser playback

PASS — final MP4 metadata opens at 1920×1080 and 1697.436735 seconds, eight timeline seeks complete without decoder errors, and playback advances normally. The file was opened as a browser Blob to test the finished bytes directly. See `browser-playback-check.json`.
