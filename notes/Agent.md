# Prompt: Deep Thesis Chapter Revision, Research Refresh, and Code/Experiment Gap Audit

You are a senior thesis editor, research assistant, LaTeX maintainer, machine-learning engineer, and software architecture reviewer. Your task is to deeply revise my thesis project, not only polish wording. You must inspect the thesis files, references, diagrams, source code, notebooks, experiments, and generated PDF so that the final Bab 1 sampai Bab 5 is coherent, technically accurate, research-grounded, and maximum 80 pages.

## Repository / Working Directory

Work inside this local project:

```bash
/Users/quatumteknologinusantara/Thesis-/smartCityReport
```

Before editing, inspect the project structure:

```bash
pwd
find . -maxdepth 3 -type f | sort
find . -maxdepth 4 \( -name "*.tex" -o -name "*.bib" -o -name "*.pdf" -o -name "*.ipynb" -o -name "*.py" -o -name "*.md" \) | sort
```

If there are multiple thesis PDFs or LaTeX entry files, identify the current main file by checking `\documentclass`, `\begin{document}`, `\include{}`, `\input{}`, `latexmkrc`, `Makefile`, `README`, or build scripts.

## Main Goal

Revise the thesis chapter files and produce a clean, consistent, evidence-backed version. The final thesis body from Bab 1 to Bab 5 must be **maximum 80 pages** after compilation. Do not merely rephrase. You must also check whether the writing matches the real code, notebook flow, experiments, diagrams, use-case diagrams, UI screenshots, and implementation.

## Hard Revision Requests

Delete these sections completely from the thesis:

- `2.4.2`
- `2.19.3`
- `2.19.4`
- `2.3.5`
- `2.3.6`
- `2.8.3`
- `2.12.6`

After deletion:

1. Fix numbering and cross-references.
2. Remove orphaned citations that were only used in deleted sections.
3. Remove unused figures/tables only referenced by those sections.
4. Recompile and verify there are no broken `\ref`, `\autoref`, `\cite`, `\label`, or bibliography warnings.

## Reference Freshness Rules

Use references from the last 5 years relative to 2026. That means prioritize **2021–2026**, with stronger preference for **2023–2026**.

Rules:

1. Papers older than 2021 should be replaced unless they are truly foundational and unavoidable.
2. If an older foundational idea is needed, find newer papers that cite/use it and cite those newer papers instead.
3. For DINOv2, note carefully: DINOv2 is not a 2016 paper. DINOv2 was released in 2023. Use the original DINOv2 paper only if methodologically necessary, then strengthen it with newer papers that use or extend DINOv2.
4. For non-paper article references, use articles published between **November 2025 and April 2026** where possible.
5. Do not invent citations. Every citation must exist in the `.bib` file and be used in the LaTeX text.
6. Build a reference audit table showing: citation key, title, year, source type, where used, status, and action.

Recommended research direction:

- DINOv2 / visual foundation models / self-supervised vision.
- Recent papers that use DINOv2 for image classification, segmentation, open-vocabulary segmentation, remote sensing, urban scenes, or smart-city-related vision tasks.
- Recent smart city, intelligent traffic monitoring, computer vision surveillance, public safety, urban AI, and real-time monitoring literature.
- Recent articles and reports from November 2025 to April 2026 for real-world smart-city AI context, privacy, deployment, and operational issues.

Candidate references to verify and consider:

- Oquab et al., **DINOv2: Learning Robust Visual Features without Supervision**, 2023.
- Jose et al., **DINOv2 Meets Text: A Unified Framework for Image- and Pixel-Level Vision-Language Alignment**, CVPR 2025.
- Barsellotti et al., **Talking to DINO: Bridging Self-Supervised Vision Backbones with Language for Open-Vocabulary Segmentation**, 2024/2025.
- Ray & Skurikhin, **Deep Clustering of Remote Sensing Scenes through Heterogeneous Transfer Learning**, 2024.
- Recent 2025–2026 smart city / traffic monitoring / urban AI papers and reports.

## Article Reference Window

For article-style references, policy/context reports, or applied smart-city examples, use references within this date range:

```text
November 2025 – April 2026
```

Use these only when they support background, urgency, real-world deployment context, or ethical/privacy discussion. Do not use blog articles as core methodology references. Core methodology must come from peer-reviewed papers, arXiv, CVF, IEEE/ACM/Springer/Elsevier/MDPI journals, or official reports.

