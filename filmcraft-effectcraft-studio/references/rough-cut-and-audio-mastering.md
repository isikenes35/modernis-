# Rough-Cut & Audio Mastering Engineering Guide

## 1. Intelligent Rough-Cut: Retakes, False-Starts & Editor Notes

Based on proven editorial algorithms from professional talking-head and documentary workflows (`appariciojunior/video-editor-skills`):

### The Retake Selection Hierarchy
1. **Always Keep the Last Complete Take:**
   * When a speaker repeats a sentence or paragraph multiple times, the final take almost invariably represents their intended phrasing, energy, and inflection.
   * Discard trailing takes that lost momentum midway through the thought.
2. **Eliminate False Starts & Restart Cues:**
   * Automatically detect and strip false starts (incomplete phrases abandoned after 2–4 words).
   * Cut the restart cue and self-admonition ("let me do that again", "wait, sorry", laughter, coughing).
3. **Automated Spoken Editor Note Detection (`transcript.inspect`):**
   * Speakers frequently speak directly to the post-production team: *"cut here"*, *"roll the screen recording now"*, *"I'll repeat from the beginning"*.
   * Scan speech transcripts for editor cues. Slice out the spoken note and automatically place a timeline marker with a note on the join seam.
4. **Natural Rhythm & Filler Protection:**
   * Do not cut fillers that would create an unnatural visual jump cut (a head jerk or eye shift).
   * In languages like Turkish or Portuguese, words like *"şey"*, *"yani"*, *"tipo"*, *"então"* often function as conversational pacing anchors. Removing them aggressively produces artificial, stuttered speech.
5. **Scene Boundary Breathing Room:**
   * Never cut immediately on the first phoneme or hard against the last syllable.
   * **In-pad:** Preserve `0.4s–0.5s` of room tone before the first word lands.
   * **Out-pad:** Preserve `0.5s–0.7s` of reaction time after the final word before cutting to B-roll.

---

## 2. Voice Restoration & Parametric EQ Recipes

When source dialogue suffers from muffling ("underwater" covered mic) or room resonance:

```mermaid
graph LR
    A[Raw Muffled Audio] --> B[High-Pass 80-100Hz]
    B --> C[Parametric Notch 280Hz -3.5dB]
    C --> D[Presence Boost 3.5-4.5kHz +2.8dB]
    D --> E[Air Shelf 10kHz +1.5dB]
    E --> F[Pristine Dialogue Track]
```

### The 5-Band Diagnostic EQ Formula

| Band | Filter Type | Frequency Range | Q Factor | Gain Adjustment | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Sub Rumble** | High-Pass (18 dB/oct) | `80 Hz – 100 Hz` | 0.707 | Cut completely | Removes air conditioner rumble, mic-stand thumps, handling noise. |
| **2. Boxy Mud** | Bell / Parametric | `250 Hz – 350 Hz` | 1.8 | `-3.0 dB to -4.5 dB` | Removes hollow "cardboard box" resonance common in small untreated rooms. |
| **3. Harsh Resonance**| Bell / Parametric | `1.2 kHz – 1.8 kHz` | 2.5 | `-1.5 dB to -2.0 dB` | Tames nasal honk and phone-speaker harshness. |
| **4. Speech Clarity** | Bell / Parametric | `3.2 kHz – 4.8 kHz` | 1.0 (Wide) | `+2.5 dB to +3.5 dB` | Restores consonant intelligibility (t, k, s, p) from muffled/covered microphones. |
| **5. Air & Sheen** | High-Shelf | `10.0 kHz – 12.0 kHz`| 0.707 | `+1.5 dB to +2.0 dB` | Adds open, modern podcast/broadcast presence. |

---

## 3. SFX Softening & Acoustic Staging

1. **Avoid Literal Foley Slop:**
   * Avoid cartoonish sound effects (literal zipper sounds, comic whooshes, generic mouse click SFX).
   * Use warm, tactile acoustic elements:
     * Deep cinema sub drops (35Hz–70Hz) for final card lockups.
     * Soft untuned broadband whooshes (pink-noise filtered through 200Hz–1200Hz bandpass).
     * Tactile wood/felt impacts for map pin drops and UI button selections.
2. **Pre-Roll Silence Before Impact:**
   * For maximum perceived impact, enforce 40ms–80ms of silence on secondary SFX beds immediately before a primary downbeat hits.

---

## 4. Musical Back-Timing Mathematics

Never arbitrarily chop a music track and fade it out mid-bar. A high-end film aligns the track's **natural resolving final hit** with the visual arrival of the end card:

### Mathematical Back-Timing Formula

$$\text{sourceIn} = \text{hit}_{\text{source}} - \text{card}_{\text{timeline}}$$

$$\text{sourceOut} = \text{sourceIn} + \text{film}_{\text{duration}}$$

* $\text{hit}_{\text{source}}$: The timestamp in seconds of the source track's final resolving downbeat (detected via `backtime_music_calc.py --list-hits`).
* $\text{card}_{\text{timeline}}$: The timestamp in seconds where the visual end card or lockup lands.

### Varispeed Tempo Matching
When matching the music track's tempo grid to the visual cut cadence:

$$\text{Ratio} = \frac{\text{BPM}_{\text{target}}}{\text{BPM}_{\text{track}}}$$

$$\text{Pitch Shift (Semitones)} = 12 \times \log_2(\text{Ratio})$$

> [!TIP]
> Keep varispeed adjustments within $\pm 1.7\%$ ($\pm 0.3$ semitones) so pitch changes remain undetectable to the human ear while locking the beat grid sample-accurately to visual cuts.
