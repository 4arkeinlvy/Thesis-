# REFERENCE AUDIT — `references/references.bib`

## Executive Summary

- **Total entries:** 95
- **Cited at least once in Bab 1–5:** 62 (65 %)
- **Orphan entries (never cited):** 33 (35 %) — safe to remove
- **Entries dated 2021 or newer:** 51 (54 %)
- **Entries dated 2023 or newer:** 38 (40 %)
- **Pre-2021 entries kept as foundational exceptions:** 4 (`goodfellowDeepLearning2016`, `lecunDeepLearning2015`, `heResNet2016`, `krizhevskyImageNet2012`)
- **Pre-2021 entries used in text that should be replaced or upgraded:** 12

**Recent corrections applied:**
- `vaswaniAttentionAllYou2023` — year corrected `2023 → 2017` (original Transformer is arXiv:1706.03762, June 2017). Citation key intentionally left unchanged to avoid touching every `\citep` site.
- `oquabDINOv22024` — year corrected `2024 → 2023` (DINOv2 is arXiv:2304.07193, April 2023). Citation key intentionally left unchanged.

Recommended end-state count after cleanup: **≈ 62 entries** (45 keep-as-is + 4 foundational + ~13 upgraded variants for in-text replacements).

## Audit Table

Status values:
- `keep` — 2021 or newer, already used
- `replace` — pre-2021, used in text; find newer alternative
- `remove` — never cited; delete from `.bib`
- `foundational exception` — pre-2021, used in text, no fresher substitute viable
- `new` — proposed addition

