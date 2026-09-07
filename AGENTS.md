# AGENTS.md — Mode Senior Developer Efisien (Ponytail Philosophy)

Aturan ini dirancang untuk semua AI Agent yang bekerja dalam proyek ini. Filosofi utama berbasis pada aturan **Ponytail**: *Lazy Senior Dev Mode*. 
"Lazy" (malas) di sini berarti **efisien, pragmatis, dan hemat kode**, bukan ceroboh. Kode terbaik adalah kode yang tidak pernah perlu ditulis.

---

## 1. Tangga Keputusan Sebelum Menulis Kode (The Decision Ladder)

Sebelum menulis atau menambahkan kode baru, ikuti urutan langkah berikut (hentikan pada langkah pertama yang terpenuhi):

1. **Apakah ini benar-benar perlu dibuat? (YAGNI - You Ain't Gonna Need It)**
   - Jangan buat fitur antisipasi masa depan yang belum diminta.
2. **Apakah fungsi ini sudah ada di dalam codebase?**
   - Gunakan kembali (reuse) helper, utility, atau pola yang sudah ada. Jangan tulis ulang.
3. **Apakah Standard Library bahasa/framework sudah memilikinya?**
   - Utamakan fitur bawaan runtime / standard library.
4. **Apakah fitur native platform sudah mencakupnya?**
   - Manfaatkan kapabilitas native platform jika ada.
5. **Apakah dependency/package yang sudah terinstall bisa menyelesaikannya?**
   - Gunakan library yang sudah terpasang sebelum menambah library baru.
6. **Bisakah dibuat menjadi 1 baris kode sederhana?**
   - Jika ya, buat 1 baris yang jelas dan mudah dibaca.
7. **Langkah Terakhir:** Tulis kode minimal yang bekerja dengan benar.

> **Catatan:** Tangga keputusan ini dijalankan *setelah* Anda memahami masalah secara mendalam, bukan sebagai alasan untuk memotong pemahaman.

---

## 2. Aturan Utama Pengembangan Kode (Core Rules)

- **Tanpa Abstraksi Berlebihan:** Jangan buat interface, class wrapper, factory, atau layer ekstra kecuali diminta secara eksplisit atau benar-benar dibutuhkan.
- **Hapus > Tambah:** Utamakan penghapusan/penyederhanaan kode dibanding menambah baris baru. Kode sederhana & membosankan lebih baik daripada kode yang "terlalu cerdas" (clever).
- **Hindari Boilerplate:** Jangan tambahkan boilerplate berlebihan yang tidak diminta.
- **Diff Terpendek Wins:** Perubahan dengan jumlah baris/file tersedikit yang bekerja dengan benar adalah pemenangnya.
- **Pertanyakan Permintaan Kompleks:** Jika ada instruksi yang rumit, tanyakan atau pertimbangkan: *"Apakah Anda benar-benar butuh solusi X, atau solusi Y yang lebih sederhana sudah cukup?"*
- **Penanganan Edge-Case:** Pilih pendekatan standard library yang menangani edge-case dengan tepat meskipun ada alternatif lain yang seukuran.

---

## 3. Perbaikan Bug (Bug Fixing Guidelines)

- **Selesaikan Akar Masalah (Root Cause), Bukan Gejala (Symptom):** Laporan bug biasanya hanya menyebutkan gejala.
- **Trace Semua Pemanggil (Callers):** Sebelum mengubah fungsi shared, periksa seluruh caller fungsi tersebut (`grep`/search callers). Perbaiki di fungsi pusat satu kali agar semua path terlindungi, daripada memasang *patch* di satu caller yang dilaporkan.

---

## 4. Hal-Hal yang TIDAK Boleh Dikompromikan (Non-Negotiables)

Meskipun mengutamakan efisiensi, Anda **TIDAK BOLEH "malas"** pada poin-poin berikut:

1. **Memahami Masalah:** Baca tugas dan pelajari kode terkait secara menyeluruh sebelum mengeksekusi.
2. **Validasi Input:** Wajib melakukan validasi input pada batas kepercayaan (*trust boundaries* seperti API endpoint, form input, external data).
3. **Penanganan Error:** Error handling harus mencegah kehilangan data (*data loss*) atau crash yang tak terduga.
4. **Keamanan & Aksesibilitas:** Standar keamanan (seperti OWASP, proteksi injection, sanitasi) dan aksesibilitas tidak boleh diabaikan.
5. **Verifikasi & Pengujian (Runnable Check):**
   - Setiap logika non-trivial WAJIB memiliki setidaknya **satu tes/pemeriksaan yang dapat dijalankan** (runnable check/unit test) untuk membuktikan logika berfungsi.
   - Kode satu baris (trivial) tidak memerlukan unit test khusus.

---

## 5. Catatan Penyederhanaan Sengaja (`ponytail:` Tag)

Jika Anda secara sengaja melakukan penyederhanaan sementara yang memiliki batas kemampuan tertentu (misal: *O(n²) scan*, *global lock*, *naive heuristic*):

- Tandai baris tersebut dengan komentar `# ponytail:` atau `// ponytail:`
- Sebutkan batasan teknisnya dan jalur peningkatannya (*upgrade path*).
- *Contoh:* `// ponytail: O(n^2) scan acceptable for <= 100 items; upgrade to indexed lookup if collection grows.`

---

## 6. Alur Kerja Agent (Agent Workflow)

1. **Eksplorasi & Pahami:** Baca instruksi, telusuri kode terkait, pahami arsitektur proyek.
2. **Rencanakan:** Buat rencana kerja yang ringkas sebelum melakukan perubahan besar.
3. **Implementasi Hemat Kode:** Terapkan perubahan sesuai *Decision Ladder*.
4. **Verifikasi:** Jalankan unit test / linter / build check untuk memastikan tidak ada deviasi atau bug baru.
5. **Konfirmasi:** Pastikan hasil bersih, terverifikasi, dan siap di-merge.
