"""
TEST SUITE UNTUK CASE BASED REASONING SYSTEM
=============================================

File ini berisi unit tests untuk memverifikasi semua komponen CBR bekerja dengan baik.
"""

import unittest
from case_base_system import CaseBasedReasoningSystem, MedicalCase
from datetime import datetime


class TestSimilarityCalculation(unittest.TestCase):
    """Test untuk perhitungan similarity"""
    
    def setUp(self):
        self.cbr = CaseBasedReasoningSystem()
    
    def test_identical_symptoms(self):
        """Test: Gejala yang identik harus return 1.0"""
        symptoms1 = ["demam", "batuk", "lelah"]
        symptoms2 = ["demam", "batuk", "lelah"]
        
        similarity = self.cbr.calculate_similarity(symptoms1, symptoms2)
        
        self.assertEqual(similarity, 1.0)
    
    def test_completely_different_symptoms(self):
        """Test: Gejala yang berbeda sama sekali harus return 0.0"""
        symptoms1 = ["demam", "batuk"]
        symptoms2 = ["ruam", "gatal"]
        
        similarity = self.cbr.calculate_similarity(symptoms1, symptoms2)
        
        self.assertEqual(similarity, 0.0)
    
    def test_partial_match_symptoms(self):
        """Test: Gejala yang sebagian cocok"""
        symptoms1 = ["demam", "batuk", "lelah"]
        symptoms2 = ["demam", "batuk", "sesak napas"]
        
        # Intersection: {demam, batuk} = 2
        # Union: {demam, batuk, lelah, sesak napas} = 4
        # Expected: 2/4 = 0.5
        similarity = self.cbr.calculate_similarity(symptoms1, symptoms2)
        
        self.assertEqual(similarity, 0.5)
    
    def test_case_insensitive_comparison(self):
        """Test: Perbandingan case-insensitive"""
        symptoms1 = ["Demam", "Batuk"]
        symptoms2 = ["demam", "batuk"]
        
        similarity = self.cbr.calculate_similarity(symptoms1, symptoms2)
        
        self.assertEqual(similarity, 1.0)
    
    def test_whitespace_handling(self):
        """Test: Handling whitespace"""
        symptoms1 = ["  demam  ", "batuk  "]
        symptoms2 = ["demam", "  batuk"]
        
        similarity = self.cbr.calculate_similarity(symptoms1, symptoms2)
        
        self.assertEqual(similarity, 1.0)
    
    def test_empty_symptoms(self):
        """Test: Handle empty symptoms"""
        symptoms1 = []
        symptoms2 = []
        
        similarity = self.cbr.calculate_similarity(symptoms1, symptoms2)
        
        self.assertEqual(similarity, 1.0)


class TestRetrieve(unittest.TestCase):
    """Test untuk retrieve functionality"""
    
    def setUp(self):
        self.cbr = CaseBasedReasoningSystem()
    
    def test_retrieve_returns_sorted_results(self):
        """Test: Retrieve mengembalikan hasil yang diurutkan"""
        symptoms = ["demam tinggi", "batuk", "lelah"]
        
        retrieved = self.cbr.retrieve(symptoms, top_k=3)
        
        # Verify similarity score sorted descending
        similarities = [sim for _, sim in retrieved]
        self.assertEqual(similarities, sorted(similarities, reverse=True))
    
    def test_retrieve_respects_top_k(self):
        """Test: Retrieve mengembalikan top-k results"""
        symptoms = ["demam"]
        
        retrieved_3 = self.cbr.retrieve(symptoms, top_k=3)
        retrieved_5 = self.cbr.retrieve(symptoms, top_k=5)
        
        self.assertLessEqual(len(retrieved_3), 3)
        self.assertLessEqual(len(retrieved_5), 5)
    
    def test_retrieve_returns_case_and_similarity(self):
        """Test: Retrieve returns tuples of (case, similarity)"""
        symptoms = ["demam", "batuk"]
        
        retrieved = self.cbr.retrieve(symptoms, top_k=1)
        
        self.assertTrue(len(retrieved) > 0)
        case, similarity = retrieved[0]
        self.assertIsInstance(case, MedicalCase)
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 1)


class TestReuse(unittest.TestCase):
    """Test untuk reuse functionality"""
    
    def setUp(self):
        self.cbr = CaseBasedReasoningSystem()
    
    def test_reuse_with_valid_cases(self):
        """Test: Reuse menghasilkan diagnosis yang valid"""
        symptoms = ["demam tinggi", "batuk", "lelah"]
        retrieved = self.cbr.retrieve(symptoms, top_k=3)
        
        result = self.cbr.reuse(retrieved)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('diagnosed_disease', result)
        self.assertIn('diagnosis', result)
        self.assertIn('treatment', result)
        self.assertIn('confidence', result)
    
    def test_reuse_confidence_calculation(self):
        """Test: Confidence calculation correctness"""
        symptoms = ["demam tinggi", "batuk", "nyeri tenggorokan", "lelah"]
        retrieved = self.cbr.retrieve(symptoms, top_k=1)
        
        result = self.cbr.reuse(retrieved)
        
        case, similarity = retrieved[0]
        expected_confidence = similarity * case.success_rate
        
        self.assertAlmostEqual(result['confidence'], expected_confidence, places=2)
    
    def test_reuse_with_empty_cases(self):
        """Test: Reuse handles empty case list"""
        result = self.cbr.reuse([])
        
        self.assertEqual(result['status'], 'no_match')


