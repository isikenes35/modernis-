# Anti-AI-Slop Editorial Rules, Prohibitions, and Quality Gates

This reference defines the exact diagnostic symptoms of an "AI-generated video edit" and the mathematical, perceptual, and editorial rules required to make FilmCraft sequences look cut by a senior human editor. Synthesized from empirical studies of professional edits in `Tejashmakwana/motionmaxxing` (53 pro films, 4,288 measured moves), `appariciojunior/video-editor-skills` (real-world creator feedback), `browser-use/video-use`, `haidrrrry/claude-remotion-skill`, and `echris6/motion-video-kit`.

## 1. The Anatomy of an "AI Edit" vs. Human Craft

| Dimension | The "AI Slop" Tell (Forbidden) | The Professional Human Standard (Required) |
| :--- | :--- | :--- |
| **Cut Triggers** | Cuts triggered purely by dB silence thresholds, chopping mid-thought into 500+ micro-fragments. | Cuts triggered by semantic phrase boundaries (`transcript.inspect`) and emotional beats. |
| **Cut Padding** | `0ms-10ms` butt-cuts where words collide and scenes slam into each other. | `50ms-150ms` intra-scene padding (`3-5 frames`); `500ms` head / `600ms` tail at scene boundaries. |
| **A/V Sync Relationship** | 100% locked straight cuts where audio and video always start and end on the exact same frame. | 30%-50% split edits (J-cuts and L-cuts) where audio leads or trails picture by `6-15 frames` (`0.25s-0.6s`). |
| **Transitions** | Default `Cross Dissolve`, `Wipe`, or `Zoom` slapped onto every single cut point. | 96% hard cuts motivated by action, eye-trace, or beat; dissolves used only for time/location passage. |
| **Camera & Zoom** | Constant ping-pong zooming on every clip or zooming on a brand-new camera angle; holding a punch-in for 60+ seconds. | New scenes open at `100%` scale. `1.08x-1.15x` punch-ins used only to mask same-angle jump cuts or land a 1-line payoff, then reset on the next cut. |
| **Keyframe Easing** | Linear interpolation (`linear`) on position, scale, and opacity; elements moving at constant robotic velocity. | Monotone cubic / Bezier easing: **Landings decelerate** (`Ease Out`), **Exits accelerate** (`Ease In`). |
| **Graphic Entrances** | Single-property opacity fades (`0% -> 100%`) or growing linearly from `scale: 0`; all lines appearing on the same frame. | Multi-property entrances (`position` + `scale` + `opacity` or decelerating from oversize `1.2x -> 1.0x`), staggered by `3-6 frames`. |
| **Page Chrome & Overlays** | Corner brand tags, fake `02 / 05` counters, decorative corner brackets, progress bars, typewriter carets. | Clean cinematic framing: one focal hero per frame, zero decorative HUD clutter, real vector typography. |
| **Audio Transitions** | Hard zero-crossing digital cuts causing audible clicks/pops at every edit point. | `30ms-50ms` (`1-2 frame`) constant-power audio crossfades on every dialogue cut plus continuous room tone on an underlying track. |
| **Music & SFX** | Flat music volume drowning speech or timid `-25 LUFS` during B-roll; 20 cheesy literal foley whooshes in 15 seconds. | Dynamic contour: `-16 LUFS` on B-roll swelling from the speaker's last word, ducked `-12 to -15 dB` under speech; sparse, pre-aligned subtle SFX. |
| **Color Grading** | Unbalanced camera log or oversaturated orange-and-teal LUT applied at `100%` intensity without checking scopes. | Primary balance first, skin tones locked at `55-70 IRE` on the vectorscope skin-tone line, look LUT/preset dialed to `35%-65%` intensity. |

## 2. Hard Prohibitions (Kesin Yasaklar - Never Violate)

