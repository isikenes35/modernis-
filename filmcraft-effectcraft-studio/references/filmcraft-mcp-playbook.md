# FilmCraft MCP & Engine Architecture Playbook

## 1. Engine & MCP Connection Architecture

FilmCraft operates on a unified command engine architecture where all UI actions, keyboard shortcuts, CLI invocations, and MCP tool calls execute through the same underlying engine commands with stable IDs and strict JSON schemas.

### Connection Modes
| Mode | Command Line Flag | Best For | Window Requirement |
| :--- | :--- | :--- | :--- |
| **Live GUI Bridge** | `filmcraft --control 9876`<br>`filmcraft-cli --bridge 127.0.0.1:9876 mcp` | Real-time agent collaboration, live timeline playback, UI inspection, and visual feedback | Yes (Desktop application running) |
| **Headless CLI / CI** | `filmcraft-cli mcp`<br>`filmcraft-cli exec <command> <json>` | Batch processing, headless render farms, automated Quality Gate audits | No (Runs in headless background process) |

### Control Channel Security & Authentication
* **Default Port:** `127.0.0.1:9876`
* **Security Token:** Environment variable `FILMCRAFT_CONTROL_TOKEN` (64-character hex string). Every request across the TCP bridge or WebSocket connection must provide this token in the handshake header or `--bridge` authentication.

---

## 2. Temporal Precision: Exact Integer Tick Mathematics

FilmCraft eliminates floating-point rounding drift by representing all media times, cut boundaries, keyframes, and durations using exact integer 64-bit ticks:

$$\text{Ticks per Second} = 254,016,000,000$$

This fundamental constant is divisible by all standard broadcast and web frame rates ($23.976, 24.0, 25.0, 29.97, 30.0, 50.0, 59.94, 60.0, 120.0$), ensuring zero rounding errors over long sequences:

| Frame Rate | Ticks per Frame | Mathematical Formula |
| :--- | :--- | :--- |
| **60.0 fps** | `4,233,600,000` | $254,016,000,000 / 60$ |
| **30.0 fps** | `8,467,200,000` | $254,016,000,000 / 30$ |
| **24.0 fps** | `10,584,000,000` | $254,016,000,000 / 24$ |
| **25.0 fps (PAL)** | `10,160,640,000` | $254,016,000,000 / 25$ |
| **23.976 fps** | `10,594,594,594` | Exact NTSC drop/non-drop conversion |

```python
# Exact tick conversion helpers
FRAME_60FPS = 4233600000
TICKS_PER_SEC = 254016000000

def seconds_to_ticks(sec: float) -> int:
    return round(sec * TICKS_PER_SEC)

def frames_to_ticks(frames: int, fps: float = 60.0) -> int:
    return round(frames * (TICKS_PER_SEC / fps))
```

---

## 3. Core Engine Commands & Schemas

### Project & Bin Management
* `file.newProject {name: string}`: Initializes project state.
* `file.newBin {name: string, parent?: string}`: Creates logical media organization bins (`01_Footage`, `02_Logos_Gfx`, `03_Audio_Music`).
* `file.import {paths: string[], bin?: string}`: Imports media files.
* `file.newSequence {name, width, height, fps, sampleRate, video, audio, mix}`: Initializes timeline sequence.
* `file.save / file.saveAs {path: string}`: Commits state to `.fcproj` on disk.

### Timeline Editing & Track Layout
* `timeline.place`: Inserts clip onto track.
  ```json
  {
    "id": "timeline.place",
    "params": {
      "item": 1,
      "track": "V1",
      "time": 0,
      "sourceIn": 254016000000,
      "duration": 508032000000,
      "video": true,
      "audio": false
    }
  }
  ```
* Standard Track Allocation:
  * `V1`: Primary narrative B-roll & gimbal drone footage (continuous, 0 gaps).
  * `V2`: Lower thirds, secondary overlays, sonar rings, badges.
  * `V3`: Brand logos, vector map pins, alpha overlays.
  * `V4`: Vector kinetic typography & accent graphic geometry.
  * `V5`: Secondary badges & sponsor lockups.
  * `A1`: Main music bed (stereo master).
  * `A2`: Primary atmosphere, whoosh transitions, cinematic impacts.
  * `A3`: Tactile UI clicks, map drops, and sub-bass impacts.

---

## 4. 32-Bit Floating Point Lumetri Color Grading

FilmCraft applies cinema-grade 32-bit floating point color operations:
* `effects.apply {clips: [...], effect: "lumetri"}`
* Core Parameters:
  * `temperature` (Kelvin warm/cool balance: -100 to +100)
  * `tint` (Green/Magenta balance: -100 to +100)
  * `contrast` (0.0 to 100.0)
  * `highlights` (-100.0 to +100.0)
  * `shadows` (-100.0 to +100.0)
  * `whites` & `blacks` (-100.0 to +100.0)
  * `saturation` (0.0 to 200.0, default 100.0)
  * `curves_on` (true/false) & `curve_luma` (`[[0.0, 0.02], [0.25, 0.22], [0.75, 0.81], [1.0, 0.98]]`)
  * `vignette_amount` (-1.0 to 1.0), `vignette_midpoint` (0-100), `vignette_feather` (0-100)
* **3D LUT Integration (`.cube`):**
  * Support for industry-standard 17x17x17, 33x33x33, and 65x65x65 `.cube` files.
  * `input_lut`: Log to Rec.709 conversion.
  * `creative_lut`: Creative film look applied at 30%–60% intensity.

---

## 5. Blend Modes & Motion Integration

FilmCraft supports 26 full blending modes matching Photoshop and Premiere Pro parity:
* Normal, Dissolve
* Darken, Multiply, Color Burn, Linear Burn, Darker Color
* Lighten, Screen, Color Dodge, Linear Dodge (Add), Lighter Color
* Overlay, Soft Light, Hard Light, Vivid Light, Linear Light, Pin Light, Hard Mix
* Difference, Exclusion, Subtract, Divide
* Hue, Saturation, Color, Luminosity

When using CinePacks light leaks or film burns on `V2`/`V3`, set `blendMode: "screen"` or `"add"`.

---

## 6. Premiere Pro `.prfpset` Preset Import Workflow

FilmCraft seamlessly imports native Adobe Premiere Pro `.prfpset` preset packages:
1. Copy `.prfpset` files into FilmCraft user preset directory:
   * Windows: `%APPDATA%\ArtCraft\FilmCraft\Effect Presets\`
   * macOS: `~/Library/Application Support/ArtCraft/FilmCraft/Effect Presets/`
2. Run `effects.importPreset {path: "..."}` via CLI or GUI (`Effects ▸ Presets`).
3. Presets containing Lumetri curves, motion ramps, or audio strips appear directly under `effects.list`.