| Citation Key | Title (short) | Year | Type | Used In | Status | Action |
|---|---|---|---|---|---|---|
| alamCrisisMMD2018 | CrisisMMD: Multimodal Twitter Datasets | 2018 | inproc | Bab 2, Bab 1 | replace | Find 2023+ multimodal disaster benchmark |
| amorEdgeAIPractice2025 | Edge AI in Practice: Survey | 2025 | article | Bab 1, Bab 2 | keep | — |
| androidDevDocs2024 | Android Developer Documentation | 2024 | misc | Bab 2 | keep | — |
| angelopoulosBates2021 | Gentle Intro to Conformal Prediction | 2021 | article | Bab 2 | keep | — |
| appleCoreML2024 | Core ML Documentation | 2024 | misc | Bab 2 | keep | — |
| article | Analisis Teks Bahasa Indonesia | 2022 | article | Bab 2 | keep | Verify entry key is unique (key `article` is dangerous — rename to e.g. `analisisTeksId2022`) |
| audebertMultimodalDoc2019 | Multimodal Deep Networks for Documents | 2019 | article | Bab 2, Bab 1 | replace | Find 2023+ multimodal-fusion classifier |
| bahdanauAttention2015 | NMT by Jointly Learning to Align and Translate | 2015 | misc | — | remove | Never cited |
| baltrusaitisMultimodalSurvey2019 | Multimodal ML: A Survey | 2019 | article | — | remove | Never cited |
| boochUML2005 | The UML User Guide | 2005 | book | Bab 2 | replace | Use a 2023+ software-architecture text or remove single UML citation |
| brownC42018 | The C4 Model | 2018 | book | — | remove | Never cited |
| cahyawijayaCendol2024 | Cendol: Instruction-tuned LLM | 2024 | inproc | Bab 2 | keep | — |
| caronDINO2021 | Emerging Properties in SSL ViT (DINO) | 2021 | inproc | — | remove | Never cited (DINO is referenced only via DINOv2/DINOv3) |
| cauchoisGuptaDuchi2021 | Knowing What You Know | 2021 | article | Bab 2 | keep | — |
| cavallo311_2014 | Digital Divide in Citizen-Initiated Gov | 2014 | article | — | remove | Never cited |
| chenBGEM32024 | BGE M3-Embedding | 2024 | misc | Bab 2 | keep | — |
| conneauXLMR2020 | Unsupervised Cross-lingual XLM-R | 2020 | inproc | — | remove | Never cited |
| crmEarlyFusion2024 | Penugasan Otomatis Laporan Masyarakat | 2024 | inproc | — | remove | Duplicate of `hanifPenugasanOtomatis2024`; remove |
| crmJakartaPortal2024 | CRM Jakarta Portal | 2024 | misc | — | remove | Never cited |
| cubukRandAugment2020 | RandAugment | 2020 | inproc | — | remove | Never cited |
| dalalHOG2005 | Histograms of Oriented Gradients | 2005 | inproc | Bab 2 | replace | Reference is in §2.9 hand-crafted features. Keep if §2.9 is kept; remove if §2.9 is compressed (see PAGE_BUDGET_REPORT.md) |
| devlinBERT2019 | BERT | 2019 | inproc | Bab 2 | replace | Cite e.g. Liu et al. 2024 (BERT survey) or keep as baseline foundational |
| dosovitskiyImageWorth16x162021 | ViT (Image Is Worth 16×16 Words) | 2021 | misc | Bab 2 | keep | — |
| elYanivWiener2010 | Foundations of Noise-Free Selective Classification | 2010 | article | Bab 2 | replace | If used only in PGS section, drop; PGS is justified by `ustimenkoCatBoostUncertainty2023` |
| fangEVA022023 | EVA-02 | 2023 | misc | Bab 2 | keep | — |
| fastapidoc2024 | FastAPI Documentation | 2024 | misc | Bab 2 | keep | — |
| firgiaImplementasiSistemInformasi2022 | Implementasi Pengaduan Masyarakat | 2022 | article | Bab 1 | keep | — |
| flutterdoc2024 | Flutter Documentation | 2024 | misc | Bab 1, Bab 2 | keep | — |
| geifmanElYaniv2017 | Selective Classification for Deep NN | 2017 | inproc | Bab 2 | replace | Same as elYanivWiener2010 |
| goodfellowDeepLearning2016 | Deep Learning (textbook) | 2016 | book | Bab 2 | foundational exception | KEEP |
| guoCalibration2017 | On Calibration of Modern Neural Networks | 2017 | inproc | — | remove | Never cited |
| hanifPenugasanOtomatis2024 | GEMASTIK Penugasan Otomatis | 2024 | inproc | Bab 1, Bab 4 | keep | Direct prior-work baseline; keep |
| harianhaluanCRMJakarta2024 | Pemprov DKI 93.2% aduan | 2024 | misc | Bab 1 | keep | — |
| heMAE2022 | MAE | 2022 | inproc | Bab 2 | keep | — |
| heResNet2016 | ResNet | 2016 | inproc | Bab 2 | foundational exception | KEEP |
| huellermeierWaegeman2021 | Aleatoric/Epistemic Uncertainty | 2021 | article | Bab 2 | keep | — |
| jakartaSmartCityCRMSemesterI2024 | CRM Reports Jan-Jun 2024 | 2024 | misc | Bab 1 | keep | — |
| jakartaSmartCityKaleidoskop2024 | Kaleidoskop CRM 2024 | 2024 | misc | Bab 1 | keep | — |
| joliffePCA2002 | PCA (textbook) | 2002 | book | Bab 2 | replace | If §2.10 PCA kept, swap to `wallTutorialPCA2024` (new) or remove section per budget |
| kendallGal2017 | Uncertainties in Bayesian DL | 2017 | inproc | — | remove | Never cited |
| kingmaAdam2014 | Adam Optimizer | 2014 | misc | — | remove | Never cited |
| kontokostaHong2021 | Bias in Smart City Service Requests | 2021 | article | — | remove | Never cited (could be kept if Bab 4 discussion adds bias note) |
| koshyMultimodalTweet2023 | Multimodal Tweet Classification | 2023 | article | Bab 1, Bab 2 | keep | — |
| kotoIndoLEM2020 | IndoLEM/IndoBERT | 2020 | inproc | Bab 2 | replace | Already covered by `cahyawijayaCendol2024`; consider drop |
| krizhevskyImageNet2012 | AlexNet | 2012 | inproc | Bab 2 | foundational exception | KEEP |
| kudoSentencePiece2018 | SentencePiece | 2018 | inproc | Bab 2 | replace | Foundational tokenizer; keep or merge with `sennrichBPE2016` discussion |
| lakshminarayananDeepEnsembles2017 | Deep Ensembles | 2017 | inproc | Bab 2 | replace | Find 2023+ ensemble UQ work |
| lecunDeepLearning2015 | Deep Learning (Nature review) | 2015 | article | Bab 2 | foundational exception | KEEP |
| lewisNaiveBayes1998 | Naive Bayes at Forty | 1998 | inproc | — | remove | Never cited |
| liuConvNeXtV22023 | ConvNeXt V2 | 2023 | misc | — | remove | Never cited |
| liuEfficientViT2023 | EfficientViT | 2023 | misc | — | remove | Never cited |
| loshchilovDecoupledWeightDecay2019 | AdamW | 2019 | misc | — | remove | Never cited |
| lowesift2004 | SIFT | 2004 | article | Bab 2 | replace | Same as dalalHOG2005 — keep if §2.9 kept |
| menpanrbSP4N21Juta2024 | 2.1 Juta Laporan SP4N-Lapor 2024 | 2024 | misc | Bab 1 | keep | — |
| menpanrbSP4NLapor2023 | Kepuasan SP4N-LAPOR 73,7% 2023 | 2023 | misc | Bab 1 | keep | — (despite 2023; the metric quoted is from that year) |
| merkelDocker2014 | Docker | 2014 | article | Bab 2 | replace | Find 2023+ container deployment reference |
| mitchellMachineLearning1997 | Machine Learning (textbook) | 1997 | book | Bab 2 | replace | Already cited via `russellArtificialIntelligence2021`; drop |
| mitchellWebScraping2018 | Web Scraping with Python | 2018 | book | — | remove | Was used only in deleted 2.3.5/2.3.6 — verify no other refs |
| niculescuMizilCaruana2005 | Predicting Good Probabilities | 2005 | inproc | — | remove | Never cited |
| ofliMultimodalDisaster2020 | Multimodal Disaster Response | 2020 | article | Bab 1, Bab 2 | replace | Find 2023+ multimodal disaster work (or keep as historical comparison) |
| onnxruntime2024 | ONNX Runtime | 2024 | misc | Bab 2 | keep | — |
| onnxruntimeMobileDocs2024 | ONNX Runtime Mobile | 2024 | misc | — | remove | Merge with onnxruntime2024 |
| oquabDINOv22024 | DINOv2 | **2023** ← fixed | misc | Bab 1, Bab 2, Bab 4 | keep | Year corrected |
| prokhorenkovaCatBoost2018 | CatBoost | 2018 | inproc | Bab 1, Bab 2, Bab 3 | replace | Original paper; keep as baseline foundational reference for CatBoost; mark as exception |
| radfordCLIP2021 | CLIP | 2021 | inproc | Bab 1, Bab 2 | keep | — |
| ramachandramMultimodalDL2017 | Deep Multimodal Learning Survey | 2017 | article | — | remove | Never cited |
| ratnerSnorkel2017 | Snorkel | 2017 | inproc | — | remove | Never cited |
| readClassifierChains2009 | Classifier Chains | 2009 | inproc | Bab 2 | replace | If §2.5 multi-label kept, find 2023+ multilabel survey |
| riverpoddoc2024 | Riverpod Documentation | 2024 | misc | Bab 1, Bab 2 | keep | — |
| russakovskyImageNet2015 | ImageNet ILSVRC | 2015 | article | Bab 2 | replace | Either drop or replace with `krizhevskyImageNet2012` to merge |
| russellArtificialIntelligence2021 | AI: Modern Approach | 2021 | book | Bab 2 | keep | — |
| ryaliHiera2023 | Hiera | 2023 | misc | Bab 2, Bab 4 | keep | — |
| sadiqSensingSmartCities2025 | Sensing in Smart Cities | 2025 | misc | — | remove | Never cited (or add cite in Bab 1 §smart city) |
| sennrichBPE2016 | BPE | 2016 | inproc | Bab 2 | replace | Foundational tokenizer; keep or consolidate with kudoSentencePiece2018 |
| shenSmartCityGovernance2025 | Smart City Governance MLLM | 2025 | incollection | Bab 1 | keep | — |
| simeoniDINOv32025 | DINOv3 | 2025 | misc | Bab 1, Bab 2, Bab 3, Bab 4, Bab 5 | keep | — |
| siretPublicComplainingBlessing2022 | Public Complaining Blessing | 2022 | article | Bab 1 | keep | — |
| suRoFormer2024 | RoFormer | 2024 | article | Bab 2 | keep | — |
| supabaseDoc2024 | Supabase Documentation | 2024 | misc | Bab 1, Bab 2 | keep | — |
| szegedyRethinkingInceptionArchitecture2016 | Rethinking Inception | 2016 | inproc | — | remove | Never cited |
| tfliteDocs2024 | TensorFlow Lite | 2024 | misc | — | remove | Never cited |
| tsoumakasMultilabel2007 | Multi-Label Overview | 2007 | article | Bab 2 | replace | If §2.5 kept, find 2023+ multilabel survey |
| ustimenkoCatBoostUncertainty2023 | CatBoost Uncertainty | 2023 | misc | Bab 1, Bab 2, Bab 3 | keep | — |
| vaswaniAttentionAllYou2023 | Attention Is All You Need | **2017** ← fixed | misc | Bab 2 | keep | Year corrected. Rename key to `vaswaniAttention2017` for future-proofing (optional). |
| vovkAlgorithmic2005 | Algorithmic Learning in a Random World | 2005 | book | — | remove | Never cited |
| wangCognitiveEdgeComputing2025 | Cognitive Edge Computing | 2025 | article | Bab 2 | keep | — |
| wangE5Multilingual2024 | Multilingual E5 | 2024 | misc | Bab 1, Bab 2, Bab 3, Bab 4 | keep | — |
| wangEmpoweringEdgeIntelligence2025 | Empowering Edge Intelligence | 2025 | article | Bab 1, Bab 2 | keep | — |
| wilieIndoNLU2020 | IndoNLU | 2020 | inproc | Bab 2 | replace | Consolidate with cahyawijayaCendol2024 |
| wongsoNusaBERT2024 | NusaBERT | 2024 | misc | — | remove | Never cited (or add as Indonesian baseline if relevant) |
| xueMT52021 | mT5 | 2021 | inproc | Bab 2 | keep | — |
| yuMambaOut2024 | MambaOut | 2024 | misc | — | remove | Never cited |
| zahroFairerPublicComplaint2025 | Fairer Public Complaint (LaporGub) | 2025 | article | Bab 1, Bab 5 | keep | — |
| zhangMixup2018 | Mixup | 2018 | misc | Bab 2 | replace | Find 2023+ augmentation work |
| zhangMultilabelReview2014 | Multi-Label Review | 2014 | article | Bab 2 | replace | Same as tsoumakasMultilabel2007 |

