"""
Unit Tests for UU 13/2003 Import Script
======================================
Tests core functions for parsing foundation employment law articles.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from import_uu13_2003_ketenagakerjaan import (
    parse_uu13_articles,
    categorize_uu13_content,
    extract_uu13_concepts,
    extract_chapter_context,
    count_ayat,
    get_implementing_regulations,
    load_sample_data
)

class TestUU13Import(unittest.TestCase):
    
    def setUp(self):
        """Setup test data"""
        self.sample_content = """## BAB I
## KETENTUAN UMUM

### Pasal 1
Dalam undang-undang ini yang dimaksud dengan:
1. Ketenagakerjaan adalah segala hal yang berhubungan dengan tenaga kerja pada waktu sebelum, selama, dan sesudah masa hubungan kerja.
2. Tenaga kerja adalah setiap orang yang mampu melakukan pekerjaan guna menghasilkan barang dan/atau jasa.

## BAB V
## HUBUNGAN KERJA

### Pasal 56
(1) Perjanjian kerja dibuat untuk waktu tertentu atau untuk waktu tidak tertentu.
(2) Perjanjian kerja untuk waktu tertentu didasarkan atas:
    a. jangka waktu; atau
    b. selesainya suatu pekerjaan tertentu.

## BAB XI
## PENGUPAHAN

