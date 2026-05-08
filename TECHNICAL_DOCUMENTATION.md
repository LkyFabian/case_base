# 📐 DOKUMENTASI TEKNIS & MATEMATIS

## Case-Based Reasoning Implementation Guide

---

## 1. KONSEP DASAR CBR

### 1.1 Definisi
Case-Based Reasoning (CBR) adalah metodologi problem-solving yang menggunakan pengalaman masa lalu (cases) untuk menyelesaikan masalah baru. 

**Prinsip Dasar:**
> "Masalah serupa memiliki solusi yang serupa"

### 1.2 Arsitektur CBR (4 Tahap)

```
┌─────────────────────────────────────────────────────┐
│         PROBLEM CASE (Kasus Baru)                  │
│     Symptoms: [demam, batuk, lelah]               │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │    1. RETRIEVE        │
          │ (Cari Kasus Mirip)    │
          └───────────┬───────────┘
                      │
        ┌─────────────▼────────────────┐
        │  Matched Cases:              │
        │  • Case1 (Sim: 95%)         │
        │  • Case2 (Sim: 50%)         │
        │  • Case3 (Sim: 30%)         │
        └─────────────┬────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │    2. REUSE           │
          │ (Gunakan Solusi)      │
          └───────────┬───────────┘
                      │
        ┌─────────────▼────────────────┐
        │  Recommended Solution:       │
        │  • Disease: Common Cold      │
        │  • Treatment: Rest & Fluids  │
        │  • Confidence: 85.5%         │
        └─────────────┬────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │    3. REVISE          │
          │ (Sesuaikan Solusi)    │
          └───────────┬───────────┘
                      │
        ┌─────────────▼────────────────┐
        │  Revised Solution:           │
        │  (After User Feedback)       │
        └─────────────┬────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │    4. RETAIN          │
          │ (Simpan Kasus Baru)   │
          └───────────┬───────────┘
                      │
        ┌─────────────▼────────────────┐
        │  Case Base Updated:          │
        │  CASE_006 Added              │
        └──────────────────────────────┘
```

---

## 2. ALGORITMA SIMILARITY - JACCARD SIMILARITY

### 2.1 Definisi Matematis

**Jaccard Similarity (Jaccard Index):**
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

Dimana:
- $A$ = Set gejala dari kasus yang ada
- $B$ = Set gejala dari pasien baru
- $|A \cap B|$ = Jumlah gejala yang sama
- $|A \cup B|$ = Total gejala unik

### 2.2 Karakteristik

| Properti | Nilai |
|----------|-------|
| Range | [0, 1] |
| Symmetric | $J(A,B) = J(B,A)$ |
| Reflexive | $J(A,A) = 1$ |
| Disjoint | $J(A,B) = 0$ jika $A \cap B = \emptyset$ |

### 2.3 Contoh Perhitungan

**Kasus 1: Perfect Match**
```
Pasien baru:  {demam, batuk, lelah, nyeri_tenggorokan}
Kasus 1:      {demam, batuk, lelah, nyeri_tenggorokan}

Intersection: {demam, batuk, lelah, nyeri_tenggorokan} → 4 elemen
Union:        {demam, batuk, lelah, nyeri_tenggorokan} → 4 elemen

Similarity = 4/4 = 1.0 (100%)
```

**Kasus 2: Partial Match**
```
Pasien baru:  {demam, batuk, lelah}
Kasus 2:      {demam, batuk, sesak_napas}

Intersection: {demam, batuk} → 2 elemen
Union:        {demam, batuk, lelah, sesak_napas} → 4 elemen

Similarity = 2/4 = 0.5 (50%)
```

**Kasus 3: No Match**
```
Pasien baru:  {demam, batuk}
Kasus 3:      {ruam, gatal}

Intersection: {} → 0 elemen
Union:        {demam, batuk, ruam, gatal} → 4 elemen

Similarity = 0/4 = 0.0 (0%)
```

### 2.4 Implementasi Python

```python
def calculate_similarity(symptoms1: List[str], symptoms2: List[str]) -> float:
    """
    Hitung Jaccard Similarity antara dua set gejala
    
    Args:
        symptoms1: List gejala pasien baru
        symptoms2: List gejala dari kasus yang ada
    
    Returns:
        Jaccard Similarity score (0-1)
    """
    # Normalisasi (lowercase dan strip whitespace)
    set1 = set(s.lower().strip() for s in symptoms1)
    set2 = set(s.lower().strip() for s in symptoms2)
    
    # Handle edge case
    if not set1 and not set2:
        return 1.0
    
    # Hitung intersection dan union
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    # Return Jaccard Similarity
    return intersection / union if union > 0 else 0
```

