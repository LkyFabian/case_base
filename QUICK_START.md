# QUICK START GUIDE
# 🚀 Panduan Cepat Memulai

## Instalasi & Menjalankan Program

### Persyaratan
- Python 3.7+
- Tidak ada library eksternal yang diperlukan (Pure Python)

### Setup

#### Opsi 1: Jalankan Demo Otomatis
```bash
python case_base_system.py
```

Output yang diharapkan:
```
╔══════════════════════════════════════════════════════════╗
║  🏥 SISTEM DIAGNOSIS PENYAKIT BERBASIS CASE              ║
║     Medical Disease Diagnosis Recommendation System      ║
╚══════════════════════════════════════════════════════════╝

✓ Berhasil memuat 5 kasus dari database

============================================================
STATISTIK CASE BASE
============================================================
Total kasus: 5
...
```

#### Opsi 2: Jalankan Aplikasi Interaktif
```bash
python interactive_app.py
```

Ini akan membuka menu interaktif dimana Anda bisa:
- Melakukan diagnosis manual
- Menambah kasus baru
- Melihat riwayat diagnosis
- Export data

#### Opsi 3: Jalankan Unit Tests
```bash
python test_cbr.py
```

Output:
```
test_case_insensitive_comparison (__main__.TestSimilarityCalculation) ... ok
test_completely_different_symptoms (__main__.TestSimilarityCalculation) ... ok
test_empty_symptoms (___main__.TestSimilarityCalculation) ... ok
...

============================================================
TEST SUMMARY
============================================================
Tests run: 30
Successes: 30
Failures: 0
Errors: 0
============================================================
```

---

## Struktur File

```
📁 case_base/
├── 📄 case_base_system.py          ← Sistem utama CBR
├── 📄 interactive_app.py            ← Aplikasi interaktif
├── 📄 test_cbr.py                  ← Unit tests
├── 📄 README.md                    ← Dokumentasi lengkap
├── 📄 TECHNICAL_DOCUMENTATION.md   ← Dokumentasi teknis
├── 📄 QUICK_START.md               ← File ini
├── 📄 case_base.json               ← Database kasus (dibuat otomatis)
└── 📄 requirements.txt             ← Dependencies
```

---

## Penggunaan Programmatic

### Contoh 1: Diagnosis Sederhana

```python
from case_base_system import CaseBasedReasoningSystem

# Inisialisasi
cbr = CaseBasedReasoningSystem()

# Input gejala
symptoms = ["demam tinggi", "batuk", "lelah"]

# Diagnosis
result = cbr.diagnose(symptoms)

# Output
print(f"Penyakit: {result['diagnosed_disease']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Treatment: {result['treatment']}")
```

**Output:**
```
Penyakit: Common Cold / Flu
Confidence: 85.50%
Treatment: Istirahat, minum air hangat, vitamin C
```

### Contoh 2: Retrieve Kasus Mirip

```python
# Cari kasus yang mirip
symptoms = ["demam", "batuk"]
retrieved = cbr.retrieve(symptoms, top_k=3)

for case, similarity in retrieved:
    print(f"{case.disease_name}: {similarity:.1%} match")
```

**Output:**
```
Common Cold / Flu: 100.0% match
Pneumonia: 50.0% match
Gastroenteritis: 0.0% match
```

### Contoh 3: Tambah Kasus Baru

```python
new_case = {
    "symptoms": ["demam", "sakit perut", "diare"],
    "diagnosis": "Gastroenteritis",
    "disease_name": "Stomach Infection",
    "severity": "moderate",
    "treatment": "Rehidrasi dan obat anti-diare",
    "success_rate": 0.92
}

cbr.retain(new_case)
print("Kasus baru disimpan!")
```

### Contoh 4: Statistik

```python
# Tampilkan statistik
cbr.display_statistics()

# Access raw data
print(f"Total cases: {len(cbr.cases)}")

for case in cbr.cases:
    print(f"- {case.disease_name} ({case.case_id})")
```

---

## Menu Interaktif

Ketika menjalankan `interactive_app.py`, Anda akan melihat menu:

```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║  🏥 MEDICAL DIAGNOSIS SYSTEM - CASE BASED REASONING               ║
║     Interactive Medical Diagnosis Recommendation                  ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

======================================================================
MENU UTAMA
======================================================================
1. 🔍 Diagnosis Penyakit
2. 📊 Lihat Statistik Case Base
3. ➕ Tambah Kasus Baru
4. 📜 Lihat Riwayat Diagnosis
5. 🔎 Cari Kasus Spesifik
6. ⚙️  Pengaturan
7. ❌ Keluar
======================================================================

Pilih menu (1-7): 
```

### Menu 1: Diagnosis Penyakit
- Input gejala satu per satu
- Sistem akan mencari kasus mirip
- Menampilkan diagnosis dengan confidence
- Ask for feedback

### Menu 2: Statistik
- Total kasus di database
- Distribusi penyakit
- Average success rate

### Menu 3: Tambah Kasus
- Input penyakit baru
- Input symptoms
- Input treatment
- Sistem otomatis simpan

### Menu 4: Riwayat
- Lihat semua diagnosis yang pernah dilakukan
- Export ke JSON

### Menu 5: Pencarian
- Cari kasus berdasarkan symptoms
- Lihat kemiripan dengan database

### Menu 6: Pengaturan
- Info sistem
- Export case base
- Reset ke default

---

## Workflow Tipikal

### Scenario: Diagnosis Penyakit Pasien

**Step 1: Inisialisasi**
```python
from case_base_system import CaseBasedReasoningSystem
cbr = CaseBasedReasoningSystem()
```

