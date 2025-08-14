"""
Unit Tests for PP 35/2021 Import Script
======================================
Tests core functions for parsing employment regulation articles.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from import_pp35_2021_pkwt_phk import (
    parse_pp35_articles,
    categorize_pp35_content,
    extract_employment_concepts,
    extract_chapter_context,
    load_sample_data
)

class TestPP35Import(unittest.TestCase):
    
    def setUp(self):
        """Setup test data"""
        self.sample_content = """## BAB I
## KETENTUAN UMUM

#### Pasal 1
Dalam Peraturan Pemerintah ini yang dimaksud dengan:
1. PKWT adalah Perjanjian Kerja antara pekerja/buruh dengan pengusaha untuk mengadakan hubungan kerja dalam waktu tertentu.

#### Pasal 2
(1) PKWT hanya dapat dibuat untuk pekerjaan tertentu yang menurut jenis dan sifat atau kegiatan pekerjaannya akan selesai dalam waktu tertentu.
(2) Pekerjaan tertentu sebagaimana dimaksud pada ayat (1) adalah:
    a. pekerjaan yang sekali selesai atau yang sementara sifatnya;
    b. pekerjaan yang bersifat musiman;

## BAB VII
## PEMUTUSAN HUBUNGAN KERJA

#### Pasal 40
(1) Pengusaha, pekerja/buruh, serikat pekerja/serikat buruh, dan pemerintah, dengan segala upaya harus mengusahakan agar jangan terjadi pemutusan hubungan kerja.
(2) Dalam hal segala upaya telah dilakukan, tetapi PHK tidak dapat dihindari, maka maksud PHK wajib dirundingkan."""

    def test_parse_pp35_articles(self):
        """Test parsing PP 35/2021 articles"""
        articles = parse_pp35_articles(self.sample_content)
        
        # Should find 3 articles
        self.assertEqual(len(articles), 3)
        
        # Check first article
        first_article = articles[0]
        self.assertEqual(first_article['pasal_number'], '1')
        self.assertEqual(first_article['regulation'], 'PP 35/2021')
        self.assertEqual(first_article['hierarchy_level'], 2)
        
        # Check content exists
        self.assertGreater(len(first_article['content']), 0)
        self.assertGreater(first_article['word_count'], 0)

    def test_categorize_pp35_content(self):
        """Test PP 35/2021 content categorization"""
        # Test PKWT category
        pkwt_content = "PKWT hanya dapat dibuat untuk pekerjaan tertentu"
        self.assertEqual(categorize_pp35_content(pkwt_content), 'pkwt')
        
        # Test PHK category
        phk_content = "pemutusan hubungan kerja tidak dapat dihindari"
        self.assertEqual(categorize_pp35_content(phk_content), 'phk')
        
        # Test alih daya category
        alih_daya_content = "pekerjaan alih daya dan outsourcing"
        self.assertEqual(categorize_pp35_content(alih_daya_content), 'alih_daya')
        
        # Test waktu kerja category
        waktu_kerja_content = "waktu kerja dan jam kerja karyawan"
        self.assertEqual(categorize_pp35_content(waktu_kerja_content), 'waktu_kerja')
        
        # Test general category
        general_content = "ketentuan umum dalam peraturan"
        self.assertEqual(categorize_pp35_content(general_content), 'umum')

    def test_extract_employment_concepts(self):
        """Test employment concept extraction"""
        # Test PKWT concepts
        pkwt_content = "PKWT dan perjanjian kerja waktu tertentu"
        concepts1 = extract_employment_concepts(pkwt_content)
        self.assertIn('pkwt', concepts1)
        
        # Test PHK concepts
        phk_content = "PHK dan pemutusan hubungan kerja dengan pesangon"
        concepts2 = extract_employment_concepts(phk_content)
        self.assertIn('phk', concepts2)
        self.assertIn('pesangon', concepts2)
        
        # Test working hours concepts
        waktu_content = "waktu kerja dan kerja lembur karyawan"
        concepts3 = extract_employment_concepts(waktu_content)
        self.assertIn('waktu_kerja', concepts3)
        self.assertIn('lembur', concepts3)
        
        # Test outsourcing concepts
        outsourcing_content = "alih daya dan pemborongan pekerjaan"
        concepts4 = extract_employment_concepts(outsourcing_content)
        self.assertIn('alih_daya', concepts4)

    def test_extract_chapter_context(self):
        """Test chapter context extraction"""
        content = """BAB I KETENTUAN UMUM
        
        #### Pasal 1
        Some content here
        
        BAB II PERJANJIAN KERJA
        
        #### Pasal 5
        More content"""
        
        # Test chapter extraction
        context1 = extract_chapter_context(content, '1')
        self.assertIn('BAB I', context1)
        
        context2 = extract_chapter_context(content, '5') 
        self.assertIn('BAB II', context2)

    def test_metadata_structure(self):
        """Test metadata structure completeness"""
        articles = parse_pp35_articles(self.sample_content)
        
        required_fields = [
            'pasal_number', 'content', 'title', 'word_count',
            'regulation', 'regulation_full', 'category', 'subcategory',
            'hierarchy_level', 'chapter_context', 'source_reference',
            'implements_regulation', 'related_uu', 'employment_concepts',
            'created_date'
        ]
        
        for article in articles:
            for field in required_fields:
                self.assertIn(field, article, f"Missing field: {field}")

    def test_word_count_accuracy(self):
        """Test word count calculation accuracy"""
        articles = parse_pp35_articles(self.sample_content)
        
        for article in articles:
            # Word count should be positive
            self.assertGreater(article['word_count'], 0)
            
            # Word count should match actual content
            actual_count = len(article['content'].split())
            self.assertEqual(article['word_count'], actual_count)

    def test_pasal_number_extraction(self):
        """Test pasal number extraction"""
        articles = parse_pp35_articles(self.sample_content)
        
        # Check pasal numbers
        pasal_numbers = [article['pasal_number'] for article in articles]
        expected_pasal = ['1', '2', '40']
        self.assertEqual(pasal_numbers, expected_pasal)

    def test_hierarchy_and_regulation_info(self):
        """Test regulation hierarchy and info"""
        articles = parse_pp35_articles(self.sample_content)
        
        for article in articles:
            # Check hierarchy level for PP
            self.assertEqual(article['hierarchy_level'], 2)
            
            # Check regulation info
            self.assertEqual(article['regulation'], 'PP 35/2021')
            self.assertEqual(article['category'], 'employment_regulation')
            self.assertEqual(article['implements_regulation'], 'UU 11/2020 (Cipta Kerja)')
            self.assertEqual(article['related_uu'], 'UU 13/2003 (Ketenagakerjaan)')

class TestFileOperations(unittest.TestCase):
    
    def test_load_sample_data_file_structure(self):
        """Test that load_sample_data handles file paths correctly"""
        # Test would pass if file structure is correct
        sample_data = load_sample_data()
        
        # If file exists, should return content
        if sample_data:
            self.assertIsInstance(sample_data, str)
            self.assertGreater(len(sample_data), 0)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)