"""
INTERACTIVE CBR MEDICAL DIAGNOSIS SYSTEM
=========================================

File ini menyediakan interface interaktif untuk sistem CBR.
User dapat melakukan diagnosis dengan input manual melalui CLI.
"""

from case_base_system import CaseBasedReasoningSystem
from typing import List
import json


class InteractiveDiagnosisApp:
    """Aplikasi interaktif untuk diagnosis penyakit berbasis CBR"""
    
    def __init__(self):
        self.cbr = CaseBasedReasoningSystem()
        self.history = []
    
    def print_header(self):
        """Tampilkan header aplikasi"""
        print("\n")
        print("╔" + "="*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  🏥 MEDICAL DIAGNOSIS SYSTEM - CASE BASED REASONING".center(68) + "║")
        print("║" + "     Interactive Medical Diagnosis Recommendation".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "="*68 + "╝")
    
    def print_menu(self):
        """Tampilkan menu utama"""
        print("\n" + "="*70)
        print("MENU UTAMA")
        print("="*70)
        print("1. 🔍 Diagnosis Penyakit")
        print("2. 📊 Lihat Statistik Case Base")
        print("3. ➕ Tambah Kasus Baru")
        print("4. 📜 Lihat Riwayat Diagnosis")
        print("5. 🔎 Cari Kasus Spesifik")
        print("6. ⚙️  Pengaturan")
        print("7. ❌ Keluar")
        print("="*70)
    
    def input_symptoms(self) -> List[str]:
        """Input gejala dari user"""
        print("\n" + "-"*70)
        print("MASUKKAN GEJALA PASIEN")
        print("-"*70)
        print("Ketik gejala satu per satu, tekan ENTER setelah setiap gejala")
        print("Ketik 'SELESAI' untuk mengakhiri input gejala")
        print("Contoh: demam tinggi → batuk → lelah → SELESAI")
        print()
        
        symptoms = []
        while True:
            symptom = input(f"Gejala ke-{len(symptoms) + 1}: ").strip()
            
            if symptom.upper() == "SELESAI":
                if symptoms:
                    break
                else:
                    print("⚠️  Minimal harus ada 1 gejala!")
                    continue
            
            if symptom:
                symptoms.append(symptom.lower())
                print(f"   ✓ Gejala ditambahkan: '{symptom}'")
            else:
                print("⚠️  Input tidak boleh kosong!")
        
        return symptoms
    
    def perform_diagnosis(self):
        """Melakukan diagnosis interaktif"""
        print("\n" + "="*70)
        print("PROSES DIAGNOSIS PENYAKIT")
        print("="*70)
        
        # Input gejala
        symptoms = self.input_symptoms()
        
        print("\n✓ Gejala yang dimasukkan:")
        for i, sym in enumerate(symptoms, 1):
            print(f"  {i}. {sym}")
        
        # Proses diagnosis
        print("\n" + "-"*70)
        print("MEMPROSES DIAGNOSIS...")
        print("-"*70)
        
        result = self.cbr.diagnose(symptoms)
        
        # Tampilkan hasil
        print("\n" + "-"*70)
        print("HASIL DIAGNOSIS")
        print("-"*70)
        
        print(f"\n📌 DIAGNOSIS:")
        print(f"   Penyakit: {result.get('diagnosed_disease', 'N/A')}")
        print(f"   Deskripsi: {result.get('diagnosis', 'N/A')}")
        
        print(f"\n⚠️  TINGKAT KEPARAHAN:")
        severity = result.get('severity', 'N/A').upper()
        if severity == 'MILD':
            print(f"   {severity} (Ringan) 🟢")
        elif severity == 'MODERATE':
            print(f"   {severity} (Sedang) 🟡")
        elif severity == 'SEVERE':
            print(f"   {severity} (Berat) 🔴")
        else:
            print(f"   {severity}")
        
        print(f"\n💊 TREATMENT:")
        print(f"   {result.get('treatment', 'N/A')}")
        
        print(f"\n📊 CONFIDENCE SCORE:")
        confidence = result.get('confidence', 0)
        confidence_pct = f"{confidence:.1%}"
        
        # Tampilkan confidence bar
        bar_length = 40
        filled = int(bar_length * confidence)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}] {confidence_pct}")
        
        print(f"\n📈 DETAIL TEKNIS:")
        print(f"   Similarity Score: {result.get('similarity_score', 'N/A')}")
        print(f"   Success Rate: {result.get('success_rate', 0):.1%}")
        print(f"   Matching Case: {result.get('best_matching_case', 'N/A')}")
        
        # Feedback
        print("\n" + "-"*70)
        feedback = input("Apakah diagnosis ini akurat? (y/n): ").strip().lower()
        result['user_feedback'] = feedback == 'y'
        
        if feedback == 'y':
            print("✅ Terima kasih atas konfirmasi Anda!")
        else:
            print("⚠️  Diagnosis perlu review oleh dokter profesional")
        
        # Simpan ke history
        self.history.append({
            'symptoms': symptoms,
            'result': result,
            'feedback': feedback
        })
        
        print("\n✓ Diagnosis telah disimpan dalam riwayat")
        
        return result
    
    def display_statistics(self):
        """Tampilkan statistik case base"""
        print("\n" + "="*70)
        print("STATISTIK CASE BASE")
        print("="*70)
        
        self.cbr.display_statistics()
        
        # Tambahan statistik
        print(f"Total diagnosis dalam sesi ini: {len(self.history)}")
        
        if self.history:
            correct_diagnoses = sum(1 for h in self.history if h['feedback'] == 'y')
            print(f"Diagnosis yang akurat: {correct_diagnoses}/{len(self.history)}")
            print(f"Accuracy: {correct_diagnoses/len(self.history):.1%}")
    
    def add_new_case(self):
        """Tambah kasus baru secara interaktif"""
        print("\n" + "="*70)
        print("TAMBAH KASUS BARU")
        print("="*70)
        
        print("\nForm Pendaftaran Kasus Baru:")
        print("-"*70)
        
        # Input data kasus
        symptoms = self.input_symptoms()
        
        disease_name = input("\nNama penyakit: ").strip()
        if not disease_name:
            print("⚠️  Nama penyakit tidak boleh kosong!")
            return
        
        diagnosis = input("Deskripsi diagnosis: ").strip()
        
        print("\nTingkat Keparahan:")
        print("1. Mild (Ringan)")
        print("2. Moderate (Sedang)")
        print("3. Severe (Berat)")
        severity_choice = input("Pilih (1-3): ").strip()
        severity_map = {'1': 'mild', '2': 'moderate', '3': 'severe'}
        severity = severity_map.get(severity_choice, 'unknown')
        
        treatment = input("Treatment/Obat: ").strip()
        
        try:
            success_rate = float(input("Success Rate (0-1): ").strip())
            if not 0 <= success_rate <= 1:
                print("⚠️  Success rate harus antara 0 dan 1")
                return
        except ValueError:
            print("⚠️  Input tidak valid!")
            return
        
        # Simpan kasus
        case_data = {
            'symptoms': symptoms,
            'disease_name': disease_name,
            'diagnosis': diagnosis,
            'severity': severity,
            'treatment': treatment,
            'success_rate': success_rate
        }
        
        self.cbr.retain(case_data)
        print("\n✅ Kasus baru berhasil ditambahkan!")
    
    def search_cases(self):
        """Cari kasus dengan gejala tertentu"""
        print("\n" + "="*70)
        print("PENCARIAN KASUS")
        print("="*70)
        
        search_symptoms = self.input_symptoms()
        
        print("\n" + "-"*70)
        print("HASIL PENCARIAN")
        print("-"*70)
        
        retrieved = self.cbr.retrieve(search_symptoms, top_k=5)
        
        if not retrieved:
            print("Tidak ada kasus yang ditemukan")
            return
        
        print(f"\nDitemukan {len(retrieved)} kasus yang mirip:\n")
        
        for i, (case, similarity) in enumerate(retrieved, 1):
            print(f"{i}. Case ID: {case.case_id}")
            print(f"   Penyakit: {case.disease_name}")
            print(f"   Gejala: {', '.join(case.symptoms)}")
            print(f"   Kemiripan: {similarity:.1%}")
            print(f"   Success Rate: {case.success_rate:.1%}")
            print()
    
    def show_history(self):
        """Tampilkan riwayat diagnosis"""
        print("\n" + "="*70)
        print("RIWAYAT DIAGNOSIS")
        print("="*70)
        
        if not self.history:
            print("\nBelum ada riwayat diagnosis")
            return
        
        print(f"\nTotal diagnosis: {len(self.history)}\n")
        
        for i, record in enumerate(self.history, 1):
            print(f"--- Diagnosis #{i} ---")
            print(f"Gejala: {', '.join(record['symptoms'])}")
            print(f"Penyakit: {record['result']['diagnosed_disease']}")
            print(f"Confidence: {record['result']['confidence']:.1%}")
            print(f"Feedback: {'✅ Akurat' if record['feedback'] == 'y' else '⚠️  Perlu Review'}")
            print()
        
        # Option untuk export
        export = input("Ingin export riwayat ke file? (y/n): ").strip().lower()
        if export == 'y':
            filename = "diagnosis_history.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            print(f"✅ Riwayat telah disimpan ke {filename}")
    
    def settings(self):
        """Menu pengaturan"""
        print("\n" + "="*70)
        print("PENGATURAN")
        print("="*70)
        print("1. Info Sistem")
        print("2. Export Case Base")
        print("3. Reset Case Base")
        print("4. Kembali")
        print("-"*70)
        
        choice = input("Pilih (1-4): ").strip()
        
        if choice == '1':
            print("\n" + "-"*70)
            print("INFO SISTEM")
            print("-"*70)
            print(f"Total Cases: {len(self.cbr.cases)}")
            print(f"Case Base File: {self.cbr.case_base_file}")
            print("Algoritma: Jaccard Similarity")
            print("Status: ✅ Aktif")
        
        elif choice == '2':
            filename = "case_base_export.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(
                    [{'case_id': c.case_id, 'disease': c.disease_name, 
                      'symptoms': c.symptoms} for c in self.cbr.cases],
                    f, ensure_ascii=False, indent=2
                )
            print(f"\n✅ Case base telah di-export ke {filename}")
        
        elif choice == '3':
            confirm = input("\n⚠️  Apakah Anda yakin ingin reset? (y/n): ").strip().lower()
            if confirm == 'y':
                self.cbr.cases.clear()
                self.cbr._initialize_sample_cases()
                self.cbr.save_case_base()
                print("✅ Case base telah di-reset ke kondisi awal")
    
    def run(self):
        """Jalankan aplikasi"""
        self.print_header()
        
        while True:
            self.print_menu()
            choice = input("\nPilih menu (1-7): ").strip()
            
            if choice == '1':
                self.perform_diagnosis()
            elif choice == '2':
                self.display_statistics()
            elif choice == '3':
                self.add_new_case()
            elif choice == '4':
                self.show_history()
            elif choice == '5':
                self.search_cases()
            elif choice == '6':
                self.settings()
            elif choice == '7':
                print("\n" + "="*70)
                print("Terima kasih telah menggunakan Medical Diagnosis System")
                print("Goodbye! 👋")
                print("="*70 + "\n")
                break
            else:
                print("⚠️  Pilihan tidak valid! Silakan coba lagi.")
            
            input("\nTekan ENTER untuk lanjut...")


def main():
    """Fungsi utama"""
    app = InteractiveDiagnosisApp()
    app.run()


if __name__ == "__main__":
    main()
