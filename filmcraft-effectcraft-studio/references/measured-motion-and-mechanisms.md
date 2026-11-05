# Measured Motion & Reusable Motion Mechanisms

## 1. Motionmaxxing: The 12 Measured Eases

Empirical analysis of 53 human-made, award-winning commercial films (~4,300 measured motion events) reveals that professional motion design follows strict physical laws rather than generic software presets:

### Fundamental Craft Laws of Timing & Velocity

1. **Entries Decelerate (58% Ease-Out), Exits Accelerate (37% Ease-In):**
   * When an element arrives on screen to be read or recognized, 50%–60% of its spatial travel occurs within the first 10%–20% of the movement. The remaining time is spent in a long, asymptotic deceleration tail.
   * Conversely, when an element departs, it leaves with sharp acceleration (`accelExit`, `crashOut`). The eye should never wait for an exiting element to crawl off-screen.
2. **Median Motion Durations:**
   * **Overall median move:** `10 frames (0.33s at 30fps / 0.17s at 60fps)`.
   * **Headline & card entries:** `11–12 frames (0.37s–0.40s)`.
   * **Opacity fades:** `6 frames (0.20s)`.
   * **Defocus / Gaussian blur ramps:** `7–8 frames (0.23s–0.27s)`.
   * **Whip pans & camera snaps:** `7 frames (0.23s)`.
3. **Logos and Elements Never Grow from 0%:**
   * An element scaling up from 0% looks amateurish ("PowerPoint pop").
   * Professional motion arrives by:
     * Decelerating from oversize (e.g., logo enters at `3.5x` scale with `snapSettle`, dropping into place).
     * Entering from outside the camera frame at high velocity.
     * Mask unmasking (`Trim Paths` or linear wipe mask).
     * Optical defocus to focus.

---

### The 12 Measured Eases Velocity Matrix

| Curve Name | Frames (30fps) | EffectCraft Out (Inf / Spd) | EffectCraft In (Inf / Spd) | Cubic Bezier | Primary Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`snapSettle`** | 11f (0.37s) | `85.0% / 0.0` | `15.0% / 0.1` | `(0.12, 0.54, 0.25, 1.0)` | Primary hero arrival (54% travel in first 10% time) |
| **`softLand`** | 12f (0.40s) | `72.0% / 0.0` | `28.0% / 0.0` | `(0.16, 1.0, 0.30, 1.0)` | Typography, staggered lines, secondary UI cards |
| **`crashIn`** | 10f (0.33s) | `78.0% / 0.0` | `18.0% / 2.8` | `(0.19, 1.18, 0.22, 1.0)` | High-energy tactile stamp, map pin drop, badges |
| **`whip`** | 7f (0.23s) | `90.0% / 0.0` | `10.0% / 0.0` | `(0.08, 0.85, 0.15, 1.0)` | Whip pan transitions, fast lateral camera sweeps |
| **`glide`** | 10f (0.33s) | `55.0% / 0.0` | `35.0% / 0.0` | `(0.25, 0.75, 0.45, 1.0)` | Subtle positional reframing during active reading |
| **`cruise`** | 9f (0.30s) | `33.3% / 1.0` | `33.3% / 1.0` | `linear` | Background drift, Ken Burns scale (100% -> 104%) |
| **`softInOut`** | 9f (0.30s) | `42.0% / 0.1` | `42.0% / 0.1` | `(0.42, 0.0, 0.58, 1.0)` | Opacity crossfades, defocus blur transitions |
| **`popOver`** | 15f (0.50s) | `65.0% / 0.0` | `25.0% / 1.6` | `(0.34, 1.25, 0.64, 1.0)` | Playful toggle, interactive micro-overshoot |
| **`bounceHard`** | 22f (0.73s) | `50.0% / 0.0` | `20.0% / 3.2` | `(0.22, 1.48, 0.38, 1.0)` | Cartoon spring (use at most once per film) |
| **`gentleIn`** | 9f (0.30s) | `20.0% / 0.0` | `65.0% / 1.8` | `(0.45, 0.05, 0.70, 0.40)` | Anticipation before transition |
| **`accelExit`** | 13f (0.43s) | `15.0% / 0.0` | `82.0% / 2.6` | `(0.55, 0.0, 0.90, 0.35)` | Standard exit for title cards, panels, and text |
| **`crashOut`** | 17f (0.57s) | `10.0% / 0.0` | `92.0% / 4.0` | `(0.70, 0.0, 1.0, 0.20)` | Hard acceleration into a cut or shutter blackout |

