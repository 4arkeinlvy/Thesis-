## Diagram Review Comment — Make It Cleaner and More Defensible

Diagram sudah menjelaskan alur besar server-side inference, tetapi masih perlu dibuat lebih clean dan mudah dibaca oleh dosen penguji.

### Main Issues
1. Judul terlalu panjang. Singkatkan agar lebih akademik dan tidak memenuhi area atas diagram.
2. Arrow diagonal dari `Konkatenasi vektor 2048d` ke `CatBoost + PGS` terlalu panjang dan membuat diagram terlihat berantakan.
3. Bahasa masih campur antara Indonesia dan English. Gunakan satu gaya bahasa secara konsisten.
4. Bagian `CatBoost + PGS (ONNX) softmax 9 kelas instansi prediksi + confidence` terlalu padat. Pecah atau sederhanakan wording.
5. Label `Jalur Citra` dan `Jalur Teks` sudah bagus, tetapi posisinya bisa dirapikan agar sejajar dengan masing-masing pipeline.
6. Catatan bawah terlalu kecil dan panjang. Buat lebih singkat atau pindahkan ke caption thesis.
7. Perlu ditegaskan bahwa routing terdekat adalah **proses backend setelah inference**, bukan bagian dari model klasifikasi.
8. Pastikan nama model benar dan konsisten dengan thesis/code. Jika di eksperimen memakai DINOv2, jangan tulis DINOv3.

---

## Revision Instruction

Please revise the diagram to be cleaner, more concise, and easier to defend in thesis presentation.

### Required Changes
- Shorten the title to:

```text
Alur Inferensi Server-Side SmartCityApps