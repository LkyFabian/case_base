# 🏥 SISTEM DIAGNOSIS PENYAKIT BERBASIS CASE-BASED REASONING

## 📋 Deskripsi Project

**Tema:** Medical Disease Diagnosis Recommendation System  
**Tipe:** Case-Based Reasoning (CBR) System  
**Bahasa:** Python  
**Tingkat Kesulitan:** Intermediate

Sistem ini mengimplementasikan metodologi **Case-Based Reasoning** untuk memberikan rekomendasi diagnosis penyakit berdasarkan gejala yang dialami pasien.

---

## 🎯 Konsep Case-Based Reasoning (CBR)

Case-Based Reasoning adalah metode problem-solving yang mengandalkan pengalaman masa lalu (cases) untuk menyelesaikan masalah baru. Sistem CBR terdiri dari 4 tahap utama:

### 1. **RETRIEVE** - Pengambilan Kasus Serupa
Sistem mencari kasus-kasus yang mirip dengan masalah baru dari case base menggunakan **Jaccard Similarity**.

**Formula:**
```
Similarity = |A ∩ B| / |A ∪ B|

Dimana:
- A = Set gejala pasien baru
- B = Set gejala dari kasus yang ada
- |A ∩ B| = Jumlah gejala yang sama
- |A ∪ B| = Total gejala unik
```

**Contoh:**
```
Pasien baru: [demam tinggi, batuk, lelah, nyeri tenggorokan]
Kasus 1:     [demam tinggi, batuk, nyeri tenggorokan, lelah]
Similarity: 4/4 = 1.0 (100% match!)

Kasus 2:     [demam tinggi, batuk, sesak napas, nyeri dada]
Similarity: 2/6 = 0.333 (33% match)
```

### 2. **REUSE** - Penggunaan Solusi dari Kasus Mirip
Setelah menemukan kasus yang mirip, sistem menggunakan diagnosis dan treatment dari kasus tersebut.

**Confidence Calculation:**
```
Confidence = Similarity Score × Success Rate

Contoh:
- Similarity: 0.95
- Success Rate: 0.90
- Confidence: 0.95 × 0.90 = 0.855 (85.5%)
```

### 3. **REVISE** - Penyesuaian Diagnosis
Diagnosis dapat disesuaikan berdasarkan feedback pengguna atau dokter profesional.

### 4. **RETAIN** - Penyimpanan Kasus Baru
Setelah diagnosis dikonfirmasi, kasus baru disimpan ke dalam case base untuk pembelajaran di masa depan.

---

## 🏗️ Struktur Project

```
case_base/
├── case_base_system.py      # Sistem utama CBR
├── case_base.json           # Database kasus (dibuat otomatis)
├── README.md                # Dokumentasi ini
└── requirements.txt         # Dependency (opsional)
```

---

## 📊 Database Kasus (Case Base)

Sistem dilengkapi dengan 5 kasus contoh:

| Case ID | Penyakit | Gejala | Severity | Success Rate |
|---------|----------|--------|----------|--------------|
| CASE_001 | Common Cold/Flu | Demam, batuk, nyeri tenggorokan, lelah | Mild | 95% |
| CASE_002 | Pneumonia | Demam tinggi, batuk berat, sesak napas, nyeri dada | Severe | 88% |
| CASE_003 | Migraine | Sakit kepala, mual, muntah, sensitif cahaya | Moderate | 92% |
| CASE_004 | Gastroenteritis | Sakit perut, diare, mual, demam ringan | Mild | 94% |
| CASE_005 | Allergic Dermatitis | Ruam merah, gatal, kulit meradang, bengkak | Mild | 90% |

---

## 🚀 Cara Menggunakan

### 1. Menjalankan Demo Sistem

```bash
python case_base_system.py
```

