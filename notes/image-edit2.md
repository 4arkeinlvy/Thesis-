## Diagram Review Comment — Kerangka Berpikir SmartCityApps

Diagram ini sudah mencakup alur penelitian secara keseluruhan, tetapi masih perlu dirapikan karena beberapa panah diagonal membuat flow terlihat membingungkan. Untuk diagram kerangka berpikir, fokusnya harus menunjukkan alur logis penelitian, bukan detail teknis terlalu dalam.

### Main Issues

1. Ada beberapa panah diagonal panjang yang membuat pembaca sulit mengikuti urutan proses.
2. Flow dari tahap penelitian, training model, deployment backend, aplikasi Android, database, dan pengujian masih terlihat bercampur.
3. Beberapa label terlalu teknis untuk diagram kerangka berpikir, misalnya `split data`, `ONNX`, dan `class + confidence + agency`.
4. Diagram terlihat seperti campuran antara research flow, system architecture, dan implementation flow.
5. Bagian `Supabase menyimpan laporan, prediksi, assignment, evidence` terlalu detail untuk kerangka berpikir utama.
6. Caption sudah bagus, tetapi diagramnya perlu dibuat lebih linear dan defensible.

---

## Revision Instruction

Please revise this diagram so it becomes cleaner, more academic, and easier to defend as a research framework diagram.

### Required Changes

- Make the flow mostly left-to-right or top-to-bottom.
- Avoid long diagonal arrows.
- Group the diagram into 4 main phases:

```text
1. Identifikasi Masalah
2. Pengembangan Model
3. Implementasi Sistem
4. Pengujian dan Evaluasi