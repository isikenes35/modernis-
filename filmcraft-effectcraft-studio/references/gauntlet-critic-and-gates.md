# The Gauntlet Protocol: Quality Gates & Slop Autopsy

## 1. The Core Law: Builder ≠ Judge

An editor agent cannot self-certify its own work. Human creators and senior directors reject AI edits when the system prints superficial praise (*"the edit looks fantastic and seamless"*) without inspecting the rendered output.

Under the **Gauntlet Protocol**:
1. The **Builder Agent** produces the edit, generates the timeline, and renders the media.
2. The **Judge / Critic** executes automated numerical gates (`audit_render_gates.py`), generates a diagnostic contact sheet (`generate_contact_sheet.py`), and evaluates the visual evidence against strict rejection rules.
3. If any gate fails or a Slop pattern is detected, the edit is rejected and sent back for revisions.

---

## 2. The G0–G5 Quality Gates

| Gate | Name | Pass Criteria | Verification Tool |
| :---: | :--- | :--- | :--- |
| **G0** | **Render Health** | File decodes without error; duration matches expected ($\pm 0.35$s); non-blank frames ($\ge 95\%$ picture); audio stream present and non-silent. | `audit_render_gates.py` (G0 block) |
| **G1** | **Proof Readability** | Any captured UI or code snippet fills $\ge 55\%$ of frame width; on-screen text height is $\ge 4\%$ of frame height ($\ge 43$px in 1080p). Never show a tiny card in an empty void. | Visual inspection on contact sheet |
| **G2** | **No Dead Frames** | No run of more than 3 consecutive flat/motionless frames ($>3$ frames with mean pixel diff $< 0.25$). A scene must breathe with organic Ken Burns drift or continuous motion. | `audit_render_gates.py` (G2 block) |
| **G3** | **End-Card Discipline** | The static, picture-unchanged hold at the end must be $\le 1.4$s (ideally $0.6$s–$1.2$s). The entire final shot must be $\le 25\%$ of total video duration. | `audit_render_gates.py` (G3 block) |
| **G4** | **Single Hero Focus** | Exactly ONE primary focal point per beat. Two panels are permitted only if one is $\ge 2\times$ the area of the other or the camera explicitly tracks between them. | Visual inspection on contact sheet |
| **G5** | **Anti-Slop Compliance** | Zero instances of C1–C7, D1, T1, or V1–V5 Slop patterns. | `audit_render_gates.py` / `lint.mjs` |
| **AUDIO** | **EBU R128 Loudness** | Integrated loudness strictly at $-14.0\text{ LUFS} \pm 1.0\text{ LU}$; True Peak $\le -1.0\text{ dBTP}$ (zero clipping on mobile/social). | `audit_render_gates.py` (ebur128) |

---

## 3. Slop Autopsy: The 25 Rejection Patterns

A film containing any of the following patterns is unfinished and must be corrected:

### A. Page Chrome & HUD Artifacts (C1–C7)
* **C1 (Corner/Edge Labels):** Tiny brand names, category tags, or decorative labels placed in screen corners ($x < 0.2$ or $x > 0.8$, $y < 0.14$ or $y > 0.86$).
* **C2 (Tracked-Caps Labels):** Small uppercase text with exaggerated letter-spacing ($>0.15\text{em}$) acting as artificial "design filler".
* **C3 (Slide/Chapter Counters):** Numbering systems such as `"02 / SPEAK"`, `"01 - THE WAIT"`, `"03 / 05"`, or bare `"01"`.
* **C4 (Production Metadata):** Fake technical readouts: `"1920x1080"`, `"60 FPS"`, `"BPM 120"`, `"TC 00:14:22"`, `"T+1.2s"`.
* **C5 (Monospace Micro-Labels):** Monospace technical font tags floating outside of an actual code editor UI.
* **C6 (Header/Footer Bars):** Artificial hairlines or top/bottom dividing strips imitating web browser chrome.
* **C7 (Kicker Over Headline):** Small category kicker directly stacked above a large headline.

### B. Slide-Deck Layouts (D1)
* **D1 (Corporate Slide Structure):** Left-anchored headline block with a small floating screenshot or device mockup on the right. A promo film is not a Keynote slide.

### C. Kinetic Typography Slop (T1)
* **T1 (Letter-Typed Headlines):** Major headline statements typed out character-by-character with a blinking cursor. Typewriter animation belongs ONLY inside real search inputs or terminal prompts; headlines must arrive as whole words or staggered lines with `softLand`.

### D. Vibe-Coded UI Cards (V1–V5)
* **V1 (Generic Greeting):** Fictitious cards displaying *"Good morning, Sarah"*, *"Welcome back"*.
* **V2 (Label-Dot-Value):** Cards with meaningless metrics: *"Revenue • $12,450"*, *"Tasks • 94%"*.
* **V3 (Status Dot Slop):** Meaningless green/pulsing circles preceding non-status text.
* **V4 (Tailwind Zinc Grey Mud):** Uninspired dark-mode zinc grey palette (`#71717a`, `#52525b`) rather than branded color worlds.
* **V5 (Generic Web Component Cluster):** Surfaces containing multiple generic placeholder components instead of real product captures.

---

## 4. Gauntlet Independent Critic Prompts

When evaluating an edit pass, execute the following inspection battery:

```text
[GAUNTLET INSPECTION BATTERY]
1. LOOK AT THE CONTACT SHEET:
   - Does frame 0 open on an already-moving, complete composition?
   - Is there any dead space where a card floats in a void without backing?
   - Does the product UI fill at least 55% of the frame width?

2. TEST THE SEAMS & TRANSITIONS:
   - Do background camera shots cut under title cards while text is being held? (Rule: NEVER cut background footage under a title card).
   - Are transitions smooth (cross_zoom, push, wipe) or do they exhibit artificial velocity jumping?

3. CHECK THE END HOLD:
   - Does the final lockup card hold steadily for 1.5s–4.0s without exceeding 25% of the film?
   - Did the final hit of the music resolve directly on the lockup impact?

4. RUN NUMERICAL GATES:
   - Execute: python audit_render_gates.py <master.mp4> --expect-duration <planned_s> --strict
   - Record and report exact LUFS, True Peak, and frozen frame counts.
```