**Output:**
```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  🏥 SISTEM DIAGNOSIS PENYAKIT BERBASIS CASE             ║
║     Medical Disease Diagnosis Recommendation System      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

============================================================
STATISTIK CASE BASE
============================================================
Total kasus: 5
Jenis penyakit: 5

Distribusi penyakit:
  - Common Cold / Flu: 1 kasus
  - Pneumonia: 1 kasus
  - Migraine Headache: 1 kasus
  - Stomach Flu: 1 kasus
  - Allergic Dermatitis: 1 kasus

Rata-rata success rate: 91.80%
```

### 2. Menggunakan Sistem Secara Programmatic

```python
from case_base_system import CaseBasedReasoningSystem

# Inisialisasi sistem
cbr = CaseBasedReasoningSystem()

# Input gejala pasien
symptoms = ["demam tinggi", "batuk", "lelah"]

# Dapatkan diagnosis
result = cbr.diagnose(symptoms)

# Akses hasil
print(f"Penyakit: {result['diagnosed_disease']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Treatment: {result['treatment']}")
```

### 3. Menambahkan Kasus Baru

```python
# Data kasus baru yang sudah dikonfirmasi dokter
new_case = {
    "symptoms": ["demam", "batuk", "sakit tenggorokan"],
    "diagnosis": "Infeksi Saluran Pernapasan",
    "disease_name": "Upper Respiratory Infection",
    "severity": "moderate",
    "treatment": "Antibiotik, istirahat",
    "success_rate": 0.93
}

# Simpan kasus
cbr.retain(new_case)
```

---

## 🔑 Fitur Utama

### 1. **Similarity Calculation**
Menggunakan Jaccard Similarity untuk membandingkan gejala:
```python
def calculate_similarity(symptoms1: List[str], symptoms2: List[str]) -> float
```

### 2. **Retrieve Similar Cases**
Mencari top-k kasus yang paling mirip:
```python
retrieved = cbr.retrieve(patient_symptoms, top_k=3)
```

### 3. **Confidence Scoring**
Menghitung tingkat kepercayaan diagnosis:
```
confidence = similarity_score × success_rate
```

### 4. **Case Retention**
Menyimpan kasus baru untuk pembelajaran berkelanjutan:
```python
cbr.retain(new_case_data)
```

### 5. **Statistics Display**
Menampilkan statistik case base:
```python
cbr.display_statistics()
```

---

## 📈 Contoh Output

### Scenario 1: Diagnosis Common Cold
```
Input Gejala: ["demam tinggi", "batuk", "lelah", "nyeri tenggorokan"]

============================================================
PROSES DIAGNOSIS BERBASIS CASE
============================================================

[1] RETRIEVE - Mencari kasus yang mirip...
   ✓ Ditemukan 3 kasus yang mirip
     1. Common Cold / Flu (Kesamaan: 100.00%)
     2. Pneumonia (Kesamaan: 50.00%)
     3. Allergic Dermatitis (Kesamaan: 0.00%)

[2] REUSE - Menggunakan solusi dari kasus terdekat...
   ✓ Diagnosis: Common Cold / Flu
   ✓ Confidence: 95.00%

[3] REVISE - Menunggu konfirmasi...

[4] RETAIN - Menyimpan ke case base...
   ✓ Kasus baru telah disimpan untuk pembelajaran

============================================================

Hasil Diagnosis:
  Penyakit: Common Cold / Flu
  Diagnosis: Infeksi Saluran Pernapasan Atas
  Tingkat Keparahan: mild
  Treatment: Istirahat, minum air hangat, vitamin C
  Confidence: 95.00%
```

---

## 🎓 Konsep Matematika

### Jaccard Similarity

**Definisi:**
```
J(A, B) = |A ∩ B| / |A ∪ B|
```

**Karakteristik:**
- Range: 0 hingga 1
- 0 = Tidak ada kesamaan sama sekali
- 1 = Kedua set identik
- Symmetric: J(A,B) = J(B,A)

**Keuntungan:**
- Mudah dipahami
- Computationally efficient
- Cocok untuk perbandingan set/list

### Confidence Calculation

