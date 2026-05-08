# CONTOH PENGGUNAAN EXTENDED
# File ini berisi contoh-contoh penggunaan yang lebih advanced

"""
ADVANCED USAGE EXAMPLES
=======================

Contoh-contoh penggunaan lebih advanced untuk sistem CBR.
"""

from case_base_system import CaseBasedReasoningSystem
import json

# ============================================================================
# EXAMPLE 1: Custom Diagnosis dengan Threshold
# ============================================================================

def diagnose_with_threshold(symptoms, min_confidence=0.7):
    """
    Diagnosis hanya diterima jika confidence >= threshold
    """
    cbr = CaseBasedReasoningSystem()
    result = cbr.diagnose(symptoms)
    
    confidence = result.get('confidence', 0)
    
    if confidence >= min_confidence:
        print(f"✅ Diagnosis ACCEPTED (confidence: {confidence:.2%})")
        return result
    else:
        print(f"⚠️  Diagnosis REJECTED (confidence: {confidence:.2%} < {min_confidence:.2%})")
        print("   Recommend manual review by doctor")
        return None


# USAGE:
if __name__ == "__main__":
    print("\n" + "="*70)
    print("EXAMPLE 1: Diagnosis dengan Threshold")
    print("="*70)
    
    symptoms = ["demam", "batuk"]
    result = diagnose_with_threshold(symptoms, min_confidence=0.8)
    if result:
        print(f"Penyakit: {result['diagnosed_disease']}")


# ============================================================================
# EXAMPLE 2: Compare Multiple Diagnosis
# ============================================================================

def compare_diagnoses(symptoms):
    """
    Bandingkan multiple diagnosis dan tampilkan ranking
    """
    cbr = CaseBasedReasoningSystem()
    retrieved = cbr.retrieve(symptoms, top_k=5)
    
    print("\n" + "-"*70)
    print("DIAGNOSIS RANKING")
    print("-"*70)
    print(f"{'Rank':<6} {'Disease':<30} {'Similarity':<15} {'Confidence':<12}")
    print("-"*70)
    
    for rank, (case, similarity) in enumerate(retrieved, 1):
        confidence = similarity * case.success_rate
        print(f"{rank:<6} {case.disease_name:<30} {similarity:.1%}{'':>8} {confidence:.1%}{'':>5}")
    
    print("-"*70)


# USAGE:
if __name__ == "__main__":
    print("\n" + "="*70)
    print("EXAMPLE 2: Compare Multiple Diagnosis")
    print("="*70)
    
    symptoms = ["demam tinggi", "batuk"]
    compare_diagnoses(symptoms)


# ============================================================================
# EXAMPLE 3: Batch Diagnosis Processing
# ============================================================================

def batch_diagnose(patient_list):
    """
    Proses diagnosis untuk multiple pasien
    """
    cbr = CaseBasedReasoningSystem()
    results = []
    
    print("\n" + "="*70)
    print("BATCH DIAGNOSIS PROCESSING")
    print("="*70)
    
    for patient_id, symptoms in patient_list:
        print(f"\nProcessing Patient {patient_id}...")
        result = cbr.diagnose(symptoms)
        results.append({
            'patient_id': patient_id,
            'diagnosis': result['diagnosed_disease'],
            'confidence': result['confidence']
        })
    
    return results


# USAGE:
if __name__ == "__main__":
    patients = [
        ("P001", ["demam tinggi", "batuk", "lelah"]),
        ("P002", ["sakit kepala", "mual", "sensitif cahaya"]),
        ("P003", ["ruam merah", "gatal", "bengkak"])
    ]
    
    batch_results = batch_diagnose(patients)
    print("\n" + "-"*70)
    print("BATCH RESULTS SUMMARY")
    print("-"*70)
    for r in batch_results:
        print(f"Patient {r['patient_id']}: {r['diagnosis']} (Confidence: {r['confidence']:.1%})")