---

## 2. Motion Video Kit: The 16 Reusable Motion Mechanisms

Distilled from 28 high-end launch films (Apple, Stripe, Linear, Replit, Wonder, Bolt):

| # | Mechanism Name | Description & Visual Behavior | Implementation Recipe |
| :-: | :--- | :--- | :--- |
| **1** | **Foreground Fly-Through** | Headline, logo, or card scales rapidly toward camera (`scale: 100% -> 450%`), blurring as edges stretch, revealing pre-positioned next scene beneath. | FilmCraft: `effects.setParam {param: "scale", value: 450.0}` + `directional_blur`. |
| **2** | **Logo-as-Portal** | The negative space in a brand mark expands until the inner boundary fills the screen, forming the matte for Scene B. | EffectCraft: Shape Layer mask expansion with `snapSettle`. |
| **3** | **Selection ➔ Expansion** | A small UI thumbnail or card expands cleanly to become the full-screen canvas for the subsequent beat. | FilmCraft: Match-cut position/scale handoff across cut seam. |
| **4** | **Materializing Result** | A container shell lands first (frame 0–12), then internal elements, data charts, and text cascade in sequence. | Staggered range selectors on `V4` with 3-frame offsets. |
| **5** | **Persistent Rails** | Structural layout lines or vector rails remain fixed while text and content swap out around them. | Vector geometry maintained on `V2` while `V4` content updates. |
| **6** | **Continuous Canvas** | Camera glides smoothly across one large continuous layout. Focused element stays sharp; surrounding items blur. | Camera pan with Camera Lens Blur depth map. |
| **7** | **Artifact Ring** | Orbiting cloud of supporting icons/metrics orbiting a central anchor statement. | EffectCraft 3D Null orbit with child parenting. |
| **8** | **Card Stack / Fan** | Multiple cards slide in, stack, and fan out; one card lifts forward to lead the narrative. | Z-space separation (50px each) + Y-rotation offsets. |
| **9** | **Perspective Fold** | 3D panel folds down into a luminous horizontal seam; new panel unrolls upward from the seam. | 3D Layer X-rotation (`-90° -> 0°`) with anchor at top edge. |
| **10** | **Exploded Layers** | Hardware device or UI dashboard separates into floating 3D layers along Z-axis, then reassembles. | Z-position keyframes (`0px -> -250px -> -500px`) with Depth of Field. |
| **11** | **Registered Decomposition** | A source chart or document separates cleanly into categorical buckets while maintaining visual anchor. | EffectCraft Shape Morphing & Position separation. |
| **12** | **Wall ➔ One Actor** | Overwhelming grid of data shrinks or recedes into background darkness, spotlighting one clear winning metric. | Background exposure dip (`-1.2 EV`) + spotlight mask on hero. |
| **13** | **Carousel Emphasis** | 3D cylinder/carousel rotates; central item scales to 100% and illuminates while neighbors scale to 70% and dim. | 3D Layer Y-rotation loop with distance-based opacity expression. |
| **14** | **Colour-Field Takeover** | Organic gradient cloud or blur wash sweeps across the screen to signal a major narrative chapter change. | 4-Color Gradient on Adjustment Layer with softInOut dissolve. |
| **15** | **Tile Wipe** | Symmetrical checkerboard or vertical ribbon wipe revealing the next scene with tactile snappiness. | Linear Wipe effect with multi-strip angle offsets. |
| **16** | **Request ➔ Picker ➔ Result** | Interactive dialogue: user input triggers cursor click, dropdown sheet opens, item is selected, state confirms. | Cursor position + click scale squash (90% for 3 frames) + state check. |
