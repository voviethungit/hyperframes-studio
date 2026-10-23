# Production rules and capability status

Channel: **История в Палочках**  
Topic: **Как люди поднимали многотонные камни без современной техники?**

This is the production manifest accompanying the **completed local animated video**.
Every HeyGen clip ID is deliberately null. The finished video uses local Canvas 2D / FFmpeg animation. No HeyGen clip, endpoint, parameter or authenticated generation is claimed.

## HeyGen capability status (local production completed)

**Callable, authenticated HeyGen visual clip generation.**

The installed HyperFrames plugin supplies HTML-animation skills. It does not
expose a HeyGen visual-generation MCP tool in this session. Available tool names
and descriptions were inspected; no HeyGen generation or browser tool exists.
The local HyperFrames authentication check returned `Not signed in to HeyGen`.
HeyGen API/access-token environment variables were absent. Local FFmpeg editing
and acoustic analysis are available; they do not supply HeyGen visual generation.
No unsupported API call was attempted. Logging in to a voice/music helper alone
must not be treated as proof that a visual-generation API is available.

The initial fallback was completed, and the user subsequently requested the finished movie. A complete local animated production now accompanies it: a continuous manifest for
the entire master, with real acoustic alignment, English actions, Russian source
excerpts, exact numeric edit boundaries, and previous/next continuity notes.

## Audio lock

- Actual uploaded files are `voice.mp3` and `script.txt`; the longer Russian
  filenames in the brief are aliases, not additional missing uploads.
- Original MP3 SHA-256:
  `9a02ea1618ce6a0caab59a0e086e8e7f270c571d807b53c750ff0fc980b3decf`.
- Original script SHA-256:
  `470685d9c6bd4fdd570a67ae8f6b39ea45b844f4b789b50cc5c86469c96f659d`.
- Original MP3 container duration: **1825.410612 s**.
- The requested 1825.410 s differs by only 0.000612 s. Do not shorten the master
  to eliminate that difference. Final visual endpoint follows the real source.
- The 16 kHz gapless analysis copy decodes to 1825.398625 s, reflecting MP3
  encoder-delay/padding metadata. It is for analysis only, never the final audio.
- No new voice, lip sync, additional spoken dialogue, subtitles or music.
- Use the original narration unchanged at 1.0x from timeline zero. Retain its
  source as the immutable audio asset. Do not use the ASR transcript as a new script.
- A fixed-fps frame grid cannot in general end at an arbitrary MP3 microsecond.
  Use a final shortened presentation interval or appropriate container trim while
  keeping every audio sample and narration speed unchanged. Verify the finished
  export's real timestamps; do not claim exact duration from frame count alone.

## Acoustic alignment and its limits

The entire MP3 was decoded for analysis, measured in 10 ms RMS-energy windows,
and passed through the Russian GigaAM v2 CTC model. Inference uses real 64-bin
filterbank features, contextual overlapping windows and a consistent 40 ms
acoustic grid. Windowing is an inference detail, not the scene segmentation.

CTC dynamic programming aligns the supplied Russian text to the acoustic frame
probabilities. A real-space token is used between phrases; monotonic character
peak refinement avoids attributing leading vowels to preceding pauses. Word and
phrase timings are derived from those acoustic positions, **not** character-count
or words-per-minute interpolation. Semantic shot boundaries were authored against
the content and then placed at the measured phrase/word starts.

This is model-based alignment, not human listening verification of each sound.
Four scene flags identify three weak CTC words and the mixed-language word
`fascinates` at approximately 21:37. The original word and narration are preserved;
the phonetic surrogate exists only in the alignment input. See the exact flags
in `alignment-report.json` or the review page. The normalized ASR word sequence
match ratio is a diagnostic, not a calibrated accuracy score or word error rate.