## Diagram, Image, and Appendix Rules

Audit all diagrams and images:

1. Keep only essential diagrams in the main body.
2. Move large UI screenshots, repetitive screens, implementation screenshots, and supporting images to appendices/lampiran.
3. Every figure must have a clear caption, label, and reference in the text.
4. Every diagram must match the actual code and system flow.
5. Fix use case diagrams if they contain actors/features that are not implemented.
6. Add missing flow diagrams if code/notebooks show important flow not represented in the thesis.
7. If the diagram is outdated, either update it or mark it as removed.

## Section 3.16 UI App Display Rule

For section `3.16`, the content should describe the application UI briefly and refer screenshots to the appendix.

Starting from:

- `3.16.1`
- `3.16.2`
- `3.16.3`
- `3.16.4`
- `3.16.5`
- `3.16.6`
- `3.16.7`

Use concise wording like:

```text
Tampilan antarmuka untuk fitur ini dapat dilihat pada Lampiran [X]. Bagian ini menjelaskan fungsi utama, alur interaksi pengguna, dan keterkaitan fitur dengan kebutuhan sistem.
```

Do not place every UI screenshot directly in Bab 3 unless it is critical to understand the architecture or method. Move most screenshots to the appendix.

## Technical and Research Gap Audit

You must inspect the code and notebooks, then compare them with the thesis writing. Focus on gaps such as:

### Research / Writing Gaps

- Problem statement in Bab 1 does not match the actual implemented system.
- Research questions, objectives, scope, and contribution are inconsistent.
- Literature review discusses methods that are not used or not connected to the experiment.
- Methodology claims a flow that the code does not implement.
- Experiment setup lacks dataset description, preprocessing details, split strategy, hyperparameters, environment, evaluation metrics, or reproducibility notes.
- Results do not connect back to research questions.
- Conclusion claims more than the experiment proves.

### Code / Flow Gaps

- Missing preprocessing step in the thesis but present in code, or vice versa.
- Dataset split not clearly explained.
- Risk of data leakage.
- Missing seed/reproducibility setting.
- Inconsistent label mapping between dataset, code, and thesis.
- Metrics in the thesis differ from metrics in notebook output.
- Diagrams do not match actual function/class/module flow.
- UI or use-case flow describes features that are not implemented.
- The thesis says DINOv2 or another model is used, but the notebook/code uses a different architecture or pipeline.
- Experiment does not include baseline/comparison but thesis claims comparison.
- Confusion matrix/classification report/accuracy/F1 are missing or not interpreted.

### Critical Experiment Checks

Inspect every `.ipynb`, `.py`, and generated result file. Verify:

1. Dataset source and directory structure.
2. Number of classes and label names.
3. Train/validation/test split.
4. Preprocessing and augmentation.
5. Model architecture and feature extractor.
6. Frozen vs fine-tuned layers.
7. Optimizer, learning rate, batch size, epochs.
8. Early stopping/checkpointing.
9. Evaluation metrics.
10. Confusion matrix and error analysis.
11. Comparison/baseline, if claimed.
12. Hardware/software environment.
13. Reproducibility: seed, package versions, deterministic settings where possible.

If an experiment claim is not supported by code/output, either fix the writing or add a clear TODO/gap note in the revision report.

## LaTeX Cleanup Requirements

Clean and standardize the LaTeX files:

1. Fix broken section numbering after deletion.
2. Use consistent Indonesian academic wording.
3. Avoid informal language inside thesis chapters.
4. Avoid overlong paragraphs.
5. Fix figure/table captions.
6. Ensure all images use consistent `figure` environments.
7. Ensure tables do not overflow page width.
8. Use `\label` after `\caption`.
9. Ensure every citation compiles.
10. Remove duplicate bibliography entries.
11. Move long code listings, huge tables, repetitive screenshots, and secondary diagrams to appendix.
12. Compile with `latexmk` or the project’s existing build command.

