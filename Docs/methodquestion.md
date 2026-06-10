# Plan: Bab 2 Closing Paragraph, Gambar 3.10 Revamp, Multi-Instansi Discussion, and PGS Limitations Justification

## Context

The thesis (`/Users/quatumteknologinusantara/Thesis-/Docs/`) currently has four open issues that need to be addressed in a single revision pass:

1. **Bab 2 closing paragraph** ([Bab2.tex:1155-1156](Docs/chapters/Bab2.tex#L1155-L1156)) is currently a *chapter-summary bridge* — a long inventory of what was covered followed by a sentence forecasting Bab 3. The user wants it rewritten in the style of [Docs/example.txt](Docs/example.txt), which is a **research-positioning paragraph**: states what the research will explore, identifies the gap, mentions methodology/dataset, articulates the goal, and closes with the expected contribution.

2. **Gambar 3.10** ([Bab3.tex:140-145](Docs/chapters/Bab3.tex#L140-L145)) is a single 324 KB screenshot (`sample_table.png`) that crams three rows × three columns (Gambar / Laporan / Label) into one figure at `width=0.95\textwidth`. The user reports it as *gabisa diliat dan berantakan* and asks if splitting helps. Only one `\ref` resolves to it ([Bab3.tex:138](Docs/chapters/Bab3.tex#L138)).

3. **Multi-instansi routing case for the professor** — the user wants a `.tex` snippet that frames the question: *"What happens when one report belongs to multiple instansi (e.g., parkir liar + jalan berlubang)?"* This needs to be added as a discussion subsection (target: end of Bab 4 ambiguity discussion or beginning of Bab 5 Saran/Future Work) so it can be presented to the supervisor.

4. **Why PGS is not working well** — Bab 4 reports a modest +0.78 pp balanced-accuracy gain and a *negative* −0.43 pp F1 on the image-only ablation ([Bab4.tex:127, 158](Docs/chapters/Bab4.tex)). The user wants a comprehensive, mathematically grounded, peer-review-cited justification of *why* — to be added to Bab 4 (analysis subsection) and forward-referenced from Bab 5.

The intended outcome is a single coherent edit pass that improves Bab 2's chapter-closing rhetoric, makes Gambar 3.10 actually readable, raises the multi-instansi limitation as a discussion item suitable for supervisory review, and replaces the current thin "PGS gave +0.78 pp" framing with a research-grounded analysis of selective-prediction theory.

---

## Deliverable 1 — Rewrite Bab 2 closing paragraph

**File:** [Docs/chapters/Bab2.tex:1155-1156](Docs/chapters/Bab2.tex#L1155-L1156)

**Current behavior:** Long inventory sentence ("Bab ini telah memaparkan landasan teoretis ... mulai dari konteks *smart city* ... hingga penelitian terkait") followed by a one-sentence Bab 3 forecast. This reads as a recap, not as research positioning.

**Target structure (mirrors [Docs/example.txt](Docs/example.txt)):**

1. **Sentence 1 — what the research explores:** "Penelitian ini akan mengeksplorasi penggunaan arsitektur *early-fusion multimodal* yang menggabungkan *encoder* visual DINOv3-large dan *encoder* teks multilingual-E5-large dengan kepala klasifikasi CatBoost untuk mengklasifikasikan laporan warga Jakarta CRM ke dalam kategori dinas operasional."
2. **Sentence 2 — the gap:** Frame the gap — to the best of the author's knowledge, no prior work has combined these specific frozen encoders with a gradient-boosted head for Bahasa Indonesia civic reports; prior multimodal disaster/civic work (CLIP, Audebert, Ofli, Alam, Koshy) used different encoders, different domains, or English-only text.
3. **Sentence 3 — methodology + dataset:** State that the dataset is sourced from Jakarta CRM (lapor.go.id portal) via web scraping, comprising image–text pairs labelled into nine consolidated dinas categories.
4. **Sentence 4 — research goal:** State the goal — improve efficiency and accuracy of routing citizen reports to the correct dinas, while quantifying predictive uncertainty via *Posterior Gaussian Sampling*.
5. **Sentence 5 — expected contribution:** Close with what the work is expected to contribute — a deployable cross-platform pipeline (FastAPI server + Flutter Android client) and an empirical comparison of multimodal fusion vs. unimodal baselines for the Indonesian civic-report domain.

**Style anchors:** Long flowing sentences, *italic* for technical terms, formal academic Indonesian register, `\citep{}`/`\citet{}` consistent with rest of chapter ([Bab2.tex:24, 296](Docs/chapters/Bab2.tex)). Re-use existing bib keys: `simeoniDINOv32025`, `wangE5Multilingual2024`, `prokhorenkovaCatBoost2018`, `ustimenkoCatBoostUncertainty2023`.

**Decision:** *Keep* the existing chapter-summary sentence as a separate, shorter prefix (one sentence), then *append* the new research-positioning paragraph as the actual closing block. This preserves the bridge to Bab 3 while adopting the example.txt style for the final paragraph.

---

## Deliverable 2 — Gambar 3.10 revamp

**File:** [Docs/chapters/Bab3.tex:140-145](Docs/chapters/Bab3.tex#L140-L145), single `\ref` site at [Bab3.tex:138](Docs/chapters/Bab3.tex#L138).

**Problem:** Single `sample_table.png` (324 KB, 3 rows × 3 columns) at 0.95\textwidth is unreadable — the photo, the multi-line `Laporan` text, and the `Label` cell all compete for space.

**Recommended approach — split into three sub-figures, one per representative row:**

```latex
\begin{figure}[htbp]
    \centering
    \begin{subfigure}[t]{\textwidth}
        \centering
        \includegraphics[width=0.85\textwidth]{bab_3/sample_row_1.png}
        \caption{Contoh 1: laporan parkir liar dengan label \textit{Dinas Perhubungan}.}
        \label{fig:sample-row-1}
    \end{subfigure}
    \vspace{0.6em}
    \begin{subfigure}[t]{\textwidth}
        \centering
        \includegraphics[width=0.85\textwidth]{bab_3/sample_row_2.png}
        \caption{Contoh 2: laporan jalan berlubang dengan label \textit{Dinas Bina Marga}.}
        \label{fig:sample-row-2}
    \end{subfigure}
    \vspace{0.6em}
    \begin{subfigure}[t]{\textwidth}
        \centering
        \includegraphics[width=0.85\textwidth]{bab_3/sample_row_3.png}
        \caption{Contoh 3: laporan sampah menumpuk dengan label \textit{Dinas Lingkungan Hidup}.}
        \label{fig:sample-row-3}
    \end{subfigure}
    \caption{Contoh struktur data multimodal: tiga baris representatif, masing-masing menampilkan kolom \textit{Gambar}, \textit{Laporan}, dan \textit{Label}.}
    \label{fig:sample-table}
\end{figure}
```

**Image preparation (script, executed in implementation phase):** Crop the existing `sample_table.png` into three horizontal strips (one per row) saved as `sample_row_1.png`, `sample_row_2.png`, `sample_row_3.png`. ImageMagick one-liner: `convert sample_table.png -crop 1xN@ +repage row_%d.png` where N is the row count, then rename. If row content is too text-heavy to read even when isolated, regenerate from source by rendering each row as a 2-column layout (photo on the left at ~40% width, text+label stacked on the right at ~60%) using a small matplotlib or HTML-to-PNG script.

**Reposition:** Move from `[htbp]` to `[H]` (require `\usepackage{float}`; check Bab2/Bab3 preambles — likely already loaded since other figures may need it) so the split lands exactly under the explanatory paragraph at [Bab3.tex:138](Docs/chapters/Bab3.tex#L138). Keep the existing label `fig:sample-table` so the single `\ref` at line 138 still resolves; sub-labels (`fig:sample-row-1` etc.) are available for future inline references.

**Packages:** Confirm `\usepackage{subcaption}` is loaded in [Docs/main.tex](Docs/main.tex). If not, add it to the preamble.

**Alternative (lighter touch) if the user rejects re-cropping:** Keep the single image but add `\rotatebox{90}` and place it on a landscape page via `\usepackage{pdflscape}` + `\begin{landscape}...\end{landscape}`. This is the fallback if regenerating row crops is not feasible.

---

## Deliverable 3 — Handling multi-instansi routing (standalone `.tex`, comparative)

**Target placement:** **Standalone file** at `Docs/chapters/multi_instansi_handling.tex` — not embedded in Bab 4 or Bab 5. Same convention as Deliverable 4: the file uses `\section{Penanganan Laporan dengan Rute Multi-Instansi pada Sistem Klasifikasi Jakarta CRM}` so it renders correctly whether `\input{}`-included into a chapter later or compiled standalone via a 5-line minimal driver. The user can decide downstream whether to fold it into Bab 4 (as a results-discussion subsection) or Bab 5 (as a future-work proposal). The tone is *comparative methodology*: enumerate every research-backed handling option, score each on mathematical soundness + practical feasibility on the Jakarta CRM dataset, and recommend the **single best** (with the runner-up named for completeness).

**Scenario worked example (used as a running example throughout the section):** Foto satu lokasi yang memuat *jalan berlubang yang dikelilingi mobil parkir liar*; narasi pelapor menyebut kedua isu. Ground-truth routing seharusnya: *{Dinas Bina Marga, Dinas Perhubungan}*. Sistem saat ini hanya mengembalikan satu label (lihat [serve_model.py:181](smartCityReport/serve_model.py#L181) — `idx = int(np.argmax(probs))`), sehingga laporan yang sah untuk dua instansi terpaksa "kalah" pada salah satunya.

**Section structure — comparative survey of six methods, then a recommended hybrid:**

### 3.1 — Formal problem reframing

Ubah ruang keluaran dari multi-class ($\hat{y} \in \{1,\dots,K\}$, $K=9$) menjadi multi-label ($\hat{Y} \subseteq \{1,\dots,K\}$, $|\hat{Y}| \geq 1$). Untuk laporan $x$ dengan lokasi GPS $\ell = (\text{lat}, \text{lon})$, tujuannya adalah meng-estimasi himpunan dinas yang sahih:

$$\hat{Y}(x, \ell) = \{ k : s_k(x, \ell) \geq \tau_k \}$$

di mana $s_k$ adalah skor relevansi per kelas dan $\tau_k$ ambang yang dikalibrasi.

### 3.2 — Survei enam metode penanganan

Setiap metode dievaluasi pada **empat kriteria**: (M) ketepatan matematis / dasar teori, (D) ketersediaan data Jakarta CRM, (C) biaya komputasi pelatihan ulang, (G) jaminan formal yang ditawarkan.

#### Metode 1 — Top-K dengan margin gating

Pertahankan softmax 9-kelas yang sudah ada; emisikan dua label jika $P_{(1)} - P_{(2)} < \delta$. Skor $s_k = P(y=k \mid x)$, dengan ambang dinamis $\delta$ alih-alih $\tau_k$. **(M)** Sederhana namun *ad hoc*; **(D)** tidak butuh data tambahan; **(C)** nol; **(G)** tidak ada.

#### Metode 2 — Binary Relevance (BR) multi-label

Latih $K=9$ klasifikator CatBoost biner independen; $\hat{Y} = \{k : P(y_k=1 \mid x) > \tau_k\}$. **(M)** Optimal *jika* label antar-dinas independen — asumsi yang dilanggar di Jakarta (Bina Marga & Perhubungan berkorelasi); **(D)** butuh ground-truth multi-label; **(C)** $K\times$ pelatihan ulang; **(G)** tidak ada (Tsoumakas & Katakis 2007; Zhang & Zhou 2014).

#### Metode 3 — Classifier Chains (CC)

$K$ klasifikator biner berurutan dengan augmentasi fitur kausal; menangkap korelasi antar-dinas. **(M)** Lebih kuat daripada BR pada label terkait, tetapi sensitif terhadap urutan rantai; **(D)** sama dengan BR; **(C)** $K\times$ + tuning urutan; **(G)** tidak ada (Read, Pfahringer, Holmes & Frank 2009).

#### Metode 4 — Label Powerset (LP)

Setiap kombinasi unik dari instansi diperlakukan sebagai kelas tunggal. **(M)** Mengubah masalah multi-label kembali ke multi-class; **(D)** ruang keluaran membengkak hingga $2^K = 512$ kelas — sebagian besar kombinasi tidak pernah muncul di data; **(C)** sangat tinggi (sparsity); **(G)** tidak ada. **Tidak direkomendasikan** untuk $K=9$.

#### Metode 5 — *Spatial prior* berbasis lokasi GPS (instansi terdekat)

Manfaatkan fakta bahwa pelaporan Jakarta CRM membawa GPS ([location_service.dart](smartCityReport/smart_city_reporter_app/lib/core/services/location_service.dart)) dan setiap dinas (terutama *Suku Dinas* tingkat kotamadya) memiliki *yurisdiksi spasial*. Estimasi *prior* spasial dengan kernel density estimation dari frekuensi historis laporan per kelas pada kisi-kisi koordinat:

$$P(k \mid \ell) = \frac{P(\ell \mid k)\,P(k)}{\sum_{k'} P(\ell \mid k')\,P(k')}$$

di mana $P(\ell \mid k)$ adalah KDE Gaussian dari lokasi laporan historis berlabel $k$. Untuk *Kelurahan*, prior spasial sangat tajam (laporan dirutekan ke kelurahan pada koordinat tersebut); untuk dinas tingkat-kota seperti *Sumber Daya Air*, prior lebih datar. **(M)** Berbasis Bayes formal; **(D)** GPS sudah ada di setiap laporan historis; **(C)** rendah (KDE one-shot offline); **(G)** tidak ada secara mandiri, tetapi memberikan informasi yang ortogonal terhadap modalitas citra+teks. Lihat literatur 311/civic-tech: Kontokosta & Hong 2021 ("Bias in smart city service request data"); Cavallo et al. 2014 ("311 service requests as indicators of urban issues").

#### Metode 6 — Split-Conformal multi-label dengan jaminan cakupan

Lapisan kalibrasi *post-hoc* yang berdiri di atas metode dasar (1, 2, 3, atau 5). Pada subset kalibrasi $\{(x_i, Y_i)\}$ dengan label multi-label, hitung skor non-konformitas $\alpha_i = 1 - \min_{k \in Y_i} s_k(x_i)$, lalu ambil kuantil $\hat{q}_{1-\alpha}$. Pada inferensi, emisikan $\hat{Y}(x) = \{k : s_k(x) \geq 1 - \hat{q}_{1-\alpha}\}$. **(M)** Berbasis teori conformal yang ketat; **(G)** memberikan jaminan marginal $\mathbb{P}(Y \subseteq \hat{Y}) \geq 1 - \alpha$ tanpa asumsi distribusi (Cauchois, Gupta & Duchi 2021; Vovk, Gammerman & Shafer 2005); **(D)** butuh subset kalibrasi multi-label kecil ($\sim 200$–$500$ contoh); **(C)** sangat rendah.

### 3.3 — Tabel perbandingan ringkas

| Metode | Dasar matematis | Data multi-label dibutuhkan? | Pelatihan ulang? | Jaminan formal |
|---|---|---|---|---|
| 1. Top-K margin | Heuristik | Tidak | Tidak | Tidak |
| 2. Binary Relevance | Asumsi independensi | Ya | Ya ($K\times$) | Tidak |
| 3. Classifier Chains | Korelasi antar-label | Ya | Ya ($K\times$) | Tidak |
| 4. Label Powerset | Multi-class atas $2^K$ | Ya | Ya (sparse) | Tidak |
| 5. Spatial prior | Bayes / KDE | Tidak (pakai histori) | Tidak | Tidak |
| 6. Split-Conformal multi-label | Conformal prediction | Ya (subset kalibrasi) | Tidak | $\mathbb{P}(Y \subseteq \hat{Y}) \geq 1 - \alpha$ |

### 3.4 — Rekomendasi: Hybrid (Metode 5 + 2 + 6)

Metode tunggal manapun tidak optimal. Yang *paling kuat* secara teori dan praktis adalah **kombinasi tiga lapis** yang memanfaatkan informasi ortogonal yang tersedia:

$$s_k(x, \ell) = \underbrace{P_{\text{BR}}(y_k = 1 \mid x)}_{\text{Metode 2}} \cdot \underbrace{P(k \mid \ell)^{\beta}}_{\text{Metode 5, prior spasial}}$$

dengan $\beta \in [0, 1]$ mengontrol bobot prior spasial (dipilih lewat validasi). Lapisan akhir adalah **split-conformal multi-label** (Metode 6) di atas $s_k$ untuk memberikan ambang $\tau$ tunggal dengan jaminan cakupan $1 - \alpha$.

**Justifikasi matematis untuk pemilihan ini (sesuai permintaan):**

1. **Faktorisasi Bayes yang sahih:** Mengasumsikan informasi citra+teks ($x$) dan informasi lokasi ($\ell$) bersifat *kondisional independen* mengingat instansi $k$ — asumsi yang masuk akal karena $x$ menggambarkan *isi* laporan sedangkan $\ell$ menggambarkan *konteks geografis* — kita peroleh $P(k \mid x, \ell) \propto P(x \mid k)\,P(\ell \mid k)\,P(k)$, sejajar dengan struktur Naive Bayes pada modalitas-bukan-kata (Lewis 1998).
2. **Diversifikasi kesalahan (error decorrelation):** Modalitas citra+teks dan modalitas lokasi memiliki sumber kesalahan yang berbeda; menggabungkan mereka mengurangi varians prediksi (Lakshminarayanan, Pritzel & Blundell 2017 — argumen ensembel).
3. **Jaminan formal end-to-end:** Hanya Metode 6 yang menyediakan jaminan marginal *distribution-free*, fitur yang krusial untuk sistem publik berkonsekuensi (mis. salah-rute laporan banjir).
4. **Mengatasi *aleatoric noise*:** Multi-label output mengakomodasi kasus di mana label "benar" memang multi-elemen (lihat kritik PGS pada Deliverable 4) — ini bukan label noise yang bisa dibersihkan, melainkan struktur masalah yang harus dimodelkan.

**Runner-up:** Jika data multi-label tidak dapat dibuat (Stage 3.5 di bawah gagal), pakai **Metode 1 + Metode 5** (Top-K margin di-rerank dengan prior spasial). Tidak ada jaminan formal, tetapi tidak butuh ground-truth multi-label.

### 3.5 — Penanganan keterbatasan label tunggal pada dataset historis

Dataset Jakarta CRM menyimpan **satu** dinas per laporan (keputusan akhir operator). Tiga jalur untuk memperoleh ground-truth multi-label yang dibutuhkan Metode 2/3/6:

1. **Augmentasi berbasis kata kunci** (paling murah): kamus kata kunci per dinas; $\geq 2$ dinas terdeteksi → tandai sebagai multi-label.
2. **Anotasi ulang aktif (active learning):** ambil laporan dengan ketidakpastian PGS tinggi (desil teratas) dan re-anotasi oleh dua anotator + adjudikasi.
3. **Weak supervision (Snorkel):** gabungkan kata kunci, kata kerja tindakan, dan entitas lokasi untuk label probabilistik multi-label (Ratner et al. 2017).

**Direkomendasikan:** kombinasi (1) + (2) — (1) untuk korpus pelatihan, (2) untuk subset kalibrasi conformal yang lebih bersih.

### 3.6 — Perubahan API, basis data, dan UI

- **`/predict`** ([serve_model.py:181](smartCityReport/serve_model.py#L181)): kembalikan `predicted_dinas: List[str]`, `confidence_per_dinas: Dict[str, float]`, `routing_strategy: str`.
- **Supabase ERD** ([bab_3/erd_supabase.png](Docs/images/bab_3/erd_supabase.png)): tabel pivot `report_dinas (report_id, dinas_id, confidence)` (many-to-many) menggantikan kolom tunggal.
- **Flutter** ([reports/ai_result_review_screen.dart](smartCityReport/smart_city_reporter_app/lib/features/reports/ai_result_review_screen.dart)): tampilkan daftar instansi + *confidence chip*; pengguna dapat menghapus instansi yang tidak relevan.

### 3.7 — Evaluasi multi-instansi

- **Subset Accuracy:** $\frac{1}{N}\sum_i \mathbb{1}[\hat{Y}_i = Y_i]$.
- **Hamming Loss:** $\frac{1}{NK}\sum_i \sum_k \mathbb{1}[\hat{y}_{ik} \neq y_{ik}]$.
- **Micro / Macro F1 multi-label** (Zhang & Zhou 2014).
- **Coverage rate empiris:** $\frac{1}{N}\sum_i \mathbb{1}[Y_i \subseteq \hat{Y}_i]$ — harus $\geq 1 - \alpha$ untuk Metode 6.
- **Avg. set size:** $\mathbb{E}[|\hat{Y}|]$ — diharapkan $\in [1, 2]$ agar tidak membanjiri operator.

**Bibliography additions needed (to `references.bib`):**
- `tsoumakasMultilabel2007` — Tsoumakas & Katakis, "Multi-Label Classification: An Overview", IJDWM 2007.
- `zhangMultilabelReview2014` — Zhang & Zhou, "A Review on Multi-Label Learning Algorithms", IEEE TKDE 2014.
- `readClassifierChains2009` — Read, Pfahringer, Holmes & Frank, "Classifier Chains for Multi-label Classification", ECML PKDD 2009.
- `cauchoisGuptaDuchi2021` — Cauchois, Gupta & Duchi, "Knowing What You Know: Valid and Validated Confidence Sets in Multiclass and Multilabel Prediction", JMLR 2021.
- `ratnerSnorkel2017` — Ratner et al., "Snorkel: Rapid Training Data Creation with Weak Supervision", VLDB 2017.
- `lewisNaiveBayes1998` — Lewis, "Naive (Bayes) at Forty: The Independence Assumption in Information Retrieval", ECML 1998.
- `kontokostaHong2021` — Kontokosta & Hong, "Bias in Smart City Service Request Data", *EPB: Urban Analytics & City Science* 2021.
- `cavallo311_2014` — Cavallo, Lynch & Scull, "The Digital Divide in Citizen-Initiated Government Contacts: A GIS Approach", *Journal of Urban Affairs* 2014.

---

## Deliverable 4 — Research-grounded justification: why PGS is not working well (standalone `.tex`)

**Target placement:** **Standalone file** at `Docs/chapters/pgs_analysis.tex` — not embedded in Bab 4 or Bab 5. The user explicitly asked for a separate analysis/justification document. The file is *not* `\input{}`-included into `main.tex` by default; it is a standalone deliverable that the user can later choose to inline (via `\input{chapters/pgs_analysis}`) into Bab 4 or hand to the supervisor as a discussion document.

**File header:** include a short preamble with `\documentclass`-agnostic content (no preamble of its own) — the file will define `\section{Analisis Keterbatasan Posterior Gaussian Sampling pada Klasifikasi Multimodal Laporan Jakarta CRM}` so that whether it is `\input{}`-ed into Bab 4 or compiled standalone via a tiny wrapper, it renders correctly. Empirical anchors are quoted from Bab 4 with explicit `\cite{}` to the existing PGS reference and to the new bib entries listed below.

**Empirical anchors to cite:**
- Balanced-accuracy gain only **+0.78 pp** ([Bab4.tex:158](Docs/chapters/Bab4.tex#L158)).
- Macro-F1 gain only **+0.63 pp** ([Bab4.tex:83-91](Docs/chapters/Bab4.tex#L83-L91)).
- Image-only modality: **−0.43 pp F1** ([Bab4.tex:127](Docs/chapters/Bab4.tex#L127)).
- Mean epistemic uncertainty: **0.00339** — very low spread, limits decision utility.

**Argument structure (5 reasons, each with math + citation):**

### Reason 1 — PGS quantifies *epistemic* uncertainty but the dominant uncertainty here is *aleatoric*

PGS (Ustimenko et al. 2023) decomposes total predictive uncertainty as:

$$U_{\text{total}}(x) = \underbrace{H\!\left(\bar{p}(x)\right)}_{\text{total}} = \underbrace{H\!\left(\bar{p}(x)\right) - \tfrac{1}{M}\sum_{m=1}^{M} H\!\left(p^{(m)}(x)\right)}_{U_{\text{epistemic}}} + \underbrace{\tfrac{1}{M}\sum_{m=1}^{M} H\!\left(p^{(m)}(x)\right)}_{U_{\text{aleatoric}}}$$

where $\bar{p}(x) = \frac{1}{M}\sum_m p^{(m)}(x)$ is the posterior mean over $M$ virtual ensembles.

The Jakarta CRM dataset suffers from substantial *aleatoric* (data-inherent) noise because (i) 487 raw SKPD names were collapsed into 9 dinas — a many-to-one map that destroys information ([Bab3.tex:189-196](Docs/chapters/Bab3.tex)); (ii) operator routing decisions are inconsistent across years ([Bab4.tex:279](Docs/chapters/Bab4.tex#L279)); (iii) the multi-instansi case (Deliverable 3) implies the "true" label is set-valued, not point-valued. Aleatoric uncertainty is *irreducible* by adding more model capacity or ensemble members (Kendall & Gal 2017; Hüllermeier & Waegeman 2021), so PGS — which tightens *epistemic* estimates — cannot help on the dominant noise component. **Cite:** Kendall & Gal 2017 ("What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?", NeurIPS); Hüllermeier & Waegeman 2021 ("Aleatoric and epistemic uncertainty in machine learning", Machine Learning).

### Reason 2 — PGS provides no coverage guarantee (unlike conformal prediction)

PGS returns calibrated-by-construction posterior means but offers *no formal guarantee* that the top-1 prediction set has any pre-specified coverage probability $1 - \alpha$. This is a structural difference from *conformal prediction* (CP), which does: for any exchangeable calibration set, CP produces sets $\hat{C}_\alpha(x)$ satisfying $\mathbb{P}(y \in \hat{C}_\alpha(x)) \geq 1 - \alpha$ marginally (Vovk, Gammerman & Shafer 2005; Angelopoulos & Bates 2021).

For a downstream decision system that must *route or escalate*, what matters is "how often is the true dinas in the top-K?" — i.e., a *coverage* quantity. PGS's epistemic-uncertainty scalar (mean 0.00339 in our results) does not directly translate into such coverage; the operator would still have to choose an arbitrary threshold without any statistical backing. **Cite:** Vovk, Gammerman & Shafer 2005 ("Algorithmic Learning in a Random World"); Angelopoulos & Bates 2021 ("A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification", arXiv:2107.07511).

### Reason 3 — PGS assumes the base learner is already well-calibrated; CatBoost on imbalanced 9-class softmax is not

PGS is a *post-hoc* refinement that computes the *posterior mean* over ensemble samples; if the per-ensemble-member softmax outputs are themselves miscalibrated, averaging them does not fix the bias. Guo et al. (2017) showed that modern over-parameterised classifiers tend to be overconfident; gradient-boosted trees on highly imbalanced multi-class targets exhibit a related problem — minority classes receive squeezed probability mass that ensemble averaging cannot restore.

Our [Bab4.tex:127](Docs/chapters/Bab4.tex#L127) observation that PGS *hurts* image-only F1 by 0.43 pp is consistent with this: when the unimodal CatBoost head is poorly calibrated (likely because DINOv3 embeddings alone do not separate classes like *Dinas Sosial* vs. *Dinas Lingkungan Hidup*), virtual-ensemble averaging amplifies the bias rather than correcting it. **Cite:** Guo, Pleiss, Sun & Weinberger 2017 ("On Calibration of Modern Neural Networks", ICML); Niculescu-Mizil & Caruana 2005 ("Predicting Good Probabilities with Supervised Learning", ICML) for the gradient-boosted-trees calibration result.

### Reason 4 — Virtual ensembles share parameters, so PGS underestimates true epistemic spread

The $M$ virtual ensembles in PGS are not independently trained models; they are sub-trees from a *single* CatBoost model under stochastic gradient Langevin dynamics (SGLD)-style sampling (Ustimenko et al. 2023, §3.2). True deep ensembles (Lakshminarayanan, Pritzel & Blundell 2017) train $M$ independent models from random initialisations and consistently outperform single-model uncertainty proxies. PGS trades that statistical strength for inference-time efficiency — a deliberate engineering choice — but the resulting *epistemic* spread is biased low, which is consistent with our observed mean uncertainty of only 0.00339. **Cite:** Lakshminarayanan, Pritzel & Blundell 2017 ("Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles", NeurIPS).

### Reason 5 — A single argmax discards the uncertainty signal at the application layer

Even if PGS produced perfect uncertainty estimates, the deployed system collapses the prediction back to a single label via `np.argmax(probs)` in [serve_model.py:110-117](smartCityReport/serve_model.py#L110-L117). The downstream Flutter client surfaces uncertainty only as a percentage on the result screen, not as an abstention or routing-to-multiple-instansi action. This means the *practical* benefit of PGS is bounded by what the UI does with the scalar — and currently it does nothing operationally. The natural fix (selective prediction with a coverage-guaranteed threshold, or set-valued output via conformal prediction) is the link to Deliverable 3. **Cite:** Geifman & El-Yaniv 2017 ("Selective Classification for Deep Neural Networks", NeurIPS); El-Yaniv & Wiener 2010 ("On the Foundations of Noise-free Selective Classification", JMLR).

### Closing recommendation

Replace the current PGS narrative ("PGS gives a small but positive lift") with: *PGS provides epistemic uncertainty quantification at near-zero inference cost, but on this dataset (i) aleatoric noise dominates, (ii) the system lacks a coverage-guaranteed selective-prediction layer, and (iii) the single-argmax UI cannot exploit the uncertainty signal. A future iteration should replace PGS with split-conformal prediction over the fused embedding to obtain set-valued routing recommendations with provable marginal coverage* — and forward-reference Deliverable 3.

**Bibliography additions needed (to `references.bib`):**
- `kendallGal2017` — Kendall & Gal, "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?", NeurIPS 2017.
- `huellermeierWaegeman2021` — Hüllermeier & Waegeman, "Aleatoric and epistemic uncertainty in machine learning: an introduction to concepts and methods", Machine Learning 2021.
- `vovkAlgorithmic2005` — Vovk, Gammerman & Shafer, "Algorithmic Learning in a Random World", Springer 2005.
- `angelopoulosBates2021` — Angelopoulos & Bates, "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification", arXiv:2107.07511.
- `guoCalibration2017` — Guo, Pleiss, Sun & Weinberger, "On Calibration of Modern Neural Networks", ICML 2017.
- `niculescuMizilCaruana2005` — Niculescu-Mizil & Caruana, "Predicting Good Probabilities with Supervised Learning", ICML 2005.
- `lakshminarayananDeepEnsembles2017` — Lakshminarayanan, Pritzel & Blundell, "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles", NeurIPS 2017.
- `geifmanElYaniv2017` — Geifman & El-Yaniv, "Selective Classification for Deep Neural Networks", NeurIPS 2017.
- `elYanivWiener2010` — El-Yaniv & Wiener, "On the Foundations of Noise-free Selective Classification", JMLR 2010.

---

## Deliverable 5 — Reconcile the 9-class vs. 4-cluster discrepancy (clarification only, no code bug)

**Investigation result (already verified during planning):** The user reported a suspicion that "the PGS code is routing to 4 instansi instead of 9". A targeted code audit found **no truncation in the codebase**:

- [smartCityReport/src/crm/__init__.py:1-11](smartCityReport/src/crm/__init__.py#L1-L11) defines `TARGET_CLASSES` with all **9** dinas.
- [smartCityReport/serve_model.py:161, 181](smartCityReport/serve_model.py) returns all 9 in `/health` and all 9 probabilities in `/predict`.
- [smartCityReport/src/crm/pgs.py](smartCityReport/src/crm/pgs.py) contains no hard-coded class counts; it is class-count-agnostic.
- The Flutter client [report_models.dart:7-89](smartCityReport/smart_city_reporter_app/lib/features/reports/report_models.dart) defines all 9 `IssueCategory` enum members (cloudId 0..8).
- [classification_routing.dart:50-60](smartCityReport/smart_city_reporter_app/lib/features/reports/classification_routing.dart#L50-L60) routes each of the 9 categories to its specific guidance.

**Root cause of confusion:** The number "4" appears in the **thesis prose only** at [Bab3.tex:196](Docs/chapters/Bab3.tex#L196), which states *"Empat kluster yang dipakai adalah Kebersihan dan Ketertiban Umum, Infrastruktur Jalan, Keselamatan Lalu Lintas, dan Pohon dan Kedaruratan"*. This describes a **conceptual operational grouping** of the 9 dinas into 4 thematic clusters — a thesis-level abstraction that has **never been implemented in code**. The code routes at the 9-dinas granularity end-to-end.

**Action items (small, two LaTeX edits + a confirmation question):**

1. **Bab 3 clarification edit** — at [Bab3.tex:196](Docs/chapters/Bab3.tex#L196), append one sentence: *"Pengelompokan ke empat kluster operasional ini bersifat konseptual untuk memudahkan pembahasan; pipeline klasifikasi tetap menghasilkan keluaran pada granularitas sembilan dinas penuh, dan tidak ada agregasi 9→4 yang diterapkan pada kode penyajian (lihat \texttt{TARGET\_CLASSES} pada \texttt{src/crm/\_\_init\_\_.py} dan \texttt{classification\_routing.dart} pada klien Flutter)."*
2. **Bab 4 cross-check** — verify Bab 4 results tables and confusion matrices report 9 classes (not 4); if any aggregation table exists, label it explicitly as a derived view.
3. **Optional, deferred:** if the user wants the 4-cluster grouping to actually exist in the code (e.g., as an aggregated routing fallback for low-confidence predictions), implement an explicit cluster-mapping function in [classification_routing.dart](smartCityReport/smart_city_reporter_app/lib/features/reports/classification_routing.dart). **This is a follow-up question for the user — do not implement without confirmation.**

This deliverable is *documentation reconciliation*, not a bug fix.

---

## Critical Files

- [Docs/chapters/Bab2.tex:1155-1156](Docs/chapters/Bab2.tex#L1155-L1156) — closing paragraph rewrite (Deliverable 1)
- [Docs/chapters/Bab3.tex:138-145](Docs/chapters/Bab3.tex#L138-L145) — Gambar 3.10 figure block + reference (Deliverable 2)
- [Docs/chapters/Bab3.tex:196](Docs/chapters/Bab3.tex#L196) — append clarifying sentence about 9 vs 4 (Deliverable 5)
- [Docs/chapters/Bab4.tex:83-91, 127, 158, 279](Docs/chapters/Bab4.tex) — empirical anchors *quoted* by Deliverables 3 & 4 (no edits inside Bab 4)
- **NEW:** [Docs/chapters/multi_instansi_handling.tex](Docs/chapters/multi_instansi_handling.tex) — standalone multi-instansi handling methodology (Deliverable 3)
- **NEW:** [Docs/chapters/pgs_analysis.tex](Docs/chapters/pgs_analysis.tex) — standalone PGS-limitations analysis (Deliverable 4)
- [Docs/references/references.bib](Docs/references/references.bib) — append ~17 new bib entries (D3: 8 new, D4: 9 new)
- [Docs/main.tex](Docs/main.tex) — verify `subcaption`, `float` packages are loaded; do **not** auto-`\input{}` either standalone file
- [Docs/images/bab_3/sample_table.png](Docs/images/bab_3/sample_table.png) — split into three row crops `sample_row_{1,2,3}.png`

## Reused Helpers / Patterns

- `\citep{...}` / `\citet{...}` — natbib style already used throughout [Bab2.tex](Docs/chapters/Bab2.tex) (e.g. lines 24, 296, 529, 652).
- Existing PGS reference `ustimenkoCatBoostUncertainty2023` is already in [references.bib](Docs/references/references.bib) — reuse.
- Existing `prokhorenkovaCatBoost2018`, `simeoniDINOv32025`, `wangE5Multilingual2024` — reuse for Bab 2 closing.
- `\subcaption` package pattern is the standard LaTeX way to split a single figure into labeled sub-figures.

## Verification

After implementing:

1. Run `latexmk -pdf main.tex` from `Docs/` and confirm zero `Undefined references`, zero `Citation undefined`, no overfull-hbox warnings on the new subfigure block.
2. Open the rendered PDF and confirm:
   - Bab 2's last paragraph reads as a research-positioning paragraph mirroring example.txt's rhetorical arc.
   - Gambar 3.10 renders as three labelled sub-figures (3.10a, 3.10b, 3.10c), each readable at normal zoom.
   - Bab 3 §3 (around line 196) has the appended clarifying sentence about 9 dinas vs. 4 conceptual clusters.
3. Standalone-compile **both** `multi_instansi_handling.tex` and `pgs_analysis.tex` by wrapping each in a 5-line minimal driver (`\documentclass{article}` + `\usepackage{amsmath, booktabs, hyperref}` + `\input`) to confirm they render cleanly outside the main document. Confirm:
   - `multi_instansi_handling.tex` renders the comparison table, the six method blocks, the recommended hybrid formula, and Stages 3.5–3.7.
   - `pgs_analysis.tex` renders all five numbered reasons with their display equations.
4. Run `bibtex main` (or `biber main`) and confirm all ~17 newly added bib keys resolve (no "I didn't find a database entry" warnings).
5. Spot-check that `\autoref{fig:sample-row-1}` / `fig:sample-row-2` / `fig:sample-row-3` resolve to the expected sub-figure numbers.
6. Confirm via `grep -rn "TARGET_CLASSES" smartCityReport/` that the class count is 9 across the codebase (Deliverable 5 sanity check — should already be true).