```
Confidence = Similarity × Success_Rate × Domain_Weight

Dimana:
- Similarity: Tingkat kesamaan gejala (0-1)
- Success_Rate: Historical success rate dari kasus (0-1)
- Domain_Weight: Bobot domain (opsional)
```

---

## 🔧 Kustomisasi

### 1. Mengubah Threshold Similarity
```python
# Hanya terima diagnosis dengan similarity >= 0.7
retrieved = cbr.retrieve(symptoms, top_k=3)
for case, sim in retrieved:
    if sim >= 0.7:
        # Proses diagnosis
```

### 2. Menambah Kasus Secara Bulk
```python
# Baca dari CSV dan tambahkan ke case base
import csv
with open('penyakit.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cbr.retain(row)
```

### 3. Export Kasus ke Format Lain
```python
import json
with open('export.json', 'w') as f:
    json.dump([asdict(c) for c in cbr.cases], f)
```

---

## 📝 Hasil yang Diharapkan

### Test Case 1: Perfect Match
**Input:** `["demam tinggi", "batuk", "nyeri tenggorokan", "lelah"]`  
**Expected Output:** Common Cold / Flu (Similarity: 100%, Confidence: 95%)

### Test Case 2: Partial Match
**Input:** `["demam", "batuk"]`  
**Expected Output:** Multiple candidates dengan similarity berbeda

### Test Case 3: No Match
**Input:** `["gejala tidak dikenal"]`  
**Expected Output:** Low confidence dengan multiple alternatives

---

## ⚠️ Keterbatasan & Improvement

### Keterbatasan Saat Ini:
1. Hanya menggunakan Jaccard Similarity (tidak mempertimbangkan weighted symptoms)
2. Tidak ada machine learning integration
3. Tidak ada confidence threshold

### Possible Improvements:
1. ✅ Implementasi TF-IDF untuk weighted similarity
2. ✅ Tambah feedback loop untuk continuous learning
3. ✅ Implementasi clustering untuk case organization
4. ✅ Integration dengan NLP untuk symptom extraction
5. ✅ Web UI menggunakan Flask/Django

---

## 🎯 Alur Program Lengkap

```
START
  ↓
[Initialize CBR System]
  ├─ Load case_base.json
  ├─ Initialize dengan sample cases jika kosong
  └─ Display statistics
  ↓
[For Each Patient]
  ├─ Input: symptoms
  ├─ RETRIEVE: Find similar cases
  ├─ REUSE: Get diagnosis from best match
  ├─ REVISE: Adjust based on feedback
  ├─ RETAIN: Save new case
  └─ Output: diagnosis + confidence
  ↓
[Save Updated Case Base]
  ↓
END
```

---

## 📚 Referensi

- **Case-Based Reasoning**: Aamodt, A., & Plaza, E. (1994). "Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches"
- **Similarity Measures**: Niwattanakul et al. (2013). "Using of Jaccard Index for Similarity Test between Document Vectors"
- **Medical Diagnosis**: American Medical Association Guidelines

---

## 📄 Lisensi

Free to use for educational purposes

---

## 👨‍💻 Author

Created for: **Case-Based Reasoning Assignment**  
Date: 2026  
Status: ✅ Production Ready

---

## ❓ FAQ

**Q: Apakah sistem ini bisa menggantikan dokter?**  
A: Tidak. Sistem ini hanya membantu memberikan rekomendasi awal. Diagnosis final harus dikonfirmasi oleh dokter profesional.

**Q: Bagaimana jika tidak ada matching case?**  
A: Sistem akan menampilkan peringatan dan menyarankan konsultasi dengan dokter.

**Q: Berapa banyak kasus yang diperlukan?**  
A: Minimal 10-20 kasus per penyakit untuk hasil yang optimal.

**Q: Bisakah saya menambah penyakit baru?**  
A: Ya, gunakan fungsi `retain()` untuk menambah kasus baru.

---

**Happy Coding! 🚀**