### 2.5 Kompleksitas Komputasi

**Time Complexity:**
- Creating sets: $O(n)$ where $n$ = total symptoms
- Set operations: $O(\min(n_1, n_2))$
- **Total: $O(n)$**

**Space Complexity: $O(n)$**

Sangat efisien untuk dataset berukuran normal!

---

## 3. RETRIEVE - CASE RETRIEVAL

### 3.1 Algoritma

```
FUNCTION retrieve(patient_symptoms, top_k):
    similarities = []
    
    FOR EACH case IN case_base:
        similarity = calculate_similarity(patient_symptoms, case.symptoms)
        similarities.append((case, similarity))
    
    // Urutkan descending
    similarities.SORT(key=similarity, reverse=True)
    
    // Kembalikan top-k
    RETURN similarities[:top_k]
```

### 3.2 Pseudo-code Detail

```
Algorithm: RETRIEVE
Input: patient_symptoms (list), top_k (integer)
Output: list of (case, similarity) sorted by similarity DESC

BEGIN
    candidates ← []
    
    // Langkah 1: Hitung similarity untuk semua cases
    FOR each_case IN case_base DO
        sim ← calculate_similarity(patient_symptoms, each_case.symptoms)
        candidates.append((each_case, sim))
    END FOR
    
    // Langkah 2: Sort by similarity descending
    candidates.sort(sim, DESC)
    
    // Langkah 3: Return top-k
    RETURN candidates[0:top_k]
END
```

### 3.3 Contoh Eksekusi

**Input:**
```
Patient symptoms: [demam tinggi, batuk, lelah]
Top-k: 3
```

**Proses:**
```
Case 1: Similarity = 1.0 → (Case_001, 1.0)
Case 2: Similarity = 0.5 → (Case_002, 0.5)
Case 3: Similarity = 0.0 → (Case_003, 0.0)
Case 4: Similarity = 0.67 → (Case_004, 0.67)
Case 5: Similarity = 0.33 → (Case_005, 0.33)

Sorted:
1. (Case_001, 1.0)   ← Best match
2. (Case_004, 0.67)  
3. (Case_002, 0.5)
```

**Output:** Top 3 cases

---

## 4. REUSE - SOLUTION REUSE & CONFIDENCE CALCULATION

### 4.1 Algoritma

```
Algorithm: REUSE
Input: retrieved_cases (list of (case, similarity))
Output: diagnosis_recommendation (dict)

BEGIN
    IF retrieved_cases is empty THEN
        RETURN {status: "no_match"}
    END IF
    
    best_case, best_similarity ← retrieved_cases[0]
    
    // Hitung confidence
    confidence ← best_similarity × best_case.success_rate
    
    diagnosis ← {
        status: "success",
        disease: best_case.disease_name,
        treatment: best_case.treatment,
        severity: best_case.severity,
        similarity: best_similarity,
        success_rate: best_case.success_rate,
        confidence: confidence
    }
    
    RETURN diagnosis
END
```

### 4.2 Confidence Score Calculation

**Formula:**
$$C = S \times R$$

Dimana:
- $C$ = Confidence Score (0-1)
- $S$ = Similarity Score (0-1)
- $R$ = Historical Success Rate (0-1)

**Interpretasi:**
- $C \geq 0.8$ : High confidence (80%)
- $0.5 \leq C < 0.8$ : Medium confidence
- $C < 0.5$ : Low confidence

**Contoh:**
```
Similarity: 0.95 (95%)
Success Rate: 0.90 (90%)
Confidence: 0.95 × 0.90 = 0.855 (85.5%)
```

### 4.3 Multi-Case Aggregation (Optional)

Jika ingin menggunakan multiple cases:

**Weighted Average:**
$$C_{avg} = \frac{\sum_{i=1}^{k} w_i \times c_i}{\sum_{i=1}^{k} w_i}$$

Dimana:
- $w_i$ = weight (biasanya similarity)
- $c_i$ = confidence dari case ke-i
- $k$ = number of cases

---

## 5. REVISE - DIAGNOSIS ADJUSTMENT