# ============================================================================
# EXAMPLE 4: Analyze Case Base Statistics
# ============================================================================

def analyze_case_base():
    """
    Analisis statistik mendalam terhadap case base
    """
    cbr = CaseBasedReasoningSystem()
    
    print("\n" + "="*70)
    print("CASE BASE ANALYSIS")
    print("="*70)
    
    # Total statistics
    total_cases = len(cbr.cases)
    total_symptoms = sum(len(c.symptoms) for c in cbr.cases)
    avg_symptoms_per_case = total_symptoms / total_cases if total_cases > 0 else 0
    
    print(f"\nBasic Statistics:")
    print(f"  Total Cases: {total_cases}")
    print(f"  Total Symptoms: {total_symptoms}")
    print(f"  Avg Symptoms/Case: {avg_symptoms_per_case:.1f}")
    
    # Disease distribution
    disease_dist = {}
    for case in cbr.cases:
        disease_dist[case.disease_name] = disease_dist.get(case.disease_name, 0) + 1
    
    print(f"\nDisease Distribution:")
    for disease, count in sorted(disease_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {disease}: {count} case(s)")
    
    # Severity distribution
    severity_dist = {}
    for case in cbr.cases:
        severity_dist[case.severity] = severity_dist.get(case.severity, 0) + 1
    
    print(f"\nSeverity Distribution:")
    for severity, count in severity_dist.items():
        print(f"  {severity.capitalize()}: {count} case(s)")
    
    # Success rate statistics
    success_rates = [c.success_rate for c in cbr.cases]
    avg_success = sum(success_rates) / len(success_rates) if success_rates else 0
    min_success = min(success_rates) if success_rates else 0
    max_success = max(success_rates) if success_rates else 0
    
    print(f"\nSuccess Rate Statistics:")
    print(f"  Average: {avg_success:.1%}")
    print(f"  Min: {min_success:.1%}")
    print(f"  Max: {max_success:.1%}")
    
    # Symptom frequency
    from collections import Counter
    symptom_freq = Counter()
    for case in cbr.cases:
        symptom_freq.update(case.symptoms)
    
    print(f"\nMost Common Symptoms:")
    for symptom, freq in symptom_freq.most_common(5):
        print(f"  {symptom}: {freq} occurrences")


# USAGE:
if __name__ == "__main__":
    analyze_case_base()


# ============================================================================
# EXAMPLE 5: Export Diagnosis History
# ============================================================================

def export_diagnosis_history(history, filename="diagnosis_export.json"):
    """
    Export riwayat diagnosis ke file JSON
    """
    export_data = []
    
    for i, record in enumerate(history, 1):
        export_data.append({
            'diagnosis_id': f'DX_{i:04d}',
            'symptoms': record['symptoms'],
            'diagnosis': record['result']['diagnosed_disease'],
            'confidence': record['result']['confidence'],
            'feedback': record['feedback'],
            'severity': record['result'].get('severity', 'N/A')
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Diagnosis history exported to {filename}")
    return filename


# ============================================================================
# EXAMPLE 6: Find Similar Cases for a Disease
# ============================================================================

def find_cases_by_disease(disease_name):
    """
    Cari semua kasus untuk penyakit tertentu
    """
    cbr = CaseBasedReasoningSystem()
    
    matching_cases = [c for c in cbr.cases if disease_name.lower() in c.disease_name.lower()]
    
    print(f"\n" + "="*70)
    print(f"CASES FOR: {disease_name}")
    print("="*70)
    
    if not matching_cases:
        print(f"No cases found for '{disease_name}'")
        return []
    
    for case in matching_cases:
        print(f"\nCase ID: {case.case_id}")
        print(f"Disease: {case.disease_name}")
        print(f"Symptoms: {', '.join(case.symptoms)}")
        print(f"Severity: {case.severity}")
        print(f"Success Rate: {case.success_rate:.1%}")
        print(f"Treatment: {case.treatment}")
    
    return matching_cases


# USAGE:
if __name__ == "__main__":
    find_cases_by_disease("Cold")


# ============================================================================
# EXAMPLE 7: Calculate Similarity Matrix
# ============================================================================

def calculate_similarity_matrix():
    """
    Hitung similarity matrix antar semua cases
    """
    cbr = CaseBasedReasoningSystem()
    
    n_cases = len(cbr.cases)
    matrix = [[0.0] * n_cases for _ in range(n_cases)]
    
    print("\nCalculating similarity matrix...")
    
    for i, case_i in enumerate(cbr.cases):
        for j, case_j in enumerate(cbr.cases):
            if i != j:
                similarity = cbr.calculate_similarity(case_i.symptoms, case_j.symptoms)
                matrix[i][j] = similarity
            else:
                matrix[i][j] = 1.0  # Self-similarity = 1
    
    print("\n" + "="*70)
    print("SIMILARITY MATRIX")
    print("="*70)
    
    # Print header
    print(f"{'':>12}", end='')
    for i in range(n_cases):
        print(f"C{i+1:>8}", end='')
    print()
    
    # Print matrix
    for i, row in enumerate(matrix):
        print(f"Case {i+1}{':':>6}", end='')
        for val in row:
            print(f"{val:>8.2f}", end='')
        print()
    
    return matrix


# USAGE:
if __name__ == "__main__":
    calculate_similarity_matrix()


# ============================================================================
# EXAMPLE 8: Confidence Distribution
# ============================================================================

def analyze_confidence_distribution():
    """
    Analisis distribusi confidence scores
    """
    cbr = CaseBasedReasoningSystem()
    
    test_symptoms_list = [
        ["demam", "batuk"],
        ["demam tinggi", "batuk", "lelah"],
        ["sakit kepala", "mual"],
        ["ruam", "gatal"],
        ["sakit perut", "diare"]
    ]
    
    confidences = []
    
    for symptoms in test_symptoms_list:
        result = cbr.diagnose(symptoms)
        confidences.append(result.get('confidence', 0))
    
    print("\n" + "="*70)
    print("CONFIDENCE DISTRIBUTION ANALYSIS")
    print("="*70)
    
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    min_conf = min(confidences) if confidences else 0
    max_conf = max(confidences) if confidences else 0
    
    print(f"\nConfidence Statistics:")
    print(f"  Average: {avg_conf:.2%}")
    print(f"  Minimum: {min_conf:.2%}")
    print(f"  Maximum: {max_conf:.2%}")
    print(f"  Range: {max_conf - min_conf:.2%}")
    
    # Histogram
    bins = [0, 0.5, 0.7, 0.8, 0.9, 1.0]
    hist = [0] * (len(bins) - 1)
    
    for conf in confidences:
        for i in range(len(bins) - 1):
            if bins[i] <= conf < bins[i+1]:
                hist[i] += 1
                break
        else:
            if conf == 1.0:
                hist[-1] += 1
    
    print(f"\nConfidence Distribution Histogram:")
    for i in range(len(bins) - 1):
        lower, upper = bins[i], bins[i+1]
        count = hist[i]
        bar = "█" * count
        print(f"  [{lower:.0%}-{upper:.0%}): {bar} ({count})")


# USAGE:
if __name__ == "__main__":
    analyze_confidence_distribution()


# ============================================================================
# MAIN - Run All Examples
# ============================================================================

if __name__ == "__main__":
    print("\n\n")
    print("╔" + "="*68 + "╗")
    print("║" + "  ADVANCED CBR EXAMPLES".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    # Run all examples
    # diagnose_with_threshold(["demam", "batuk"])
    # compare_diagnoses(["demam tinggi", "batuk"])
    # batch_diagnose([...])
    # analyze_case_base()
    # find_cases_by_disease("Cold")
    # calculate_similarity_matrix()
    # analyze_confidence_distribution()
    
    print("\n✓ Run individual examples by uncommenting in main section")