class TestRevise(unittest.TestCase):
    """Test untuk revise functionality"""
    
    def setUp(self):
        self.cbr = CaseBasedReasoningSystem()
    
    def test_revise_with_positive_feedback(self):
        """Test: Revise dengan feedback positif"""
        diagnosis = {'status': 'success', 'diagnosed_disease': 'Common Cold'}
        
        revised = self.cbr.revise(diagnosis, user_feedback=True)
        
        self.assertEqual(revised['feedback_status'], 'CONFIRMED')
        self.assertFalse(revised['revised'])
    
    def test_revise_with_negative_feedback(self):
        """Test: Revise dengan feedback negatif"""
        diagnosis = {'status': 'success', 'diagnosed_disease': 'Common Cold'}
        
        revised = self.cbr.revise(diagnosis, user_feedback=False)
        
        self.assertEqual(revised['feedback_status'], 'NEEDS_REVISION')
        self.assertTrue(revised['revised'])


class TestRetain(unittest.TestCase):
    """Test untuk retain functionality"""
    
    def setUp(self):
        self.cbr = CaseBasedReasoningSystem()
        self.initial_count = len(self.cbr.cases)
    
    def test_retain_adds_case_to_base(self):
        """Test: Retain menambah kasus ke case base"""
        case_data = {
            'symptoms': ['gejala1', 'gejala2'],
            'diagnosis': 'Test Diagnosis',
            'disease_name': 'Test Disease',
            'severity': 'mild',
            'treatment': 'Test Treatment',
            'success_rate': 0.8
        }
        
        self.cbr.retain(case_data)
        
        self.assertEqual(len(self.cbr.cases), self.initial_count + 1)
    
    def test_retain_generates_unique_case_id(self):
        """Test: Retain menghasilkan unique case ID"""
        case_data = {
            'symptoms': ['gejala1'],
            'diagnosis': 'Test',
            'disease_name': 'Test',
            'severity': 'mild',
            'treatment': 'Test',
            'success_rate': 0.8
        }
        
        case1 = self.cbr.retain(case_data)
        case2 = self.cbr.retain(case_data)
        
        self.assertNotEqual(case1.case_id, case2.case_id)


class TestDiagnose(unittest.TestCase):
    """Test untuk full diagnose pipeline"""
    
    def setUp(self):
        self.cbr = CaseBasedReasoningSystem()
    
    def test_diagnose_common_cold(self):
        """Test: Full pipeline untuk Common Cold diagnosis"""
        symptoms = ["demam tinggi", "batuk", "lelah", "nyeri tenggorokan"]
        
        result = self.cbr.diagnose(symptoms)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['status'], 'success')
        self.assertIn('diagnosed_disease', result)
    
    def test_diagnose_pneumonia(self):
        """Test: Full pipeline untuk Pneumonia diagnosis"""
        symptoms = ["demam tinggi", "batuk berat", "sesak napas", "nyeri dada"]
        
        result = self.cbr.diagnose(symptoms)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['diagnosed_disease'], 'Pneumonia')
    
    def test_diagnose_with_partial_symptoms(self):
        """Test: Diagnose dengan partial symptoms"""
        symptoms = ["demam", "batuk"]
        
        result = self.cbr.diagnose(symptoms)
        
        self.assertIsNotNone(result)
        self.assertIn('confidence', result)


class TestEdgeCases(unittest.TestCase):
    """Test untuk edge cases"""
    
    def setUp(self):
        self.cbr = CaseBasedReasoningSystem()
    
    def test_empty_symptoms_list(self):
        """Test: Handle empty symptoms list"""
        symptoms = []
        
        # Should not raise exception
        retrieved = self.cbr.retrieve(symptoms, top_k=1)
        
        self.assertIsInstance(retrieved, list)
    
    def test_very_long_symptoms_list(self):
        """Test: Handle very long symptoms list"""
        symptoms = [f"gejala_{i}" for i in range(100)]
        
        result = self.cbr.diagnose(symptoms)
        
        self.assertIsNotNone(result)
    
    def test_special_characters_in_symptoms(self):
        """Test: Handle special characters"""
        symptoms = ["demam-tinggi", "batuk/pilek", "nyeri_tenggorokan"]
        
        similarity = self.cbr.calculate_similarity(symptoms, symptoms)
        
        self.assertEqual(similarity, 1.0)


class TestPerformance(unittest.TestCase):
    """Test untuk performance"""
    
    def setUp(self):
        self.cbr = CaseBasedReasoningSystem()
    
    def test_retrieve_performance(self):
        """Test: Retrieve performance dengan banyak cases"""
        import time
        
        symptoms = ["demam", "batuk"]
        
        start_time = time.time()
        for _ in range(100):
            self.cbr.retrieve(symptoms, top_k=3)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete 100 retrievals in less than 1 second
        self.assertLess(execution_time, 1.0)
    
    def test_case_base_size(self):
        """Test: Case base size"""
        # Case base should not be too large
        self.assertGreater(len(self.cbr.cases), 0)
        self.assertLess(len(self.cbr.cases), 10000)


def run_tests():
    """Jalankan semua tests"""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSimilarityCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestRetrieve))
    suite.addTests(loader.loadTestsFromTestCase(TestReuse))
    suite.addTests(loader.loadTestsFromTestCase(TestRevise))
    suite.addTests(loader.loadTestsFromTestCase(TestRetain))
    suite.addTests(loader.loadTestsFromTestCase(TestDiagnose))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
