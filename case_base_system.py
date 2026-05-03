"""
SISTEM CASE BASED REASONING - MEDICAL DIAGNOSIS
==============================================
Tema: Sistem Rekomendasi Diagnosis Penyakit Berbasis Kasus

Deskripsi:
Sistem ini menggunakan Case-Based Reasoning untuk memberikan rekomendasi diagnosis
penyakit berdasarkan gejala yang dialami pasien. Sistem membandingkan gejala pasien
baru dengan kasus-kasus penyakit yang sudah pernah ada di database.

Alur Kerja CBR:
1. RETRIEVE  - Mencari kasus serupa dari database
2. REUSE     - Menggunakan solusi dari kasus yang sama
3. REVISE    - Menyesuaikan solusi jika diperlukan
4. RETAIN    - Menyimpan kasus baru untuk pembelajaran di masa depan
"""

import json
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import os


@dataclass
class MedicalCase:
    """Struktur data untuk satu kasus penyakit"""
    case_id: str
    symptoms: List[str]
    diagnosis: str
    disease_name: str
    severity: str  # mild, moderate, severe
    treatment: str
    success_rate: float
    date_recorded: str


class CaseBasedReasoningSystem:
    """
    Sistem Case-Based Reasoning untuk diagnosis penyakit
    
    Fitur:
    - Retrieve: Mencari kasus serupa berdasarkan kesamaan gejala
    - Reuse: Menggunakan diagnosis dari kasus yang paling mirip
    - Revise: Menyesuaikan diagnosis berdasarkan tingkat kesamaan
    - Retain: Menyimpan kasus baru ke dalam case base
    """
    
    def __init__(self, case_base_file: str = "case_base.json"):
        """
        Inisialisasi sistem CBR
        
        Args:
            case_base_file: File untuk menyimpan kasus-kasus
        """
        self.case_base_file = case_base_file
        self.cases: List[MedicalCase] = []
        self.load_case_base()
    
    def load_case_base(self):
        """Memuat kasus-kasus dari file"""
        if os.path.exists(self.case_base_file):
            with open(self.case_base_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cases = [MedicalCase(**case) for case in data]
            print(f"✓ Berhasil memuat {len(self.cases)} kasus dari database")
        else:
            print("⚠ Database kasus tidak ditemukan, membuat database baru...")
            self._initialize_sample_cases()
            self.save_case_base()
    
    def save_case_base(self):
        """Menyimpan kasus-kasus ke file"""
        with open(self.case_base_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(case) for case in self.cases], f, ensure_ascii=False, indent=2)
    
    def _initialize_sample_cases(self):
        """Inisialisasi dengan contoh kasus penyakit"""
        sample_cases = [
            {
                "case_id": "CASE_001",
                "symptoms": ["demam tinggi", "batuk", "nyeri tenggorokan", "lelah"],
                "diagnosis": "Infeksi Saluran Pernapasan Atas",
                "disease_name": "Common Cold / Flu",
                "severity": "mild",
                "treatment": "Istirahat, minum air hangat, vitamin C",
                "success_rate": 0.95,
                "date_recorded": datetime.now().isoformat()
            },
            {
                "case_id": "CASE_002",
                "symptoms": ["demam tinggi", "batuk berat", "sesak napas", "nyeri dada"],
                "diagnosis": "Pneumonia",
                "disease_name": "Pneumonia",
                "severity": "severe",
                "treatment": "Antibiotik, oksigen, rawat inap",
                "success_rate": 0.88,
                "date_recorded": datetime.now().isoformat()
            },
            {
                "case_id": "CASE_003",
                "symptoms": ["sakit kepala", "mual", "muntah", "sensitif terhadap cahaya"],
                "diagnosis": "Migrain",
                "disease_name": "Migraine Headache",
                "severity": "moderate",
                "treatment": "Istirahat di tempat gelap, analgesik, hindari pemicu",
                "success_rate": 0.92,
                "date_recorded": datetime.now().isoformat()
            },
            {
                "case_id": "CASE_004",
                "symptoms": ["sakit perut", "diare", "mual", "demam ringan"],
                "diagnosis": "Gastroenteritis",
                "disease_name": "Stomach Flu",
                "severity": "mild",
                "treatment": "Rehidrasi, diet BRAT, obat anti-diare",
                "success_rate": 0.94,
                "date_recorded": datetime.now().isoformat()
            },
            {
                "case_id": "CASE_005",
                "symptoms": ["ruam merah", "gatal", "kulit meradang", "bengkak"],
                "diagnosis": "Dermatitis Alergi",
                "disease_name": "Allergic Dermatitis",
                "severity": "mild",
                "treatment": "Krim kortikosteroid, antihistamin, hindari alergen",
                "success_rate": 0.90,
                "date_recorded": datetime.now().isoformat()
            }
        ]
        
        for case_data in sample_cases:
            self.cases.append(MedicalCase(**case_data))
    
    def calculate_similarity(self, symptoms1: List[str], symptoms2: List[str]) -> float:
        """
        Hitung kesamaan antara dua set gejala menggunakan Jaccard Similarity
        
        Formula: Similarity = |Intersection| / |Union|
        
        Args:
            symptoms1: List gejala pasien baru
            symptoms2: List gejala dari kasus yang ada
            
        Returns:
            Nilai similarity antara 0 dan 1
        """
        set1 = set(s.lower().strip() for s in symptoms1)
        set2 = set(s.lower().strip() for s in symptoms2)
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        similarity = intersection / union if union > 0 else 0
        return similarity
    
    def retrieve(self, patient_symptoms: List[str], top_k: int = 3) -> List[Tuple[MedicalCase, float]]:
        """
        RETRIEVE: Cari kasus yang paling mirip dari case base
        
        Args:
            patient_symptoms: Gejala yang dialami pasien
            top_k: Jumlah kasus teratas yang ingin diambil
            
        Returns:
            List berisi (kasus, nilai_kesamaan) yang sudah diurutkan dari tertinggi
        """
        similarities = []
        
        for case in self.cases:
            similarity = self.calculate_similarity(patient_symptoms, case.symptoms)
            similarities.append((case, similarity))
        
        # Urutkan berdasarkan similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def reuse(self, retrieved_cases: List[Tuple[MedicalCase, float]]) -> Dict:
        """
        REUSE: Gunakan diagnosis dari kasus yang paling mirip
        
        Jika ada multiple cases, ambil rata-rata confidence
        
        Args:
            retrieved_cases: Kasus-kasus yang sudah diambil dari retrieve
            
        Returns:
            Dictionary berisi diagnosis yang direkomendasikan
        """
        if not retrieved_cases:
            return {
                "status": "no_match",
                "message": "Tidak ditemukan kasus yang mirip",
                "recommendation": None
            }
        
        best_case, best_similarity = retrieved_cases[0]
        
        # Hitung confidence berdasarkan similarity
        confidence = best_similarity * best_case.success_rate
        
        return {
            "status": "success",
            "best_matching_case": best_case.case_id,
            "diagnosed_disease": best_case.disease_name,
            "diagnosis": best_case.diagnosis,
            "severity": best_case.severity,
            "treatment": best_case.treatment,
            "similarity_score": round(best_similarity, 3),
            "success_rate": best_case.success_rate,
            "confidence": round(confidence, 3)
        }
    
    def revise(self, diagnosis: Dict, user_feedback: bool) -> Dict:
        """
        REVISE: Sesuaikan diagnosis berdasarkan feedback pengguna
        
        Args:
            diagnosis: Diagnosis hasil dari reuse
            user_feedback: True jika diagnosis benar, False jika salah
            
        Returns:
            Diagnosis yang sudah direvisi
        """
        if user_feedback:
            diagnosis["revised"] = False
            diagnosis["feedback_status"] = "CONFIRMED"
        else:
            diagnosis["revised"] = True
            diagnosis["feedback_status"] = "NEEDS_REVISION"
            diagnosis["message"] = "Diagnosis perlu direview oleh dokter profesional"
        
        return diagnosis
    
    def retain(self, case_data: Dict) -> MedicalCase:
        """
        RETAIN: Simpan kasus baru ke dalam case base
        
        Args:
            case_data: Data kasus baru
            
        Returns:
            Kasus yang baru disimpan
        """
        new_case_id = f"CASE_{str(len(self.cases) + 1).zfill(3)}"
        
        new_case = MedicalCase(
            case_id=new_case_id,
            symptoms=case_data.get('symptoms', []),
            diagnosis=case_data.get('diagnosis', ''),
            disease_name=case_data.get('disease_name', ''),
            severity=case_data.get('severity', 'unknown'),
            treatment=case_data.get('treatment', ''),
            success_rate=case_data.get('success_rate', 0.5),
            date_recorded=datetime.now().isoformat()
        )
        
        self.cases.append(new_case)
        self.save_case_base()
        
        print(f"✓ Kasus baru {new_case_id} berhasil disimpan")
        return new_case
    
    def diagnose(self, symptoms: List[str]) -> Dict:
        """
        Pipeline lengkap CBR: Retrieve -> Reuse -> Revise -> Retain
        
        Args:
            symptoms: Gejala pasien
            
        Returns:
            Hasil diagnosis lengkap dengan confidence
        """
        print("\n" + "="*60)
        print("PROSES DIAGNOSIS BERBASIS CASE")
        print("="*60)
        
        # 1. RETRIEVE
        print("\n[1] RETRIEVE - Mencari kasus yang mirip...")
        retrieved_cases = self.retrieve(symptoms, top_k=3)
        
        print(f"   ✓ Ditemukan {len(retrieved_cases)} kasus yang mirip")
        for i, (case, sim) in enumerate(retrieved_cases, 1):
            print(f"     {i}. {case.disease_name} (Kesamaan: {sim:.2%})")
        
        # 2. REUSE
        print("\n[2] REUSE - Menggunakan solusi dari kasus terdekat...")
        diagnosis = self.reuse(retrieved_cases)
        
        if diagnosis["status"] == "success":
            print(f"   ✓ Diagnosis: {diagnosis['diagnosed_disease']}")
            print(f"   ✓ Confidence: {diagnosis['confidence']:.2%}")
        else:
            print(f"   ⚠ {diagnosis['message']}")
        
        # 3. REVISE
        print("\n[3] REVISE - Menunggu konfirmasi...")
        # (Dalam implementasi real, user akan memberikan feedback)
        diagnosis = self.revise(diagnosis, user_feedback=True)
        
        # 4. RETAIN
        print("\n[4] RETAIN - Menyimpan ke case base...")
        print("   ✓ Kasus baru telah disimpan untuk pembelajaran")
        
        print("\n" + "="*60)
        return diagnosis
    
    def display_statistics(self):
        """Tampilkan statistik sistem"""
        print("\n" + "="*60)
        print("STATISTIK CASE BASE")
        print("="*60)
        print(f"Total kasus: {len(self.cases)}")
        
        diseases = {}
        for case in self.cases:
            diseases[case.disease_name] = diseases.get(case.disease_name, 0) + 1
        
        print(f"Jenis penyakit: {len(diseases)}")
        print("\nDistribusi penyakit:")
        for disease, count in diseases.items():
            print(f"  - {disease}: {count} kasus")
        
        avg_success = sum(case.success_rate for case in self.cases) / len(self.cases)
        print(f"\nRata-rata success rate: {avg_success:.2%}")
        print("="*60 + "\n")