1. **Ban Unfiltered Silence Stripping:** Never run automated pause removal with a single aggressive threshold across an entire timeline without checking the genre. A `0.3s` pause threshold works for a fast coding tutorial clip, but destroys the natural storytelling cadence of a vlog, documentary, or interview.
2. **Ban Cutting Inside Words or Breaths That Carry Emotion:** Never place an In or Out point inside a word (`< 150ms` gap). Preserve intentional sighs, laughs, and reaction beats after punchlines - in human editing, **the reaction IS the beat**.
3. **Ban "Orphan" Punch-Ins:** Never apply a scale change (`110%`) to a clip for a punchline without placing a razor split (`timeline.razor`) after the punchline to return the remainder of the take to `100%` (or cutting to B-roll).
4. **Ban Blind B-Roll Slicing:** Never drop B-roll onto `V2` at random 3-second intervals without inspecting the B-roll frames first (`render_frame` at `~2 fps`). Placing a clip that contains a wild camera whip-pan or lens cap at the tail ruins the edit.
5. **Ban Literal / Cartoonish Foley:** Do not stack literal sound effects on every noun the speaker says (e.g., zipper sounds, cash register dings, cartoon boings, loud jet swooshes on every cut). Limit SFX to at most 1 subtle acoustic event per major visual transition (`~6-8` subtle hits per 20 seconds max).
6. **Ban Audio Normalization on Quiet Clips:** Never run `clip.audioGain` with `normalizeMax` or `normalizeAll` across unselected timeline clips that include room tone, silence, or B-roll ambient tracks - it amplifies noise floor by +30 dB into harsh static.
7. **Ban Caption-Overlay Collisions:** Never place a lower-third title card, callout, or product badge in the bottom `15%` of the frame when caption track `C1` is active at the same timestamp.
8. **Ban Emoji Icons in Titles:** Never use raw system emojis (`🚀`, `🔥`, `✅`) inside `graphics.newText` layers on professional edits. They render as inconsistent platform glyphs that clash with the color grade. Use vector shapes (`graphics.newShape`) or clean typographic markers instead.

## 3. Mandatory Mathematical & Perceptual Rules (Zorunlu Kurallar)

### Rule 1: The Cut Padding & Pause Matrix

- **Intra-Phrase Micro-Cut Padding:** When cutting out a filler word (`um`, `uh`) or stutter mid-sentence, leave `40ms-80ms` (`1-2 frames` at 24/30fps) of padding around the adjacent words so consonants (`p`, `t`, `k`, `s`) are never clipped.
- **Speaker Handoff Air:** In multi-speaker interviews or podcasts, maintain `400ms-600ms` of air between Speaker A finishing and Speaker B starting (unless an interruption is intentional).
- **Scene Boundary Handles:** Start the opening shot of a new scene `0.5s` (`12-15 frames`) before the first spoken word and hold `0.6s-0.8s` (`15-24 frames`) after the final word before cutting to the next scene, stopping before the speaker's hand reaches to turn off the camera.

### Rule 2: J-Cut and L-Cut Split-Edit Mechanics

- **The J-Cut (Audio Leads Video):** Start the incoming clip's audio `6-12 frames` (`0.25s-0.5s`) *before* its video cut appears on screen. Use this when transitioning from B-roll back to A-roll or introducing a new location/speaker - the viewer's ear turns toward the new voice before the eye sees the cut, making the transition invisible.
- **The L-Cut (Video Leads Audio):** Let the outgoing speaker's audio continue for `8-18 frames` (`0.33s-0.75s`) *under* the incoming B-roll or reaction shot, or bring in B-roll `0.5s` *before* the speaker finishes their sentence.
- **Payoff Word Synchronization:** When introducing a B-roll reveal or graphic overlay (`V2` / `V3`) tied to a spoken keyword, find the exact timestamp of the **payoff word** in `transcript.inspect`. Start the visual entrance `reveal_duration` seconds (`~0.35s / 10 frames`) *before* the word so the graphic or B-roll lands in its settled position on the exact frame the payoff word is spoken.

### Rule 3: Measured Motion Physics (The 10-Frame Law)

From frame-by-frame analysis of professional motion design (`motionmaxxing` & `claude-remotion-skill`):

- **Median Move Duration:** `10-12 frames` (`0.33s-0.40s` at 30fps) for sharp UI/title entrances; `18-24 frames` (`0.6s-0.8s`) for calm cinematic titles.
- **Asymmetric Easing:**
  - **Entrances (Landing):** Must decelerate (`Ease Out` / Bezier handle pulled flat at the destination). Objects arrive with energy and settle gently.
  - **Exits (Leaving):** Must accelerate (`Ease In` / Bezier handle flat at the start, steep at the end) and take **half the frames** of the entrance (`~8-10 frames` exit vs `~16-20 frames` entrance).
