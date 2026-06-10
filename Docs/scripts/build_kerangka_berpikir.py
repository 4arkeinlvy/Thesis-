"""Generate Gambar 3.1: Kerangka Berpikir Penelitian SmartCityApps.

Clean 4-phase top-to-bottom research framework.
No long diagonal arrows; one short vertical arrow between consecutive phases.
Technical jargon replaced with research-level wording.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "images" / "bab_3" / "kerangka_berpikir.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "font.size": 11})

FIG_W, FIG_H = 11.5, 11.5
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=300)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis("off")

# Title
ax.text(
    FIG_W / 2, FIG_H - 0.30,
    "Kerangka Berpikir Penelitian SmartCityApps",
    ha="center", va="center",
    fontsize=15, fontweight="bold", color="#17202a",
)

PALETTE = {
    "phase1": "#fef9e7",  # identifikasi masalah
    "phase2": "#e8daef",  # pengembangan model
    "phase3": "#d4efdf",  # implementasi sistem
    "phase4": "#f5cba7",  # pengujian dan evaluasi
}

# Phase boxes (4 stacked top to bottom)
phase_w = 9.0
phase_h = 1.95
phase_x = (FIG_W - phase_w) / 2
gap = 0.50

phases = [
    {
        "title": "1. Identifikasi Masalah",
        "body": (
            "Triase manual laporan warga membutuhkan waktu lama dan rentan kesalahan.\n"
            "Volume laporan meningkat dan kategori dinas yang relevan beragam."
        ),
        "fc": PALETTE["phase1"],
    },
    {
        "title": "2. Pengembangan Model",
        "body": (
            "Akuisisi dan pembersihan dataset CRM Jakarta menjadi 9 instansi target.\n"
            "Ekstraksi fitur citra dan teks, lalu pelatihan klasifier multimodal CatBoost + PGS."
        ),
        "fc": PALETTE["phase2"],
    },
    {
        "title": "3. Implementasi Sistem",
        "body": (
            "Backend FastAPI menjalankan inferensi server-side dan routing instansi terdekat.\n"
            "Aplikasi Android SmartCityApps berperan sebagai klien yang mengirim laporan."
        ),
        "fc": PALETTE["phase3"],
    },
    {
        "title": "4. Pengujian dan Evaluasi",
        "body": (
            "Pengujian metrik klasifikasi pada partisi uji dan validasi end-to-end sistem.\n"
            "Analisis dampak fusi multimodal dan PGS terhadap akurasi serta confidence."
        ),
        "fc": PALETTE["phase4"],
    },
]

# Place phases from top to bottom
phase_top_y = FIG_H - 1.30  # leave room for title
phase_rects = []
for i, p in enumerate(phases):
    y = phase_top_y - i * (phase_h + gap) - phase_h
    rect = FancyBboxPatch(
        (phase_x, y), phase_w, phase_h,
        boxstyle="round,pad=0.10,rounding_size=0.22",
        facecolor=p["fc"], edgecolor="#2c3e50", linewidth=1.4,
    )
    ax.add_patch(rect)
    # Title at the top of the box
    ax.text(
        phase_x + 0.30, y + phase_h - 0.40,
        p["title"],
        ha="left", va="center",
        fontsize=13, fontweight="bold", color="#17202a",
    )
    # Body lines
    ax.text(
        phase_x + 0.30, y + phase_h / 2 - 0.25,
        p["body"],
        ha="left", va="center",
        fontsize=11, color="#1b2631",
    )
    phase_rects.append((phase_x, y, phase_w, phase_h))

# Single vertical arrow between each consecutive pair (centered)
for i in range(len(phase_rects) - 1):
    px, py, pw, ph = phase_rects[i]
    nx, ny, nw, nh = phase_rects[i + 1]
    start = (px + pw / 2, py)
    end = (nx + nw / 2, ny + nh)
    ax.add_patch(
        FancyArrowPatch(
            start, end,
            arrowstyle="-|>", mutation_scale=20,
            linewidth=1.8, color="#34495e",
        )
    )

plt.tight_layout()
fig.savefig(OUT, bbox_inches="tight", facecolor="white", pad_inches=0.30)
plt.close(fig)
print(f"wrote {OUT}")
