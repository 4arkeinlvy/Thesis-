"""Generate Bab 4 figures from artifact CSVs."""
from __future__ import annotations

import csv
from collections import OrderedDict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "smartCityReport" / "artifacts"
OUT = ROOT / "Docs" / "images" / "bab_4"
OUT.mkdir(parents=True, exist_ok=True)

LABEL_NAMES = OrderedDict(
    [
        ("0", "Dinas Bina Marga"),
        ("1", "Satpol PP"),
        ("2", "Dinas Perhubungan"),
        ("3", "Kelurahan"),
        ("4", "Dinas Pertamanan dan Hutan"),
        ("5", "Dinas Sumber Daya Air"),
        ("6", "Dinas Cipta Karya, Tata Ruang, dan Pertanahan"),
        ("7", "Badan Pembinaan BUMD"),
        ("8", "Instansi lain"),
    ]
)

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 200,
    }
)


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def plot_class_distribution():
    counts = {k: 0 for k in LABEL_NAMES}
    rows = load_csv(ART / "splits" / "train.csv")
    for r in rows:
        counts[r["label_id"]] = counts.get(r["label_id"], 0) + 1
    labels = list(LABEL_NAMES.values())
    values = [counts[k] for k in LABEL_NAMES]
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    bars = ax.barh(labels, values, color="#3a6ea5", edgecolor="black", linewidth=0.4)
    for bar, v in zip(bars, values):
        ax.text(v + max(values) * 0.005, bar.get_y() + bar.get_height() / 2,
                f"{v:,}", va="center", fontsize=8)
    ax.set_xlabel("Jumlah sampel pelatihan")
    ax.set_title("Distribusi Sembilan Kategori Dinas pada Set Train (43.241 sampel)")
    ax.invert_yaxis()
    plt.tight_layout()
    out = OUT / "class_distribution.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


def plot_modality_ablation():
    rows = load_csv(ART / "models" / "modality_ablation.csv")
    configs = [r["config"] for r in rows]
    f1_cb = [float(r["f1_catboost"]) for r in rows]
    f1_pgs = [float(r["f1_pgs"]) for r in rows]
    acc_cb = [float(r["acc_catboost"]) for r in rows]
    acc_pgs = [float(r["acc_pgs"]) for r in rows]

    x = np.arange(len(configs))
    w = 0.2
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    ax.bar(x - 1.5 * w, acc_cb, w, label="Acc (CatBoost)", color="#9bb7d4")
    ax.bar(x - 0.5 * w, acc_pgs, w, label="Acc (CatBoost+PGS)", color="#3a6ea5")
    ax.bar(x + 0.5 * w, f1_cb, w, label="Macro F1 (CatBoost)", color="#f0b67f")
    ax.bar(x + 1.5 * w, f1_pgs, w, label="Macro F1 (CatBoost+PGS)", color="#d96e30")

    for i, (a1, a2, f1, f2) in enumerate(zip(acc_cb, acc_pgs, f1_cb, f1_pgs)):
        for offset, val in zip([-1.5, -0.5, 0.5, 1.5], [a1, a2, f1, f2]):
            ax.text(i + offset * w, val + 0.005, f"{val:.3f}", ha="center", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace(" only", " saja").replace("fusion", "fusi awal") for c in configs])
    ax.set_ylim(0, 0.95)
    ax.set_ylabel("Skor")
    ax.set_title("Ablasi Modalitas: Citra, Teks, dan Fusi Awal")
    ax.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    out = OUT / "modality_ablation.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


def plot_pgs_comparison():
    rows = load_csv(ART / "models" / "pgs_ablation.csv")
    models = [r["model"] for r in rows]
    acc = [float(r["accuracy"]) for r in rows]
    f1 = [float(r["macro_f1"]) for r in rows]

    x = np.arange(len(models))
    w = 0.34
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.bar(x - w / 2, acc, w, label="Balanced Accuracy", color="#3a6ea5")
    ax.bar(x + w / 2, f1, w, label="Macro F1", color="#d96e30")
    for i, (a, f) in enumerate(zip(acc, f1)):
        ax.text(i - w / 2, a + 0.004, f"{a:.4f}", ha="center", fontsize=8)
        ax.text(i + w / 2, f + 0.004, f"{f:.4f}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylim(0.7, 0.86)
    ax.set_ylabel("Skor")
    ax.set_title("Ablasi Kalibrasi: CatBoost dengan dan tanpa PGS")
    ax.legend()
    plt.tight_layout()
    out = OUT / "pgs_comparison.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


def plot_encoder_matrix():
    rows = load_csv(ART / "models" / "matrix_results.csv")
    image_order = ["dinov3_large", "dinov2_large", "eva02_large", "hiera_large"]
    text_order = ["mE5_large", "bge_m3", "indobert", "cendol_mt5"]
    grid = np.full((len(image_order), len(text_order)), np.nan)
    for r in rows:
        try:
            i = image_order.index(r["image"])
            j = text_order.index(r["text"])
            grid[i, j] = float(r["f1_pgs"])
        except ValueError:
            continue

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    im = ax.imshow(grid, cmap="YlGnBu", vmin=0.7, vmax=0.78)
    ax.set_xticks(range(len(text_order)))
    ax.set_xticklabels(["mE5 large", "BGE-M3", "IndoBERT", "Cendol-mT5"], rotation=20)
    ax.set_yticks(range(len(image_order)))
    ax.set_yticklabels(["DINOv3 large", "DINOv2 large", "EVA-02 large", "Hiera large"])
    for i in range(len(image_order)):
        for j in range(len(text_order)):
            v = grid[i, j]
            if np.isnan(v):
                continue
            color = "white" if v > 0.755 else "black"
            ax.text(j, i, f"{v:.4f}", ha="center", va="center", fontsize=9, color=color)
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.04)
    cb.set_label("Macro F1 (CatBoost+PGS)")
    ax.set_title("Ablasi Pasangan Encoder pada CatBoost+PGS")
    plt.tight_layout()
    out = OUT / "encoder_matrix.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


def main():
    plot_class_distribution()
    plot_modality_ablation()
    plot_pgs_comparison()
    plot_encoder_matrix()


if __name__ == "__main__":
    main()