### 5.1 Algoritma

```
Algorithm: REVISE
Input: diagnosis (dict), user_feedback (boolean)
Output: revised_diagnosis (dict)

BEGIN
    IF user_feedback is TRUE THEN
        diagnosis.status ← "CONFIRMED"
        diagnosis.revised ← FALSE
    ELSE
        diagnosis.status ← "NEEDS_REVISION"
        diagnosis.revised ← TRUE
        diagnosis.confidence ← diagnosis.confidence × 0.5  // Reduce confidence
    END IF
    
    RETURN diagnosis
END
```

### 5.2 Feedback Integration

```python
# Positive feedback
result = revise(diagnosis, user_feedback=True)
# → confidence unchanged
# → status = CONFIRMED

# Negative feedback  
result = revise(diagnosis, user_feedback=False)
# → confidence reduced
# → status = NEEDS_REVISION
# → requires doctor review
```

---

## 6. RETAIN - CASE LEARNING

### 6.1 Algoritma

```
Algorithm: RETAIN
Input: case_data (dict), user_feedback (boolean)
Output: new_case (MedicalCase)

BEGIN
    // Generate unique ID
    new_id ← "CASE_" + (case_base.length + 1)
    
    // Create new case
    new_case ← MedicalCase(
        case_id: new_id,
        symptoms: case_data.symptoms,
        diagnosis: case_data.diagnosis,
        disease_name: case_data.disease_name,
        severity: case_data.severity,
        treatment: case_data.treatment,
        success_rate: case_data.success_rate,
        date_recorded: current_datetime()
    )
    
    // Add to case base
    case_base.append(new_case)
    
    // Persist to storage
    save_case_base()
    
    RETURN new_case
END
```

### 6.2 Case Structure

```json
{
    "case_id": "CASE_006",
    "symptoms": ["demam", "batuk", "lelah"],
    "diagnosis": "Common Cold",
    "disease_name": "Upper Respiratory Infection",
    "severity": "mild",
    "treatment": "Rest and fluids",
    "success_rate": 0.95,
    "date_recorded": "2026-05-03T10:30:00"
}
```

---

## 7. COMPLETE CBR PIPELINE

### 7.1 Pseudocode Lengkap

```
Algorithm: DIAGNOSE (Complete CBR Pipeline)
Input: patient_symptoms (list)
Output: diagnosis_result (dict)

BEGIN
    // ============ RETRIEVE ============
    PRINT "Step 1: RETRIEVE - Finding similar cases..."
    retrieved_cases ← retrieve(patient_symptoms, top_k=3)
    
    IF retrieved_cases is empty THEN
        diagnosis_result ← {status: "no_match"}
        RETURN diagnosis_result
    END IF
    
    PRINT retrieved_cases
    
    // ============ REUSE ============
    PRINT "Step 2: REUSE - Using solution from best match..."
    diagnosis_result ← reuse(retrieved_cases)
    
    PRINT diagnosis_result
    
    // ============ REVISE ============
    PRINT "Step 3: REVISE - Waiting for confirmation..."
    user_feedback ← get_user_input("Is diagnosis correct? (y/n)")
    diagnosis_result ← revise(diagnosis_result, user_feedback)
    
    PRINT diagnosis_result
    
    // ============ RETAIN ============
    IF user_feedback is TRUE THEN
        PRINT "Step 4: RETAIN - Saving case to case base..."
        new_case ← retain({
            symptoms: patient_symptoms,
            diagnosis: diagnosis_result.diagnosis,
            disease_name: diagnosis_result.disease_name,
            severity: diagnosis_result.severity,
            treatment: diagnosis_result.treatment,
            success_rate: calculate_success_rate(diagnosis_result)
        })
        
        PRINT "Case " + new_case.case_id + " saved successfully"
    END IF
    
    RETURN diagnosis_result
END
```

### 7.2 Flowchart