- **No Zero-Scale Growth:** Never animate `scale` from `0% -> 100%`. Either animate from `88% -> 100%` coupled with `opacity: 0 -> 100%` and a `15px-25px` vertical translation, or decelerate down from oversize (`115% -> 100%`).
- **Stagger Cadence:** When revealing a title + subtitle + badge, offset each layer's start keyframe by `3-6 frames` (`0.1s-0.2s`). Nothing enters on the exact same frame.
- **Rhythm Cycle:** Follow `HIT -> hold (15-20 frames still/micro-drift) -> build -> HIT`. Never leave the screen completely static for more than `3 seconds` (`90 frames`) in fast-paced edits, and never allow more than `3 consecutive dead frames` during an active motion sequence.

### Rule 4: Sound Design & Acoustic Pre-Alignment

- **Transient Pre-Alignment:** Sound effects (whooshes, swells, clicks, risers) have an acoustic attack build before their peak transient. Inspect or calculate the attack offset (first sample above `-30 dBFS` to peak) and place the audio clip on `A3` so its **peak transient** aligns with the visual cut frame - meaning the clip starts `0.15s-0.40s` *before* the cut point.
- **Music Swell on B-Roll Transitions:** When transitioning from talking-head dialogue into a B-roll sequence, begin ramping the music track (`A2`) up from `-28 LUFS` toward `-16 LUFS` during the last `0.4s` of the speaker's final word, not after the speaker has already stopped talking.
- **Clean Music Endings:** Never let a music track get chopped off abruptly at the end of the sequence or fade out 25 seconds early. Back-time the music clip so its final chord hits the end card, or craft a deliberate `1.5s-2.5s` exponential fade-out into a final acoustic stinger.

### Rule 5: Caption Readability & Linguistic Cleanup

- **Linguistic Polish:** Remove stutters (`"pro-product"` -> `"product"`), aborted words (`"es--"`), and non-lexical fillers (`"uh"`, `"ummm"`), while preserving the speaker's authentic vocabulary and tone. Beware of false-positive filler stripping (e.g., short real words in Turkish like `"o"`, `"ve"`, `"ki"`, `"de"`, `"ya"` must never be stripped by naive regexes).
- **Geometry & Timing:**
  - Single line preferred (`max 42 characters`; allow up to `50` only to avoid leaving a single short word orphaned on a next cue).
  - Break cues at natural pauses `>= 0.6s`, at sentence boundaries, or after `3.2s` max duration.
  - Minimum on-screen duration: `0.9s` (unless ultra-fast 2-word social hook mode is explicitly requested, where minimum is `0.35s`).
  - Trail the last spoken word by `+0.25s`, never overlapping the next cue.

## 4. The 6 Quality Gates (Mandatory Self-Evaluation Before Delivery)

Every edit must pass Gates G0 through G5 before you report completion to the user:

- **Gate G0 (Integrity & Online Check):** `sequence_inspect` and `media.status` confirm zero offline media items (`offlineMedia: []`), sequence frame rate and resolution match the target delivery spec, and total duration matches the planned target.
- **Gate G1 (Cut Boundary & Flash-Frame Audit):** Sample `render_frame` around cut boundaries and verify zero 1-frame black gaps, zero unintended jump-cuts without scale/B-roll mitigation, and zero mid-word audio truncations.
- **Gate G2 (Visual Salience & Safe Zones):** Inspect rendered frames containing graphics (`V3`) and captions (`C1`). Verify that:
  - Text is never occluded by an overlay above it.
  - Critical content stays inside the central `75%` vertical safe zone for `9:16` vertical videos (since TikTok/Reels/Shorts UI covers the top `10%` and bottom `15%`) or standard `90%` title-safe area for `16:9`.
  - Only **one hero focal point** dominates each frame.
- **Gate G3 (Color & Broadcast Scopes Gate):** Call `scopes.read` on graded clips. Confirm luma waveform sits cleanly within `0-100 IRE` (blacks anchored at `2-5 IRE`, highlights rolled off below `98 IRE`) and skin tones align with the vectorscope skin-tone axis without unnatural green/magenta casts.
- **Gate G4 (Loudness & Mix Balance Gate):** Verify integrated loudness matches the platform target (`-14 LUFS` / `-1.0 dBTP` true peak for web/social; `-23 LUFS` for broadcast), dialogue peaks sit `-6 to -3 dBFS`, and music sits at least `12-15 dB` below speech during dialogue sections.
- **Gate G5 (Anti-Slop Lint Gate):** Visually confirm zero "AI Page Chrome" (no corner counters, no fake timecodes, no linear-interpolated animations, no back-to-back cross-dissolves, and end-card hold is `<= 1.4s`).