### Pasal 88
(1) Setiap pekerja/buruh berhak memperoleh penghasilan yang memenuhi penghidupan yang layak bagi kemanusiaan.
(2) Untuk mewujudkan penghasilan yang memenuhi penghidupan yang layak bagi kemanusiaan sebagaimana dimaksud pada ayat (1), pemerintah menetapkan kebijakan pengupahan yang melindungi pekerja/buruh."""

    def test_parse_uu13_articles(self):
        """Test parsing UU 13/2003 articles"""
        articles = parse_uu13_articles(self.sample_content)
        
        # Should find 3 articles
        self.assertEqual(len(articles), 3)
        
        # Check first article
        first_article = articles[0]
        self.assertEqual(first_article['pasal_number'], '1')
        self.assertEqual(first_article['regulation'], 'UU 13/2003')
        self.assertEqual(first_article['hierarchy_level'], 1)
        self.assertEqual(first_article['category'], 'employment_law')
        
        # Check content exists
        self.assertGreater(len(first_article['content']), 0)
        self.assertGreater(first_article['word_count'], 0)

    def test_categorize_uu13_content(self):
        """Test UU 13/2003 content categorization"""
        # Test hubungan kerja category
        hubungan_kerja_content = "perjanjian kerja antara pengusaha dan pekerja PKWT"
        category1 = categorize_uu13_content(hubungan_kerja_content, "HUBUNGAN KERJA")
        self.assertEqual(category1, 'hubungan_kerja')
        
        # Test pengupahan category
        upah_content = "upah minimum dan pengupahan pekerja"
        category2 = categorize_uu13_content(upah_content, "PENGUPAHAN")
        self.assertEqual(category2, 'pengupahan')
        
        # Test waktu kerja category
        waktu_kerja_content = "jam kerja dan waktu kerja karyawan"
        category3 = categorize_uu13_content(waktu_kerja_content, "WAKTU KERJA")
        self.assertEqual(category3, 'waktu_kerja')
        
        # Test serikat pekerja category
        serikat_content = "serikat pekerja dan organisasi buruh"
        category4 = categorize_uu13_content(serikat_content, "SERIKAT PEKERJA")
        self.assertEqual(category4, 'serikat_pekerja')

    def test_extract_uu13_concepts(self):
        """Test UU 13/2003 concept extraction"""
        # Test basic employment concepts
        content1 = "tenaga kerja dan pekerja buruh dengan pengusaha"
        concepts1 = extract_uu13_concepts(content1)
        self.assertIn('tenaga_kerja', concepts1)
        self.assertIn('pekerja_buruh', concepts1)
        self.assertIn('pengusaha', concepts1)
        
        # Test PKWT concepts
        content2 = "PKWT dan perjanjian kerja waktu tertentu"
        concepts2 = extract_uu13_concepts(content2)
        self.assertIn('pkwt', concepts2)
        
        # Test wage concepts
        content3 = "upah minimum dan pengupahan karyawan"
        concepts3 = extract_uu13_concepts(content3)
        self.assertIn('upah', concepts3)
        
        # Test termination concepts
        content4 = "PHK dan pemutusan hubungan kerja dengan pesangon"
        concepts4 = extract_uu13_concepts(content4)
        self.assertIn('pemutusan_hubungan_kerja', concepts4)
        self.assertIn('pesangon', concepts4)

    def test_count_ayat(self):
        """Test ayat counting functionality"""
        # Test content with ayat
        content_with_ayat = """(1) Pasal pertama dengan ayat satu.
        (2) Pasal kedua dengan ayat dua.
        (3) Pasal ketiga dengan ayat tiga."""
        
        ayat_count = count_ayat(content_with_ayat)
        self.assertEqual(ayat_count, 3)
        
        # Test content without ayat
        content_no_ayat = "Pasal tanpa ayat bernomor."
        ayat_count_zero = count_ayat(content_no_ayat)
        self.assertEqual(ayat_count_zero, 0)

    def test_extract_chapter_context(self):
        """Test chapter context extraction"""
        content = """BAB I KETENTUAN UMUM
        
        ### Pasal 1
        Some content here
        
        BAB V HUBUNGAN KERJA
        
        ### Pasal 56
        More content"""
        
        # Test chapter extraction
        context1 = extract_chapter_context(content, '1')
        self.assertIn('BAB I', context1)
        
        context2 = extract_chapter_context(content, '56')
        self.assertIn('BAB V', context2)

    def test_get_implementing_regulations(self):
        """Test implementing regulations mapping"""
        # Test hubungan_kerja implementing regulations
        impl1 = get_implementing_regulations('hubungan_kerja')
        self.assertIn('PP 35/2021 (PKWT & PHK)', impl1)
        
        # Test pengupahan implementing regulations
        impl2 = get_implementing_regulations('pengupahan')
        self.assertIn('PP 36/2021 (Pengupahan)', impl2)
        
        # Test unknown category
        impl3 = get_implementing_regulations('unknown_category')
        self.assertEqual(impl3, [])

    def test_metadata_structure(self):
        """Test metadata structure completeness"""
        articles = parse_uu13_articles(self.sample_content)
        
        required_fields = [
            'pasal_number', 'content', 'title', 'ayat_count', 'word_count',
            'regulation', 'regulation_full', 'category', 'subcategory',
            'hierarchy_level', 'chapter_context', 'source_reference',
            'amended_by', 'implementing_regulations', 'employment_concepts',
            'created_date'
        ]
        
        for article in articles:
            for field in required_fields:
                self.assertIn(field, article, f"Missing field: {field}")

    def test_hierarchy_and_regulation_info(self):
        """Test regulation hierarchy and info"""
        articles = parse_uu13_articles(self.sample_content)
        
        for article in articles:
            # Check hierarchy level for UU (highest)
            self.assertEqual(article['hierarchy_level'], 1)
            
            # Check regulation info
            self.assertEqual(article['regulation'], 'UU 13/2003')
            self.assertEqual(article['category'], 'employment_law')
            self.assertIn('UU 11/2020', article['amended_by'])
            self.assertIn('UU 6/2023', article['amended_by'])

    def test_word_count_and_ayat_accuracy(self):
        """Test word count and ayat calculation accuracy"""
        articles = parse_uu13_articles(self.sample_content)
        
        for article in articles:
            # Word count should be positive
            self.assertGreater(article['word_count'], 0)
            
            # Word count should match actual content
            actual_count = len(article['content'].split())
            self.assertEqual(article['word_count'], actual_count)
            
            # Ayat count should be non-negative
            self.assertGreaterEqual(article['ayat_count'], 0)

    def test_pasal_number_extraction(self):
        """Test pasal number extraction"""
        articles = parse_uu13_articles(self.sample_content)
        
        # Check pasal numbers
        pasal_numbers = [article['pasal_number'] for article in articles]
        expected_pasal = ['1', '56', '88']
        self.assertEqual(pasal_numbers, expected_pasal)

    def test_employment_concepts_coverage(self):
        """Test employment concept coverage"""
        articles = parse_uu13_articles(self.sample_content)
        
        # Should extract relevant concepts from each article
        all_concepts = []
        for article in articles:
            all_concepts.extend(article['employment_concepts'])
        
        # Should find common employment concepts
        self.assertTrue(len(all_concepts) > 0)
        
        # Check specific concepts based on content
        concept_names = set(all_concepts)
        expected_concepts = {'tenaga_kerja', 'pekerja_buruh', 'upah'}
        self.assertTrue(len(concept_names.intersection(expected_concepts)) > 0)

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