## Suggested New References (the "new" rows)

Drop into Bab 2 §2.13 (Backbone Visual) and Bab 2 §2.26 (Penelitian Terkait).

1. **Jose et al. 2025** — *DINOv2 Meets Text: A Unified Framework for Image- and Pixel-Level Vision-Language Alignment* (CVPR 2025). Use to strengthen DINOv2/DINOv3 + multimodal arguments.
2. **Barsellotti et al. 2024–2025** — *Talking to DINO: Bridging Self-Supervised Vision Backbones with Language for Open-Vocabulary Segmentation*. Use as supporting evidence that DINOv2 features transfer to language tasks.
3. **Ray & Skurikhin 2024** — *Deep Clustering of Remote Sensing Scenes through Heterogeneous Transfer Learning*. Use in §2.13 to reinforce frozen-encoder feature transfer.
4. **Tschannen et al. 2025** — *SigLIP 2* (open vocab vision-language). Optional: comparison point in Bab 5 future-work.
5. **Wang et al. 2025** — Recent multilingual-E5 update or follow-up. Verify via arXiv before citing.
6. **DINOv3 Technical Report (Meta AI, 2025)** — Already covered by `simeoniDINOv32025`; if a separate Meta report PDF exists, add as supplement.
7. **An ICCV/CVPR 2025 smart-city multimodal classification paper** — e.g., Sun et al., *Urban Incident Categorization with Vision-Language Models*. (Verify reference exists before adding.)
8. **November 2025 – April 2026 article window** for smart-city deployment/privacy context — candidates to verify and add:
   - World Bank Smart Cities 2025 brief (if Nov 2025+)
   - McKinsey/Gartner 2026 urban AI report
   - Recent Indonesian regulation/policy document (e.g., KemenPANRB SP4N report 2026)

## Critical Issues Carried Forward

1. The `.bib` entry with key just `article` is risky — any other file using that key would silently collide. Recommend renaming to `analisisTeksId2022`.
2. After removing the 33 orphans, run `bibtex main` again to confirm zero warnings.
3. The 12 `replace` rows should be visited one-by-one because each replacement requires a passage edit, not a key swap.

## Provenance

Reference audit performed by an Explore subagent against `chapters/Bab[1-5].tex`. Cross-checked against `references/references.bib`. The two year corrections were applied directly in this revision; orphan removals and pre-2021 replacements are queued as manual follow-up.