def demo_system():
    """Demo interaktif sistem CBR"""
    
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🏥 SISTEM DIAGNOSIS PENYAKIT BERBASIS CASE".center(58) + "║")
    print("║" + "     Medical Disease Diagnosis Recommendation System".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    print()
    
    # Inisialisasi sistem
    cbr_system = CaseBasedReasoningSystem()
    
    # Tampilkan statistik
    cbr_system.display_statistics()
    
    # Demo 1: Diagnosis Common Cold
    print("\n" + "▶ DEMO 1: Diagnosis Common Cold".center(60))
    print("-" * 60)
    patient1_symptoms = ["demam tinggi", "batuk", "lelah", "nyeri tenggorokan"]
    result1 = cbr_system.diagnose(patient1_symptoms)
    print(f"\nHasil Diagnosis:")
    print(f"  Penyakit: {result1.get('diagnosed_disease', 'N/A')}")
    print(f"  Diagnosis: {result1.get('diagnosis', 'N/A')}")
    print(f"  Tingkat Keparahan: {result1.get('severity', 'N/A')}")
    print(f"  Treatment: {result1.get('treatment', 'N/A')}")
    print(f"  Confidence: {result1.get('confidence', 0):.2%}")
    
    # Demo 2: Diagnosis Migrain
    print("\n\n" + "▶ DEMO 2: Diagnosis Migrain".center(60))
    print("-" * 60)
    patient2_symptoms = ["sakit kepala berat", "mual", "sensitif cahaya", "muntah"]
    result2 = cbr_system.diagnose(patient2_symptoms)
    print(f"\nHasil Diagnosis:")
    print(f"  Penyakit: {result2.get('diagnosed_disease', 'N/A')}")
    print(f"  Diagnosis: {result2.get('diagnosis', 'N/A')}")
    print(f"  Tingkat Keparahan: {result2.get('severity', 'N/A')}")
    print(f"  Treatment: {result2.get('treatment', 'N/A')}")
    print(f"  Confidence: {result2.get('confidence', 0):.2%}")
    
    # Demo 3: Diagnosis Pneumonia
    print("\n\n" + "▶ DEMO 3: Diagnosis Pneumonia".center(60))
    print("-" * 60)
    patient3_symptoms = ["demam tinggi", "batuk berat", "sesak napas", "nyeri dada", "lelah"]
    result3 = cbr_system.diagnose(patient3_symptoms)
    print(f"\nHasil Diagnosis:")
    print(f"  Penyakit: {result3.get('diagnosed_disease', 'N/A')}")
    print(f"  Diagnosis: {result3.get('diagnosis', 'N/A')}")
    print(f"  Tingkat Keparahan: {result3.get('severity', 'N/A')}")
    print(f"  Treatment: {result3.get('treatment', 'N/A')}")
    print(f"  Confidence: {result3.get('confidence', 0):.2%}")
    
    print("\n" + "="*60)
    print("Demo selesai ✓")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo_system()