**Step 2: Input Gejala**
```
Gejala pasien:
- Demam tinggi
- Batuk berat
- Sesak napas
- Nyeri dada
```

**Step 3: RETRIEVE**
```
Mencari 3 kasus paling mirip...
✓ Case 001: Common Cold (Similarity: 50%)
✓ Case 002: Pneumonia (Similarity: 95%)  ← Best match!
✓ Case 003: Flu (Similarity: 60%)
```

**Step 4: REUSE**
```
Menggunakan solusi dari Case 002:
- Penyakit: Pneumonia
- Severity: Severe
- Treatment: Antibiotik, oksigen, rawat inap
- Success Rate: 88%
- Confidence: 95% × 88% = 83.6%
```

**Step 5: REVISE**
```
Dokter mengkonfirmasi diagnosis: ✓ Benar
```

**Step 6: RETAIN**
```
Menyimpan sebagai Case 006 untuk pembelajaran:
- Symptoms, diagnosis, treatment semua disimpan
- Success rate diupdate berdasarkan outcome
```

---

## Data Format

### Case JSON Format
```json
{
    "case_id": "CASE_001",
    "symptoms": ["demam tinggi", "batuk", "nyeri tenggorokan", "lelah"],
    "diagnosis": "Infeksi Saluran Pernapasan Atas",
    "disease_name": "Common Cold / Flu",
    "severity": "mild",
    "treatment": "Istirahat, minum air hangat, vitamin C",
    "success_rate": 0.95,
    "date_recorded": "2026-05-03T10:30:00.123456"
}
```

### Diagnosis Result Format
```json
{
    "status": "success",
    "best_matching_case": "CASE_001",
    "diagnosed_disease": "Common Cold / Flu",
    "diagnosis": "Infeksi Saluran Pernapasan Atas",
    "severity": "mild",
    "treatment": "Istirahat, minum air hangat, vitamin C",
    "similarity_score": 0.95,
    "success_rate": 0.95,
    "confidence": 0.9025
}
```

---

## Troubleshooting

### Problem: `ModuleNotFoundError`
**Solution:** Pastikan Anda berada di direktori yang tepat
```bash
cd "c:\Fabian\Kuliah\Semester 8\kecerdasan buatan\case base"
python case_base_system.py
```

### Problem: `case_base.json not found`
**Solution:** File ini akan dibuat otomatis saat pertama kali run

### Problem: Diagnosis confidence sangat rendah
**Solution:** 
- Case base mungkin masih kecil
- Tambahkan lebih banyak kasus dengan `retain()`
- Gejala pasien mungkin unik

---

## Tips & Tricks

### 1. Batch Import Cases
```python
import csv

with open('diseases.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cbr.retain(row)
```

### 2. Calculate Accuracy
```python
correct = sum(1 for h in app.history if h['feedback'] == 'y')
accuracy = correct / len(app.history)
print(f"Accuracy: {accuracy:.1%}")
```

### 3. Export Case Base
```python
import json

with open('export.json', 'w') as f:
    json.dump([{
        'id': c.case_id,
        'disease': c.disease_name,
        'symptoms': c.symptoms,
        'success_rate': c.success_rate
    } for c in cbr.cases], f)
```

### 4. Analyze Symptoms
```python
from collections import Counter

symptoms_count = Counter()
for case in cbr.cases:
    symptoms_count.update(case.symptoms)

print(symptoms_count.most_common(10))
```

---

## Performance Tuning

### 1. Reduce Top-K
```python
# Instead of top 5, use top 3
retrieved = cbr.retrieve(symptoms, top_k=3)
```

### 2. Add Symptom Weighting
```python
# For future enhancement
weights = {
    'demam tinggi': 1.0,
    'batuk': 0.8,
    'lelah': 0.5
}
```

### 3. Batch Processing
```python
for symptoms_batch in batch_symptoms:
    result = cbr.diagnose(symptoms_batch)
    # Process result
```

---

## Next Steps

1. **Read Full Documentation**
   - README.md (konsep CBR)
   - TECHNICAL_DOCUMENTATION.md (matematis)

2. **Explore the Code**
   - case_base_system.py (main logic)
   - interactive_app.py (UI)
   - test_cbr.py (test cases)

3. **Customize**
   - Tambah penyakit baru
   - Implementasi weighted similarity
   - Integrasikan dengan database

4. **Deploy**
   - Wrap dengan Flask/Django untuk web
   - Integrasikan dengan mobile app
   - Connect dengan medical database

---

## Resources

- **Jaccard Similarity**: https://en.wikipedia.org/wiki/Jaccard_index
- **Case-Based Reasoning**: https://en.wikipedia.org/wiki/Case-based_reasoning
- **Similarity Measures**: https://en.wikipedia.org/wiki/Similarity_measure

---

## FAQ

**Q: Bisakah saya modifikasi algorithm?**  
A: Ya! Anda bisa mengganti `calculate_similarity()` dengan algorithm lain.

**Q: Bagaimana menambah lebih banyak penyakit?**  
A: Edit file `case_base.json` atau gunakan menu "Tambah Kasus Baru" di app interaktif.

**Q: Apakah sistem ini akurat?**  
A: Accuracy tergantung jumlah cases dan quality feedback. Sistem ini untuk educational purposes.

---

## Support

Untuk pertanyaan atau issue, silakan check:
1. README.md - Dokumentasi lengkap
2. TECHNICAL_DOCUMENTATION.md - Penjelasan matematis
3. test_cbr.py - Test cases sebagai contoh

---

**Happy Learning! 🎓**
