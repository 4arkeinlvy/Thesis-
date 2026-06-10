"""Generate Gambar 3.7: Alur Inferensi Server-Side SmartCityApps.

Clean layout, all-Indonesian labels, short title.
  Row 1 (top):    image and text lanes (2 boxes each) -> Konkatenasi
  Row 2 (bottom): Klasifier -> Routing -> Output

Bottom row is centered under the fusion block so the vertical arrow is short.
No long diagonal arrows. No arrows cross box text.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "images" / "bab_3" / "flow_inferensi.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "font.size": 12})

PALETTE = {
    "input":   "#fdf2e9",
    "encoder": "#d6eaf8",
    "fusion":  "#e8daef",
    "head":    "#abebc6",
    "router":  "#f5cba7",
    "output":  "#d4efdf",
}

FIG_W, FIG_H = 15.0, 8.5
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=300)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis("off")


def block(x, y, w, h, text, fc="#ffffff", ec="#2c3e50", lw=1.4, fontsize=11):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.05,rounding_size=0.18",
            facecolor=fc, edgecolor=ec, linewidth=lw, zorder=4,
        )
    )
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center",
        fontsize=fontsize, color="#1b2631", wrap=True, zorder=5,
    )
    return (x, y, w, h)


def harrow(a, b, color="#2c3e50", lw=1.6):
    ax_, ay_, aw_, ah_ = a
    bx_, by_, bw_, bh_ = b
    ax.add_patch(
        FancyArrowPatch(
            (ax_ + aw_, ay_ + ah_ / 2), (bx_, by_ + bh_ / 2),
            arrowstyle="-|>", mutation_scale=18,
            color=color, linewidth=lw, zorder=6,
        )
    )


def varrow(start, end, label=None, color="#2c3e50", lw=1.6):
    ax.add_patch(
        FancyArrowPatch(
            start, end,
            arrowstyle="-|>", mutation_scale=18,
            color=color, linewidth=lw, zorder=6,
        )
    )
    if label:
        ax.text(
            (start[0] + end[0]) / 2 + 0.18, (start[1] + end[1]) / 2, label,
            ha="left", va="center",
            fontsize=10, color="#34495e", style="italic", zorder=6,
        )


# ---------- TITLE ----------
ax.text(
    FIG_W / 2, FIG_H - 0.25,
    "Alur Inferensi Server-Side SmartCityApps",
    ha="center", fontsize=15, fontweight="bold", color="#17202a",
)

# ---------- TOP LANES (2 boxes per lane) ----------
bw, bh = 2.70, 1.25
gap = 0.35
x0 = 0.90
y_img = 6.30
y_txt = 4.55

ax.text(0.30, y_img + bh / 2, "Jalur Citra", fontsize=11, fontweight="bold",
        color="#5b6e8c", rotation=90, va="center")
ax.text(0.30, y_txt + bh / 2, "Jalur Teks", fontsize=11, fontweight="bold",
        color="#5b6e8c", rotation=90, va="center")

# Image lane
I1 = block(x0, y_img, bw, bh,
           "Citra laporan\n(JPEG)\nResize 224x224\nNormalisasi ImageNet",
           fc=PALETTE["input"], fontsize=10)
I2 = block(x0 + bw + gap, y_img, bw, bh,
           "Encoder Citra\nDINOv3 large\n(frozen ONNX)\nembedding 1024d",
           fc=PALETTE["encoder"], fontsize=10)
harrow(I1, I2)

# Text lane
T1 = block(x0, y_txt, bw, bh,
           "Narasi laporan\n(Bahasa Indonesia)\nTokenisasi SentencePiece\nmaksimal 256 token",
           fc=PALETTE["input"], fontsize=10)
T2 = block(x0 + bw + gap, y_txt, bw, bh,
           "Encoder Teks\nmultilingual-E5 large\n(frozen ONNX)\nembedding 1024d",
           fc=PALETTE["encoder"], fontsize=10)
harrow(T1, T2)

# ---------- FUSION (right of lanes, vertically centered) ----------
fx = x0 + 2 * (bw + gap) + 0.15
fusion_y = (y_img + y_txt) / 2  # centered vertically between lanes
fusion = block(fx, fusion_y, 2.50, bh,
               "Konkatenasi\nvektor 2048d", fc=PALETTE["fusion"], fontsize=12)

# Curved arrows from each lane encoder to fusion
ax.add_patch(
    FancyArrowPatch(
        (I2[0] + I2[2], I2[1] + I2[3] / 2),
        (fusion[0], fusion[1] + fusion[3] - 0.25),
        arrowstyle="-|>", mutation_scale=18, color="#2c3e50",
        linewidth=1.6, connectionstyle="arc3,rad=-0.20", zorder=6,
    )
)
ax.add_patch(
    FancyArrowPatch(
        (T2[0] + T2[2], T2[1] + T2[3] / 2),
        (fusion[0], fusion[1] + 0.25),
        arrowstyle="-|>", mutation_scale=18, color="#2c3e50",
        linewidth=1.6, connectionstyle="arc3,rad=0.20", zorder=6,
    )
)

# ---------- BOTTOM ROW (centered under fusion area) ----------
y_bot = 1.95
bot_bh = 1.45
head_w, router_w, out_w = 3.30, 3.60, 3.60
bot_total = head_w + gap + router_w + gap + out_w
# Center the bottom row under the fusion block to keep the vertical arrow short
fusion_center_x = fusion[0] + fusion[2] / 2
bot_x0 = fusion_center_x - bot_total / 2
# Clamp to canvas margin
bot_x0 = max(0.40, min(bot_x0, FIG_W - bot_total - 0.40))

head = block(bot_x0, y_bot, head_w, bot_bh,
             "Klasifier\nCatBoost + PGS (ONNX)\nsoftmax 9 instansi\nkeluaran: prediksi + confidence",
             fc=PALETTE["head"], fontsize=10)

router = block(bot_x0 + head_w + gap, y_bot, router_w, bot_bh,
               "Routing Backend\n(setelah inferensi)\nHaversine antara koordinat\nlaporan dan kantor instansi",
               fc=PALETTE["router"], fontsize=10)

final_out = block(bot_x0 + head_w + gap + router_w + gap, y_bot, out_w, bot_bh,
                  "Output ke SmartCityApps\ninstansi prediksi + confidence\ninstansi terdekat + jarak",
                  fc=PALETTE["output"], fontsize=10)

# Vertical arrow: fusion -> head (short, near-vertical since bottom row is centered)
varrow(
    (fusion[0] + fusion[2] / 2, fusion[1]),
    (head[0] + head[2] / 2, head[1] + head[3]),
    label="2048d",
)

# Horizontal arrows on bottom row (no labels to avoid overlap)
harrow(head, router)
harrow(router, final_out)

plt.tight_layout()
fig.savefig(OUT, bbox_inches="tight", facecolor="white", pad_inches=0.30)
plt.close(fig)
print(f"wrote {OUT}")