The first visual starts at zero; the last continues through the original MP3's
container endpoint. Pauses belong to an evolving current scene, never a blank gap.
Readable timecodes have millisecond precision; numeric seconds retain the actual
container endpoint. Acoustic estimates themselves have 40 ms resolution.

## One coherent drawing language

- Canvas: horizontal **1920×1080**, 16:9. No vertical crop or letterboxed footage.
- Warm light ground `#F4ECD7`; dark ink `#253235`; round head fill `#FFFEF8`.
- Clothing accents: terracotta `#D46B3D`, blue `#3B84A0`, ochre `#E4AE44`,
  sage `#7F9B70`, muted plum `#8D6B8B`. Earth and stone stay subdued so hands,
  rope, contact edges and supports remain easy to read.
- Black clean stick bodies and limbs with round pale heads; strong readable poses.
  Simple cartoon hands grip objects. Clothing is a small colored shape over the
  stick skeleton. No fully realistic bodies or photorealistic faces.
- Clear eyes, brows and small mouths express effort or curiosity. Mouths rest
  closed unless a non-speaking expression needs an open mouth. No speech animation.
- Simple foreground, midground and background depth. Consistent line weight;
  at 1080p, approximately 6–10 px for primary outlines, less for detail.
- No 3D, anime, painterly inserts, random bounce, idle waving or stock history B-roll.
- No readable writing generated into a scene, no fake inscriptions or logos.
  The sole planned overlay is `Возможная реконструкция` on selected uncertain
  reconstructions, added cleanly in editing. It is not an automatic subtitle.

## Planned character references, not generated assets

For each culture, create a separate reference crew before generation. Maintain
the same reference within a continuous example. These are **planning keys**;
they are not existing HeyGen asset IDs, seeds, or accepted reference images.

| Crew role | Identity anchor | Stable task in detailed demonstrations |
| --- | --- | --- |
| 01 | Tall; terracotta clothing accent | Long-arm lever operator / front hauler |
| 02 | Shorter; blue clothing accent or headband | Packing-board and chock handler |
| 03 | Ochre clothing accent | Second lever or rope handler |
| 04 | Sage clothing accent | Road preparation / front roller carrier |
| 05 | Muted plum accent; short beard where appropriate | Rear roller carrier / guide line |
| 06 | Neutral clothing; distinctive cap where appropriate | Foreman, outside the load path |

Use culture-specific prefixes for planned reference keys: `D` neutral mechanism
demonstrations, `E` Egypt, `B` prehistoric Britain, `G` Greece, `R` Rome, `I` Inca,
`M` medieval Europe, `X` modern experimental reconstruction. Egyptian accents
belong on linen kilts/waistbands, not Greek tunics. British clothing is simplified
hide/woven material; Inca clothing uses woven tunics/headbands; medieval crews
use period tunics and caps. No modern helmets or construction wear in old scenes.

A six-person foreground team may stand for a larger labor operation. Extra
workers must be visible in the initial wide shot or enter from an established
location. Never duplicate or remove people between adjoining shots. A foreman
signals with hands rather than speaking. Do not infer enslavement from worker
costumes or from the Russian script's job-title list.

## Load, tool and location continuity

Object names inside actions/end states, such as H1, D3, S3, J1, JS1 and O1, are
logical continuity keys. Treat them as scoped to their named sequence. They do
not indicate existing generated assets. The manifest's sequence return notes
identify which earlier supported state must be resumed after an insert.

- Keep screen-right as the forward haul direction. A changed direction needs a
  new wide establishment, never a mirror flip that changes rope or worker positions.
- A sledge remains under its load until an explicit supported transfer removes it.
- Load-attachment points, knots, hauling lines and guide lines persist.
- Supports stay beneath the load until they are visibly unloaded and carried out.
- Rollers must first be placed, contact both ground and runners, rotate, become
  fully free at the rear, then be carried around the visible side to the front.
- A lever rotates around a seated fulcrum. First lift, then insert the support,
  then release the force, then reset. Never reverse this sequence.
