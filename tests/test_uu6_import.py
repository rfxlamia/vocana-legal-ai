"""
Unit Tests for UU 6/2023 Import Script
=====================================
Tests core functions for parsing legal amendments and metadata extraction.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from import_uu6_2023_cipta_kerja import (
    parse_uu6_changes, 
    detect_amendment_type, 
    extract_legal_concepts,
    load_sample_data
)

class TestUU6Import(unittest.TestCase):
    
    def setUp(self):
        """Setup test data"""
        self.sample_content = """####(1) Ketentuan Pasal 13 diubah sehingga berbunyi sebagai berikut:**
Pasal 13
(1) Pelatihan Kerja diselenggarakan berdasarkan program pelatihan yang mengacu pada standar kompetensi kerja.
(2) Program pelatihan sebagaimana dimaksud pada ayat (1) disusun berdasarkan:
    a. jenis pelatihan;
    b. jenjang pelatihan; dan
    c. sifat pelatihan.

####(2) Pasal 15 dihapus.**

####(3) Di antara Pasal 16 dan Pasal 17, disisipkan 1 (satu) pasal, yakni Pasal 16A yang berbunyi sebagai berikut:**
Pasal 16A
(1) Pelatihan kerja diselenggarakan dengan memperhatian kebutuhan pasar kerja dan dunia usaha."""

    def test_parse_uu6_changes(self):
        """Test parsing UU 6/2023 changes"""
        articles = parse_uu6_changes(self.sample_content)
        
        # Should find 3 changes
        self.assertEqual(len(articles), 3)
        
        # Check first change
        first_change = articles[0]
        self.assertEqual(first_change['change_number'], '1')
        self.assertEqual(first_change['pasal_number'], '13')
        self.assertEqual(first_change['amendment_type'], 'diubah')
        self.assertEqual(first_change['regulation'], 'UU 6/2023')
        
        # Check second change (deletion)
        second_change = articles[1]
        self.assertEqual(second_change['change_number'], '2')
        self.assertEqual(second_change['pasal_number'], '15')
        self.assertEqual(second_change['amendment_type'], 'dihapus')
        
        # Check third change (insertion)
        third_change = articles[2]
        self.assertEqual(third_change['change_number'], '3')
        self.assertEqual(third_change['pasal_number'], '16A')
        self.assertEqual(third_change['amendment_type'], 'disisipkan')

    def test_detect_amendment_type(self):
        """Test amendment type detection"""
        # Test diubah
        self.assertEqual(detect_amendment_type("Pasal 13 diubah"), 'diubah')
        self.assertEqual(detect_amendment_type("ketentuan diganti"), 'diubah')
        
        # Test dihapus
        self.assertEqual(detect_amendment_type("Pasal 15 dihapus"), 'dihapus')
        self.assertEqual(detect_amendment_type("ayat dicabut"), 'dihapus')
        
        # Test disisipkan
        self.assertEqual(detect_amendment_type("disisipkan 1 pasal"), 'disisipkan')
        self.assertEqual(detect_amendment_type("ditambah ketentuan"), 'disisipkan')
        
        # Test default
        self.assertEqual(detect_amendment_type("some other text"), 'modified')

    def test_extract_legal_concepts(self):
        """Test legal concept extraction"""
        # Test employment concepts
        content1 = "perjanjian kerja dan upah minimum pekerja"
        concepts1 = extract_legal_concepts(content1)
        self.assertIn('kontrak_kerja', concepts1)
        self.assertIn('pengupahan', concepts1)
        
        # Test PHK concepts
        content2 = "pemutusan hubungan kerja dan pemberhentian"
        concepts2 = extract_legal_concepts(content2)
        self.assertIn('phk', concepts2)
        
        # Test working hours
        content3 = "jam kerja dan lembur shift"
        concepts3 = extract_legal_concepts(content3)
        self.assertIn('jam_kerja', concepts3)
        
        # Test foreign workers
        content4 = "tenaga kerja asing TKA"
        concepts4 = extract_legal_concepts(content4)
        self.assertIn('pekerja_asing', concepts4)
        
        # Test no concepts
        content5 = "some random text without legal terms"
        concepts5 = extract_legal_concepts(content5)
        self.assertEqual(len(concepts5), 0)

    def test_pasal_number_extraction(self):
        """Test pasal number extraction from content"""
        articles = parse_uu6_changes(self.sample_content)
        
        # Check pasal numbers
        pasal_numbers = [article['pasal_number'] for article in articles]
        expected_pasal = ['13', '15', '16A']
        self.assertEqual(pasal_numbers, expected_pasal)

    def test_cross_reference_generation(self):
        """Test cross-reference generation"""
        articles = parse_uu6_changes(self.sample_content)
        
        # Check cross-references
        for article in articles:
            if article['pasal_number'] not in ['Change_1', 'Change_2', 'Change_3']:
                expected_ref = f"Mengubah UU 13/2003 Pasal {article['pasal_number']}"
                self.assertEqual(article['cross_reference'], expected_ref)

    def test_metadata_structure(self):
        """Test metadata structure completeness"""
        articles = parse_uu6_changes(self.sample_content)
        
        required_fields = [
            'pasal_number', 'change_number', 'content', 'title',
            'amendment_type', 'word_count', 'regulation', 'regulation_full',
            'category', 'subcategory', 'hierarchy_level', 'source_reference',
            'cross_reference', 'legal_concept', 'created_date'
        ]
        
        for article in articles:
            for field in required_fields:
                self.assertIn(field, article, f"Missing field: {field}")

    def test_word_count_calculation(self):
        """Test word count calculation"""
        articles = parse_uu6_changes(self.sample_content)
        
        for article in articles:
            # Word count should be positive
            self.assertGreater(article['word_count'], 0)
            
            # Word count should match actual content
            actual_count = len(article['content'].split())
            self.assertEqual(article['word_count'], actual_count)

class TestFileOperations(unittest.TestCase):
    
    def test_load_sample_data_file_structure(self):
        """Test that load_sample_data handles file paths correctly"""
        # This tests the function behavior when file doesn't exist
        # In actual environment, it should load from ../sample_data/uu6_sample.txt
        
        # Test would pass if file structure is correct
        sample_data = load_sample_data()
        
        # If file exists, should return content
        if sample_data:
            self.assertIsInstance(sample_data, str)
            self.assertGreater(len(sample_data), 0)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)