"""Generate the app development lifecycle diagram (horizontal phase flow)."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parents[1] / "images" / "bab_3" / "app_development_lifecycle.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "font.size": 9.5})

PHASES = [
    {
        "title": "1. Analisis Kebutuhan",
        "items": [
            "Identifikasi 3 peran pengguna (Warga, Operator, Moderator)",
            "Daftar kebutuhan fungsional dan non-fungsional",
            "Studi sistem CRM Jakarta dan SP4N-LAPOR! sebagai konteks operasional",
        ],
        "color": "#fdebd0",
        "border": "#b9770e",
    },
    {
        "title": "2. Perancangan Sistem",
        "items": [
            "Arsitektur klien-server: Flutter + FastAPI + Supabase",
            "Use case diagram lengkap (3 aktor utama, 4 aktor sistem)",
            "Class diagram lapisan service dan repositori",
            "Sequence diagram alur POST /predict",
            "ERD Supabase (profiles, reports, report_history)",
            "Routing instansi terdekat dari kelas + lat/lon",
        ],
        "color": "#d6eaf8",
        "border": "#2874a6",
    },
    {
        "title": "3. Perancangan Antarmuka",
        "items": [
            "Information architecture: 17 layar utama",
            "Mockup berbasis Material Design 3",
            "Komponen reusable (card laporan, peta, bottom sheet)",
            "Flow Buat Laporan dari foto sampai submit",
        ],
        "color": "#e8daef",
        "border": "#6c3483",
    },
    {
        "title": "4. Implementasi Backend (FastAPI)",
        "items": [
            "Endpoint /health (GET) dan /predict (POST multipart)",
            "Pemuatan 3 ONNX session pada startup",
            "Pipeline fusi awal: image encoder → text encoder → concat → CatBoost+PGS",
            "Dockerfile dan Docker Compose untuk reproducibility",
        ],
        "color": "#d5f5e3",
        "border": "#1e8449",
    },
    {
        "title": "5. Implementasi Frontend (Flutter)",
        "items": [
            "State management Riverpod, navigasi GoRouter",
            "Layanan: AiClassificationService, CloudClassificationService, LocationService, MediaService",
            "17 layar pada lib/features/<feature>/<screen>.dart",
            "Fitur: kamera, galeri, GPS, peta, pelaporan, tinjauan AI, riwayat, dashboard",
        ],
        "color": "#fef5e7",
        "border": "#b9770e",
    },
    {
        "title": "6. Integrasi Backend dan Layanan",
        "items": [
            "Supabase Auth (PKCE flow)",
            "Row Level Security per peran pada tabel utama",
            "Supabase Storage bucket report-images",
            "Supabase Realtime untuk update status lintas peran",
            "AppConfig.CRM_API_URL untuk endpoint FastAPI",
        ],
        "color": "#d4efdf",
        "border": "#196f3d",
    },
    {
        "title": "7. Pengujian",
        "items": [
            "Unit test layanan klasifikasi",
            "Integrasi alur Buat Laporan end-to-end",
            "Pengujian pada perangkat Android fisik (adb reverse)",
            "Validasi paritas PyTorch ↔ ONNX (|Δp|_max < 1e-5)",
            "Evaluasi macro F1, balanced accuracy, confusion matrix",
        ],
        "color": "#fadbd8",
        "border": "#922b21",
    },
    {
        "title": "8. Deployment",
        "items": [
            "Build APK release Flutter",
            "Deploy server FastAPI ke RunPod / VPS via Docker image",
            "Migrasi skema dan RPC Supabase",
            "Pengaturan retry, timeout, circuit breaker",
            "Distribusi prototipe ke pengguna uji",
        ],
        "color": "#d1f2eb",
        "border": "#117864",
    },
]

FIG_W = 22.0
FIG_H = 10.5

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=180)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis("off")

ax.text(
    FIG_W / 2,
    FIG_H - 0.35,
    "Siklus Pengembangan Aplikasi SmartCityApps",
    ha="center",
    fontsize=15,
    fontweight="bold",
    color="#17202a",
)

# Phase columns
n_phases = len(PHASES)
margin_x = 0.4
total_phase_w = FIG_W - 2 * margin_x
phase_w = total_phase_w / n_phases - 0.2
gap = 0.2
phase_h = 7.6
phase_y = 1.4

for i, phase in enumerate(PHASES):
    x = margin_x + i * (phase_w + gap)
    # Header band
    header_h = 0.65
    ax.add_patch(
        FancyBboxPatch(
            (x, phase_y + phase_h - header_h),
            phase_w,
            header_h,
            boxstyle="round,pad=0.04,rounding_size=0.10",
            facecolor=phase["border"],
            edgecolor=phase["border"],
            linewidth=0.8,
            zorder=4,
        )
    )
    ax.text(
        x + phase_w / 2,
        phase_y + phase_h - header_h / 2,
        phase["title"],
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="white",
        zorder=5,
        wrap=True,
    )
    # Body
    body_h = phase_h - header_h - 0.05
    ax.add_patch(
        FancyBboxPatch(
            (x, phase_y),
            phase_w,
            body_h,
            boxstyle="round,pad=0.04,rounding_size=0.10",
            facecolor=phase["color"],
            edgecolor=phase["border"],
            linewidth=0.8,
            zorder=3,
        )
    )
    # Bullet items
    n_items = len(phase["items"])
    item_top = phase_y + body_h - 0.20
    item_step = (body_h - 0.40) / max(n_items, 1)
    for k, item in enumerate(phase["items"]):
        y_item = item_top - k * item_step - item_step / 2
        ax.text(
            x + 0.10,
            y_item,
            f"• {item}",
            ha="left",
            va="center",
            fontsize=8.5,
            color="#1b2631",
            wrap=True,
            zorder=5,
        )

# Bottom arrow strip linking phases sequentially
arrow_y = phase_y - 0.55
for i in range(n_phases - 1):
    x_a = margin_x + i * (phase_w + gap) + phase_w
    x_b = margin_x + (i + 1) * (phase_w + gap)
    ax.add_patch(
        FancyArrowPatch(
            (x_a + 0.02, arrow_y),
            (x_b - 0.02, arrow_y),
            arrowstyle="-|>",
            mutation_scale=18,
            color="#34495e",
            linewidth=1.5,
            zorder=6,
        )
    )

# Footer note
ax.text(
    FIG_W / 2,
    0.45,
    "Catatan: setiap fase dapat di-iterasi berdasarkan umpan balik dari fase berikutnya, sehingga proses bersifat iteratif (bukan strict waterfall).",
    ha="center",
    fontsize=9.2,
    style="italic",
    color="#7f8c8d",
)

plt.tight_layout()
fig.savefig(OUT, bbox_inches="tight", facecolor="white", pad_inches=0.25)
plt.close(fig)
print(f"wrote {OUT}")
