"""
Unit Tests for PP 36/2021 Import Script
======================================
Tests core functions for parsing wage regulation articles.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from import_pp36_2021_pengupahan import (
    parse_pp36_articles,
    categorize_pp36_content,
    extract_wage_concepts,
    extract_chapter_context,
    count_ayat,
    load_sample_data
)

class TestPP36Import(unittest.TestCase):
    
    def setUp(self):
        """Setup test data"""
        self.sample_content = """## BAB I
## KETENTUAN UMUM

### Pasal 1
Dalam Peraturan Pemerintah ini yang dimaksud dengan:
1. Pengupahan adalah segala sesuatu yang berhubungan dengan upah.
2. Upah minimum adalah upah bulanan terendah yang terdiri atas upah pokok dan tunjangan tetap.

## BAB II
## KOMPONEN DAN STRUKTUR UPAH

### Pasal 3
(1) Komponen upah terdiri atas:
    a. upah pokok; dan
    b. tunjangan.
(2) Besarnya upah pokok paling sedikit 75% dari jumlah upah pokok dan tunjangan tetap.

## BAB VII
## TUNJANGAN HARI RAYA KEAGAMAAN

### Pasal 36
(1) Pengusaha wajib memberikan tunjangan hari raya keagamaan kepada pekerja/buruh yang telah mempunyai masa kerja 1 (satu) bulan secara terus menerus atau lebih.
(2) Tunjangan hari raya keagamaan sebagaimana dimaksud pada ayat (1) dibayarkan 1 (satu) kali dalam 1 (satu) tahun."""

    def test_parse_pp36_articles(self):
        """Test parsing PP 36/2021 articles"""
        articles = parse_pp36_articles(self.sample_content)
        
        # Should find 3 articles
        self.assertEqual(len(articles), 3)
        
        # Check first article
        first_article = articles[0]
        self.assertEqual(first_article['pasal_number'], '1')
        self.assertEqual(first_article['regulation'], 'PP 36/2021')
        self.assertEqual(first_article['hierarchy_level'], 2)
        self.assertEqual(first_article['category'], 'wage_regulation')
        
        # Check content exists
        self.assertGreater(len(first_article['content']), 0)
        self.assertGreater(first_article['word_count'], 0)

    def test_categorize_pp36_content(self):
        """Test PP 36/2021 content categorization"""
        # Test komponen upah category
        komponen_content = "komponen upah terdiri atas upah pokok dan tunjangan"
        category1 = categorize_pp36_content(komponen_content, "KOMPONEN DAN STRUKTUR UPAH")
        self.assertEqual(category1, 'komponen_upah')
        
        # Test upah minimum category
        upmin_content = "upah minimum adalah upah bulanan terendah"
        category2 = categorize_pp36_content(upmin_content, "UPAH MINIMUM")
        self.assertEqual(category2, 'upah_minimum')
        
        # Test THR category
        thr_content = "tunjangan hari raya keagamaan kepada pekerja"
        category3 = categorize_pp36_content(thr_content, "TUNJANGAN HARI RAYA")
        self.assertEqual(category3, 'thr')
        
        # Test upah lembur category
        lembur_content = "upah kerja lembur dan perhitungan lembur"
        category4 = categorize_pp36_content(lembur_content, "UPAH KERJA LEMBUR")
        self.assertEqual(category4, 'upah_lembur')

    def test_extract_wage_concepts(self):
        """Test wage concept extraction"""
        # Test basic wage concepts
        content1 = "upah pokok dan tunjangan tetap untuk karyawan"
        concepts1 = extract_wage_concepts(content1)
        self.assertIn('upah_pokok', concepts1)
        self.assertIn('tunjangan_tetap', concepts1)
        
        # Test minimum wage concepts
        content2 = "upah minimum provinsi dan kebutuhan hidup layak"
        concepts2 = extract_wage_concepts(content2)
        self.assertIn('upah_minimum', concepts2)
        self.assertIn('kebutuhan_hidup_layak', concepts2)
        
        # Test overtime concepts
        content3 = "upah lembur dan perhitungan kerja lembur"
        concepts3 = extract_wage_concepts(content3)
        self.assertIn('upah_lembur', concepts3)
        
        # Test THR concepts
        content4 = "THR dan tunjangan hari raya untuk pekerja"
        concepts4 = extract_wage_concepts(content4)
        self.assertIn('thr', concepts4)

    def test_count_ayat(self):
        """Test ayat counting functionality"""
        # Test content with ayat
        content_with_ayat = """(1) Ayat pertama tentang upah.
        (2) Ayat kedua tentang tunjangan.
        (3) Ayat ketiga tentang komponen."""
        
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
        
        BAB II KOMPONEN UPAH
        
        ### Pasal 3
        More content"""
        
        # Test chapter extraction
        context1 = extract_chapter_context(content, '1')
        self.assertIn('BAB I', context1)
        
        context2 = extract_chapter_context(content, '3')
        self.assertIn('BAB II', context2)

    def test_metadata_structure(self):
        """Test metadata structure completeness"""
        articles = parse_pp36_articles(self.sample_content)
        
        required_fields = [
            'pasal_number', 'content', 'title', 'ayat_count', 'word_count',
            'regulation', 'regulation_full', 'category', 'subcategory',
            'hierarchy_level', 'chapter_context', 'source_reference',
            'implements_regulation', 'related_uu', 'wage_concepts',
            'created_date'
        ]
        
        for article in articles:
            for field in required_fields:
                self.assertIn(field, article, f"Missing field: {field}")

    def test_hierarchy_and_regulation_info(self):
        """Test regulation hierarchy and info"""
        articles = parse_pp36_articles(self.sample_content)
        
        for article in articles:
            # Check hierarchy level for PP
            self.assertEqual(article['hierarchy_level'], 2)
            
            # Check regulation info
            self.assertEqual(article['regulation'], 'PP 36/2021')
            self.assertEqual(article['category'], 'wage_regulation')
            self.assertEqual(article['implements_regulation'], 'UU 11/2020 (Cipta Kerja)')
            self.assertEqual(article['related_uu'], 'UU 13/2003 (Ketenagakerjaan)')

    def test_word_count_and_ayat_accuracy(self):
        """Test word count and ayat calculation accuracy"""
        articles = parse_pp36_articles(self.sample_content)
        
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
        articles = parse_pp36_articles(self.sample_content)
        
        # Check pasal numbers
        pasal_numbers = [article['pasal_number'] for article in articles]
        expected_pasal = ['1', '3', '36']
        self.assertEqual(pasal_numbers, expected_pasal)

    def test_wage_concepts_coverage(self):
        """Test wage concept coverage"""
        articles = parse_pp36_articles(self.sample_content)
        
        # Should extract relevant wage concepts from each article
        all_concepts = []
        for article in articles:
            all_concepts.extend(article['wage_concepts'])
        
        # Should find common wage concepts
        self.assertTrue(len(all_concepts) > 0)
        
        # Check specific concepts based on content
        concept_names = set(all_concepts)
        expected_concepts = {'upah_pokok', 'tunjangan_tetap', 'thr'}
        self.assertTrue(len(concept_names.intersection(expected_concepts)) > 0)

    def test_wage_specific_categorization(self):
        """Test wage-specific categorization logic"""
        articles = parse_pp36_articles(self.sample_content)
        
        # Check that articles are properly categorized
        categories = [article['subcategory'] for article in articles]
        
        # Should have proper wage-related categories
        valid_categories = {
            'ketentuan_umum', 'komponen_upah', 'upah_minimum',
            'thr', 'upah_lembur', 'perlindungan_upah'
        }
        
        for category in categories:
            self.assertIn(category, valid_categories, f"Invalid category: {category}")

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