Suggested compile commands:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
# or use the existing project build command if different
```

If compilation fails, fix the LaTeX error before continuing.

## Page Budget Strategy: Bab 1–Bab 5 Max 80 Pages

Use this target allocation:

| Chapter | Target Pages | Notes |
|---|---:|---|
| Bab 1 | 8–12 | Problem, scope, objectives, contribution. Keep concise. |
| Bab 2 | 18–25 | Literature review. Remove deleted/irrelevant sections. Use recent references. |
| Bab 3 | 18–24 | Methodology/system design. Diagrams must match actual code. Move UI screenshots to appendix. |
| Bab 4 | 18–24 | Experiments/results/discussion. Prioritize tables, metrics, analysis. |
| Bab 5 | 4–6 | Conclusion and future work. Do not overclaim. |

If the PDF exceeds 80 pages:

1. Move UI screenshots to appendix.
2. Compress literature review.
3. Merge repetitive subsections.
4. Move long implementation details to appendix.
5. Keep only key diagrams and result tables in main body.

## Required Output Files

Create a revision folder:

```bash
mkdir -p docs/thesis-revision
```

Produce these files:

```text
docs/thesis-revision/REVISION_REPORT.md
docs/thesis-revision/REFERENCE_AUDIT.md
docs/thesis-revision/CODE_EXPERIMENT_GAP_AUDIT.md
docs/thesis-revision/DIAGRAM_UI_APPENDIX_AUDIT.md
docs/thesis-revision/PAGE_BUDGET_REPORT.md
```

### `REVISION_REPORT.md`

Include:

- Summary of changed files.
- Sections deleted.
- Major wording/LaTeX changes.
- Remaining risks.
- Build status.
- Final page count.

### `REFERENCE_AUDIT.md`

Include:

| Citation Key | Title | Year | Type | Used In | Status | Action |
|---|---|---:|---|---|---|---|

Status options:

- `keep`
- `replace`
- `remove`
- `new`
- `foundational exception`

### `CODE_EXPERIMENT_GAP_AUDIT.md`

Include:

| Area | Thesis Claim | Code/Notebook Evidence | Gap | Severity | Fix |
|---|---|---|---|---|---|

Severity:

- `critical`
- `major`
- `minor`

### `DIAGRAM_UI_APPENDIX_AUDIT.md`

Include:

| Figure/Diagram | Current Location | Problem | Action | New Location |
|---|---|---|---|---|

### `PAGE_BUDGET_REPORT.md`

Include:

| Chapter | Pages Before | Pages After | Action Taken |
|---|---:|---:|---|

## Workflow

Follow this order:

1. Inspect repository structure.
2. Identify LaTeX main file and bibliography file.
3. Compile current PDF and record current page count.
4. Search and map all target sections to delete.
5. Delete the requested sections.
6. Audit references and update to 2021–2026 where possible.
7. Inspect code/notebooks/results.
8. Compare actual implementation with Bab 1–Bab 5 claims.
9. Fix diagrams, use-case flow, methodology wording, and experiment description.
10. Move UI screenshots from section 3.16.1–3.16.7 to appendix references.
11. Clean LaTeX formatting.
12. Compile again.
13. Fix warnings/errors.
14. Check final page count is <= 80 pages for Bab 1–Bab 5.
15. Produce the five audit reports.

## Search Commands to Use

Use `rg` aggressively:

```bash
rg "2\.4\.2|2\.19\.3|2\.19\.4|2\.3\.5|2\.3\.6|2\.8\.3|2\.12\.6" -n .
rg "DINO|DINOv2|ViT|Vision Transformer|YOLO|CNN|smart city|smart\s*city|classification|segmentation" -n .
rg "use case|Use Case|diagram|flow|activity|sequence|UI|antarmuka|lampiran|appendix" -n .
rg "\\cite|\\ref|\\label|\\includegraphics|\\section|\\subsection|\\subsubsection" -n .
```

For notebooks:

```bash
find . -name "*.ipynb" -print
jupyter nbconvert --to markdown path/to/notebook.ipynb --output-dir docs/thesis-revision/notebook_exports
```

## Important Constraints

- Do not hallucinate implementation details.
- Do not claim a model, dataset, result, or metric unless it is supported by code/notebook/output.
- Do not remove important methodology just to reduce pages; move supporting details to appendix instead.
- Do not cite outdated papers unless justified as foundational.
- Do not leave broken references.
- Do not leave unused `.bib` entries if they are clearly obsolete and not cited.
- Do not put repetitive UI screenshots in the main body.
- Keep thesis wording formal, clear, and academically acceptable in Indonesian.

## Final Response Expected From Agent

When done, summarize:

1. Files modified.
2. Deleted sections.
3. Reference changes.
4. Technical/code gaps found and fixed.
5. Diagrams/UI screenshots moved or revised.
6. Final page count.
7. Build command used and build status.
8. Remaining issues that still need manual decision.

Also include exact paths to the generated reports.