```
                 START
                   │
                   ▼
        ┌─────────────────────┐
        │  Input: Symptoms    │
        └─────────────────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ [1] RETRIEVE        │
        │ Find Similar Cases  │
        └─────────────────────┘
                   │
         ┌─────────┴─────────┐
         │ Cases Found?      │
         │                   │
         NO                 YES
         │                   │
         ▼                   ▼
      Return             ┌──────────────┐
      No Match    │ [2] REUSE        │
                  │ Get Diagnosis    │
                  └──────────────────┘
                          │
                          ▼
                  ┌──────────────────┐
                  │ [3] REVISE       │
                  │ Adjust Solution  │
                  └──────────────────┘
                          │
                          ▼
                  ┌──────────────────┐
                  │ Get Feedback     │
                  │ (Correct?)       │
                  └──────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
             YES                      NO
              │                       │
              ▼                       ▼
        ┌──────────────┐      ┌──────────────┐
        │ [4] RETAIN   │      │ Manual       │
        │ Save Case    │      │ Review by    │
        └──────────────┘      │ Doctor      │
              │               └──────────────┘
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                     ┌─────────┐
                     │   END   │
                     └─────────┘
```

---

## 8. COMPLEXITY ANALYSIS

### 8.1 Time Complexity

| Operation | Complexity | Remarks |
|-----------|-----------|---------|
| calculate_similarity | $O(n)$ | n = total symptoms |
| retrieve (single case) | $O(n)$ | n = avg symptoms per case |
| retrieve (all cases) | $O(m \times n)$ | m = cases, n = avg symptoms |
| retrieve + sort | $O(m \times n + m \log m)$ | Dominated by sort |
| reuse | $O(1)$ | Constant time |
| revise | $O(1)$ | Constant time |
| retain | $O(1)$ | Constant time (disk I/O negligible) |
| **Full diagnose** | **$O(m \times n + m \log m)$** | Dominated by retrieve+sort |

### 8.2 Space Complexity

| Component | Space | Remarks |
|-----------|-------|---------|
| Case base | $O(m \times n)$ | m cases, n symptoms each |
| Temp sets | $O(n)$ | For similarity calculation |
| Retrieved cases | $O(k)$ | k = top_k |
| **Total** | **$O(m \times n)$** | Case base dominates |

### 8.3 Performance Metrics

**Untuk 1000 cases, 10 symptoms rata-rata:**
- Single retrieve: ~1ms
- Full diagnose: ~100ms
- Retrieve + sort: ~50ms

**Skalabilitas: Excellent untuk dataset kecil-menengah**

---

## 9. IMPROVEMENTS & VARIATIONS

### 9.1 Weighted Similarity

$$S_w = \frac{\sum_{i=1}^{n} w_i \times m_i}{\sum_{i=1}^{n} w_i}$$

Dimana:
- $w_i$ = weight dari gejala ke-i
- $m_i$ = match indicator (0 atau 1)

### 9.2 TF-IDF Similarity

$$S_{tfidf} = \frac{\sum_{i} tfidf(s_i) \times tfidf(c_i)}{\sqrt{\sum tfidf(s_i)^2} \times \sqrt{\sum tfidf(c_i)^2}}$$

### 9.3 Cosine Similarity

$$S_{cos} = \frac{A \cdot B}{||A|| \times ||B||}$$

---

## 10. TESTING & VALIDATION

### 10.1 Unit Test Cases

```python
# Test 1: Identical symptoms
assert calculate_similarity([a,b,c], [a,b,c]) == 1.0

# Test 2: Completely different
assert calculate_similarity([a,b], [x,y]) == 0.0

# Test 3: Partial match
assert calculate_similarity([a,b,c], [a,b,x]) == 2/4 == 0.5

# Test 4: Case insensitive
assert calculate_similarity([A,B], [a,b]) == 1.0

# Test 5: Empty list
assert calculate_similarity([], []) == 1.0
```

### 10.2 Performance Test

```python
import time

symptoms = ["gejala_" + str(i) for i in range(10)]
start = time.time()

for _ in range(1000):
    cbr.diagnose(symptoms)

elapsed = time.time() - start
print(f"1000 diagnoses in {elapsed:.2f}s")
# Expected: < 1 second
```

---

## 11. REFERENSI MATEMATIS

### Bibliography

1. **Aamodt, A., & Plaza, E. (1994).** "Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches." *AICOM*, 7(1), 39-59.

2. **Niwattanakul, S., et al. (2013).** "Using of Jaccard Index for Similarity Test between Document Vectors." *ICTIM*.

3. **Jaccard, P. (1901).** "Distribution de la flore alpine dans le bassin des Dranses et dans quelques régions voisines." *Bulletin de la Société Vaudoise des Sciences Naturelles*, 37, 241-272.

---

**End of Technical Documentation**
