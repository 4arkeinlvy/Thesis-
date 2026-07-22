# Integrasi Data Gambar dan Teks untuk Mendukung *Smart City*

> **Integrating Image and Text Data to Support Smart City Initiatives**
>
> Undergraduate thesis (*Skripsi*) — a multimodal (image + text) classification
> system that routes citizen environmental complaints to the responsible Jakarta
> city agency (*dinas*), plus the full implementation that backs it.

Manual triage in urban complaint systems is a bottleneck: a single report can take
nearly two hours to reach the right agency, and most platforms ignore the two
signals citizens already provide — a **photo** of the incident and a **free-text
description** (*laporan*). This project fuses both. A frozen **DINOv3-large** image
encoder and a frozen **multilingual-E5-large** text encoder produce dense
embeddings that are concatenated via **early fusion** and classified by a
**CatBoost** head calibrated with **Posterior Gaussian Sampling (PGS)** into Jakarta
CRM agency categories. A deterministic rule-based engine then combines the predicted
*dinas* with the report's GPS coordinates to route it to the nearest active relevant
unit — near-instant distribution with no human in the loop.

### Key results

| Metric | Value |
| --- | --- |
| Macro F1-score (9,266-report held-out test set) | **0.7747** |
| Accuracy / Balanced accuracy | 0.8074 / 0.7916 |
| System Usability Scale (n = 30 citizen testers) | **71.6** — *Acceptable* |

**Keywords:** smart city, multimodal classification, early fusion, CatBoost,
Posterior Gaussian Sampling, Jakarta CRM.

---

## Repository layout

This repository has two sub-projects:

| Path | What it is |
| --- | --- |
| [`Docs/`](Docs/) | The LaTeX thesis document (chapters, appendices, figures, compiled PDFs). |
| [`smartCityReport/`](smartCityReport/) | The implementation — Python multimodal inference pipeline + FastAPI server + Flutter Android app. Has its own [README](smartCityReport/README.md). |

> `smartCityReport/` is an embedded Git repository with its own history and remote
> (`github.com/4arkeinlvy/smartCityReport`); the pointer tracked here records the
> exact commit the thesis was written against.

---

## The thesis document — `Docs/`

Written in LaTeX (bilingual abstract, body in Bahasa Indonesia).

```
Docs/
├── main.tex                    # entry point
├── front/                      # cover, abstract, statement, kata pengantar
├── chapters/                   # Bab1–Bab5 (intro → conclusion)
├── appendix/                   # lampiran (appendices)
├── images/                     # figures, diagrams, screenshots
├── diagrams_src/               # PlantUML sources for schema/architecture diagrams
├── references/                 # references.bib
└── scripts/                    # Python figure/plot builders (matplotlib, PlantUML)
```

### Compiled PDFs

Three PDFs are committed and rebuilt after edits:

| File | Contents | Pages |
| --- | --- | --- |
| `Docs/main.pdf` | Full thesis (body + appendix) | ~200 |
| `Docs/Skripsi_tanpa_Lampiran.pdf` | Body only, without appendix | ~186 |
| `Docs/Lampiran.pdf` | Appendix only | ~14 |

The two slices are page-ranges of `main.pdf`; regenerate all three together so they
never drift apart.

### Building

```bash
cd Docs
latexmk -pdf main.tex        # or: pdflatex main.tex (×2) + bibtex main
```

Auxiliary build files (`*.aux`, `*.log`, `*.bbl`, `*.toc`, …) are git-ignored.

---

## The implementation — `smartCityReport/`

The active path is **early-fusion multimodal** inference served over HTTP and
consumed by a Flutter Android client:

- **Encoders** — DINOv3-large (image) + multilingual-E5-large (text), both frozen
  and exported to **ONNX** (opset 17); only the CatBoost head is trained.
- **Server** — FastAPI `serve_model.py`; `POST /predict` takes a multipart image
  file + `laporan` text and returns the predicted *dinas* with probabilities.
- **App** — Flutter (`smart_city_reporter_app/`): capture photo + GPS + complaint
  text, classify via the server, review/correct the category, and route to the
  matching agency.

See [`smartCityReport/README.md`](smartCityReport/README.md) for setup, serving,
Docker, and app run instructions.

---

## Notes

- Raw questionnaire data / screenshots with respondent names (PII), credentials,
  large datasets, and model checkpoints are intentionally **not** committed.
- `CLAUDE.md` holds repo-specific guidance for the Claude Code assistant.
