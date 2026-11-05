#!/usr/bin/env python3
"""backtime_music_calc.py - Precise Musical Back-Timing & Transient Alignment Calculator.

Calculates exact sourceIn times and varispeed ratios to ensure a music track's natural
resolving downbeat/impact lands with sample-accuracy on the film's visual end-card cut.

Usage:
  python backtime_music_calc.py <audio_file> --list-hits
  python backtime_music_calc.py <audio_file> --film 26.5 --card 22.5 --hit 96.018 [--bpm 121 --to-bpm 120] [--out processed.wav]
"""

import argparse
import os
import shutil
import subprocess
import sys
import numpy as np
from scipy.io import wavfile

SR = 48000

def parse_args():
    parser = argparse.ArgumentParser(description="Back-time a music track so its final hit lands on the end card cut.")
    parser.add_argument("audio", help="Source audio file (WAV, MP3, FLAC).")
    parser.add_argument("--list-hits", action="store_true", help="List candidate final hit transients in the track.")
    parser.add_argument("--film", type=float, help="Total film duration in seconds.")
    parser.add_argument("--card", type=float, help="Timeline second where the final end card appears.")
    parser.add_argument("--hit", type=float, help="Timestamp (seconds) of the selected hit in the source audio.")
    parser.add_argument("--bpm", type=float, help="Original measured BPM of the track.")
    parser.add_argument("--to-bpm", type=float, help="Target timeline BPM (for pitch-locked or varispeed sync).")
    parser.add_argument("--out", default=None, help="Optional output path to write pre-trimmed audio file.")
    return parser.parse_args()

def load_audio_pcm(file_path):
    # Try scipy wavfile directly if WAV
    if file_path.lower().endswith(".wav"):
        try:
            rate, data = wavfile.read(file_path)
            if data.dtype == np.int16:
                st = data.astype(np.float64) / 32768.0
            elif data.dtype == np.int32:
                st = data.astype(np.float64) / 2147483648.0
            else:
                st = data.astype(np.float64)
            if st.ndim == 1:
                st = np.stack([st, st], axis=1)
            return st
        except Exception:
            pass

    # Try ffmpeg
    if shutil.which("ffmpeg"):
        cmd = ["ffmpeg", "-v", "error", "-i", file_path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
        res = subprocess.run(cmd, capture_output=True, check=True)
        return np.frombuffer(res.stdout, np.float32).reshape(-1, 2).astype(np.float64)

    raise RuntimeError(f"Unable to decode audio: ensure file is an uncompressed WAV or ffmpeg is installed.")

def list_candidate_hits(x, search_window=20.0):
    mono = x.mean(axis=1)
    hop = int(0.01 * SR)
    n_frames = len(mono) // hop
    if n_frames < 100:
        print("Audio file is too short.")
        return

    rms = 10 * np.log10((mono[:n_frames * hop].reshape(n_frames, hop) ** 2).mean(axis=1) + 1e-12)
    body_level = np.percentile(rms, 90)

    start_idx = max(3, n_frames - int(search_window * 100))
    candidates = []

    for i in range(start_idx, n_frames - 1):
        if rms[i] > body_level - 9 and rms[i] - rms[i - 3:i].min() > 6 and rms[i] >= rms[max(0, i - 5):i + 6].max():
            later_window = rms[i + 5:min(n_frames, i + 150)]
            drop = rms[i] - (10 * np.log10((10 ** (later_window / 10)).mean()) if len(later_window) else -120)
            candidates.append((i * hop / SR, rms[i] - body_level, drop))

    print(f"\n--- Candidate Final Hits in last {search_window}s ---")
    print("  Time (s)     Rel Level (dB)     Drop in next 1.5s")
    for t_sec, rel_db, drop_db in candidates:
        print(f"  {t_sec:8.3f}s     {rel_db:+6.1f} dB          {drop_db:5.1f} dB")
    print("\nTip: Choose the hit where the downbeat resolves cleanly.")

def main():
    args = parse_args()
    x = load_audio_pcm(args.audio)
    total_src_sec = len(x) / SR

    if args.list_hits:
        list_candidate_hits(x)
        return

    if args.film is None or args.card is None or args.hit is None:
        print("Error: When calculating back-time, --film, --card, and --hit are all required.", file=sys.stderr)
        print("Run with --list-hits first to find candidate hits.", file=sys.stderr)
        sys.exit(2)

    ratio = 1.0
    if args.bpm and args.to_bpm:
        ratio = args.to_bpm / args.bpm

    effective_hit = args.hit / ratio
    source_in = effective_hit - args.card
    source_out = source_in + args.film

    print("\n=== MUSICAL BACK-TIMING SOLUTION ===")
    print(f"Source Track Duration: {total_src_sec:.3f} s")
    print(f"Selected Source Hit:   {args.hit:.3f} s")
    print(f"Target End Card Cut:   {args.card:.3f} s (in {args.film:.2f}s film)")
    if ratio != 1.0:
        print(f"Varispeed Ratio:       {ratio:.4f} ({(ratio - 1) * 100:+.2f}%)")
    print(f"Calculated sourceIn:   {max(0.0, source_in):.3f} s ({round(max(0.0, source_in) * 60)} frames @ 60fps)")
    print(f"Calculated sourceOut:  {source_out:.3f} s")
    print(f"FilmCraft Integer Ticks: {round(max(0.0, source_in) * 254016000000)} ticks")

    if source_in < 0:
        print(f"Notice: Track will start {-source_in:.2f}s after film begins (lead-in silence).")

    if args.out:
        from scipy.signal import resample_poly
        if abs(ratio - 1.0) > 1e-5:
            up, down = 1000, int(round(1000 * ratio))
            x = resample_poly(x, up, down, axis=0)

        start_samp = int(round(source_in * SR))
        n_samp = int(round(args.film * SR))
        y = np.zeros((n_samp, 2), dtype=np.float64)

        src_offset = max(0, start_samp)
        dst_offset = src_offset - start_samp
        avail = min(len(x) - src_offset, n_samp - dst_offset)
        if avail > 0:
            y[dst_offset:dst_offset + avail] = x[src_offset:src_offset + avail]

        fi = int(0.04 * SR)
        y[:fi] *= (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, fi)))[:, None]

        wavfile.write(args.out, SR, np.clip(y * 32767.0, -32768, 32767).astype(np.int16))
        print(f"Exported pre-trimmed audio file to: {args.out}")

if __name__ == "__main__":
    main()