- A ramp stays present throughout the same haul and final placement. Remove it
  only after the stone has been seated, using an explicit later action.
- Wet sand compacts after water is applied and reduces resistance; no magic glide.
- Every pulley is supported. Draw the full rope path and actual supporting legs.
  A fixed pulley changes direction; a two-leg movable rig gives a distance/force
  tradeoff. Rope cannot intersect stone, bodies or unsupported empty bends.
- Capstan rotation winds rope; the load responds directly. Avoid spinning a drum
  while the rope or load remains inexplicably disconnected from it.
- Obelisk O1 pivots from a supported horizontal/inclined state into a prepared
  socket; butt enters first, shaft rises gradually, counter-ropes check overrun.
  It is a plausible reconstruction, not a certified exact ancient procedure.
- The J1 end-to-end journey keeps its chipped upper-right corner, sledge JS1,
  rope cradle and crew from quarry separation to final supported placement.

## Historical separation and uncertainty

Egypt: Nile/desert, linen kilts, local quarry and barges, no classical or Gothic
architecture. Show the bronze-tool example when the script lists bronze or iron;
do not insert later iron equipment into the Egyptian vignette.

Britain: chalk grassland, rough standing stones and simple prehistoric clothing.
Water movement is an explicit possible reconstruction, not proof of a known
Stonehenge journey. Do not imply the bluestones and sarsens all share one route.

Greece/Rome: classical temple or harbor architecture, appropriate tunics, braced
timber lifting rigs for manageable drums and blocks. Do not use that rig as an
unsupported explanation for every giant prehistoric or Egyptian monolith.

Inca: Andes, appropriate woven clothing and polygonal stone fitting. No routine
wheeled transport, modern iron equipment or magical melting/laser-cut stone.
Human traction and small supported corrections are plausible visual explanations,
not a claim that one exact mechanism is archaeologically proved for every wall.

Medieval Europe: Gothic masonry, timber scaffold, treadwheel/axle/drum/sheave
mechanism and period iron fittings. The iron smithy belongs here, not in the
earlier Egyptian quarry scene. Weather and preparation changes use explicit time
passage, not a live load suddenly standing in a different season.

The script's wedge expansion, thermal cracking, precise pyramid ramp layouts,
monolith raising and transport alternatives require care. Present them as
material-dependent examples or plausible reconstructions, never universal facts.
Keep uncertain layouts in separate views or use the listed reconstruction overlay.
The script itself is not independently rewritten or certified as a scholarly source.

## Real generation, continuation and export when capability exists

1. Discover the provider's actual schema, clip limits and available reference/
   continuation controls. Do not invent endpoints, parameters, seeds or quotas.
2. Create and accept the culture-specific crew/environment/load reference assets.
   Replace null asset IDs only after receiving actual returned identifiers.
3. Generate each manifest scene with its timed narration cues, state-in, action
   and state-out. Split a long semantic beat only if the real tool requires it.
4. For continuation clips, use the prior accepted final frame/reference state
   where supported. Never restart the action, refill a removed roller, switch
   hands, swap costumes or place an already raised stone back on the ground.
5. Inspect every clip's anatomy, contact geometry, ropes, historical environment
   and meaningful movement. Reject false physics or drift before assembly.
6. Place accepted clips against the original master. Extend a short clip with
   meaningful continuation or a motivated camera detail; do not stretch the voice.
7. Keep SFX off by default. If deliberately used later, keep them well below every
   spoken word and avoid loud loops. No additional dialogue or automatic subtitles.
8. Inspect the entire assembled timeline, beginning, all joins and final frame;
   verify source-audio preservation and exact export endpoint. Full-file decoding, exact endpoint, original-audio hash equality, all-scene frame review and motion checks have now been completed for the local movie. See `final-video-check.json`.

The current package makes no claim that HeyGen accepts this JSON directly. It is
an editorial production manifest, with a schema chosen for review and assembly.
