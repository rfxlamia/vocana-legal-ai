"""
Unit Tests for UU 2/2004 Import Script
=====================================
Tests core functions for parsing industrial dispute resolution articles.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from import_uu2_2004_perselisihan import (
    parse_uu2_articles,
    categorize_uu2_content,
    extract_dispute_concepts,
    extract_chapter_context,
    count_ayat,
    get_related_dispute_regulations,
    load_sample_data
)

class TestUU2Import(unittest.TestCase):
    
    def setUp(self):
        """Setup test data"""
        self.sample_content = """## BAB I
## KETENTUAN UMUM

### Pasal 1
Dalam Undang-undang ini yang dimaksud dengan:
1. Hubungan Industrial adalah suatu sistem hubungan yang terbentuk antara para pelaku dalam proses produksi.
2. Perselisihan Hubungan Industrial adalah perbedaan pendapat yang mengakibatkan pertentangan.

## BAB III
## PENYELESAIAN PERSELISIHAN MELALUI MEDIASI

### Pasal 7
(1) Mediasi Hubungan Industrial yang selanjutnya disebut mediasi adalah penyelesaian perselisihan hak, perselisihan kepentingan, perselisihan pemutusan hubungan kerja melalui musyawarah yang ditengahi oleh seorang atau lebih mediator yang netral.
(2) Mediator sebagaimana dimaksud pada ayat (1) adalah pegawai instansi yang bertanggung jawab di bidang ketenagakerjaan."""

    def test_parse_uu2_articles(self):
        """Test parsing UU 2/2004 articles"""
        articles = parse_uu2_articles(self.sample_content)
        
        # Should find 2 articles
        self.assertEqual(len(articles), 2)
        
        # Check first article
        first_article = articles[0]
        self.assertEqual(first_article['pasal_number'], '1')
        self.assertEqual(first_article['regulation'], 'UU 2/2004')
        self.assertEqual(first_article['hierarchy_level'], 1)
        self.assertEqual(first_article['category'], 'industrial_dispute_law')
        
        # Check content exists
        self.assertGreater(len(first_article['content']), 0)
        self.assertGreater(first_article['word_count'], 0)

    def test_categorize_uu2_content(self):
        """Test UU 2/2004 content categorization"""
        # Test mediasi category
        mediasi_content = "mediasi adalah penyelesaian perselisihan melalui musyawarah"
        category1 = categorize_uu2_content(mediasi_content, "PENYELESAIAN PERSELISIHAN MELALUI MEDIASI")
        self.assertEqual(category1, 'mediasi')
        
        # Test arbitrase category
        arbitrase_content = "arbitrase adalah penyelesaian perselisihan kepentingan"
        category2 = categorize_uu2_content(arbitrase_content, "ARBITRASE")
        self.assertEqual(category2, 'arbitrase')
        
        # Test sengketa PHK category
        phk_content = "perselisihan pemutusan hubungan kerja antara pekerja dan pengusaha"
        category3 = categorize_uu2_content(phk_content, "SENGKETA PHK")
        self.assertEqual(category3, 'sengketa_phk')

    def test_extract_dispute_concepts(self):
        """Test dispute concept extraction"""
        # Test basic dispute concepts
        content1 = "perselisihan hubungan industrial antara pekerja dan pengusaha"
        concepts1 = extract_dispute_concepts(content1)
        self.assertIn('perselisihan_hubungan_industrial', concepts1)
        
        # Test mediation concepts
        content2 = "mediasi dengan bantuan mediator yang netral"
        concepts2 = extract_dispute_concepts(content2)
        self.assertIn('mediasi', concepts2)
        
        # Test court concepts
        content3 = "putusan pengadilan hubungan industrial dengan majelis hakim"
        concepts3 = extract_dispute_concepts(content3)
        self.assertIn('pengadilan_hubungan_industrial', concepts3)
        self.assertIn('putusan', concepts3)
        self.assertIn('majelis_hakim', concepts3)

    def test_get_related_dispute_regulations(self):
        """Test related dispute regulations mapping"""
        # Test mediasi related regulations
        related1 = get_related_dispute_regulations('mediasi')
        self.assertIn('Permenaker 2/2015 (Mediasi HI)', related1)
        
        # Test arbitrase related regulations
        related2 = get_related_dispute_regulations('arbitrase')
        self.assertIn('Permenaker 31/2008 (Arbitrase)', related2)
        
        # Test unknown category
        related3 = get_related_dispute_regulations('unknown_category')
        self.assertEqual(related3, [])

    def test_count_ayat(self):
        """Test ayat counting functionality"""
        content_with_ayat = """(1) Ayat pertama tentang mediasi.
        (2) Ayat kedua tentang arbitrase.
        (3) Ayat ketiga tentang pengadilan."""
        
        ayat_count = count_ayat(content_with_ayat)
        self.assertEqual(ayat_count, 3)

    def test_extract_chapter_context(self):
        """Test chapter context extraction"""
        content = """BAB I KETENTUAN UMUM
        
        ### Pasal 1
        Some content here
        
        BAB III MEDIASI
        
        ### Pasal 7
        More content"""
        
        # Test chapter extraction
        context1 = extract_chapter_context(content, '1')
        self.assertIn('BAB I', context1)
        
        context2 = extract_chapter_context(content, '7')
        self.assertIn('BAB III', context2)

    def test_metadata_structure(self):
        """Test metadata structure completeness"""
        articles = parse_uu2_articles(self.sample_content)
        
        required_fields = [
            'pasal_number', 'content', 'title', 'ayat_count', 'word_count',
            'regulation', 'regulation_full', 'category', 'subcategory',
            'hierarchy_level', 'chapter_context', 'source_reference',
            'related_regulations', 'dispute_concepts', 'created_date'
        ]
        
        for article in articles:
            for field in required_fields:
                self.assertIn(field, article, f"Missing field: {field}")

    def test_hierarchy_and_regulation_info(self):
        """Test regulation hierarchy and info"""
        articles = parse_uu2_articles(self.sample_content)
        
        for article in articles:
            # Check hierarchy level for UU (highest)
            self.assertEqual(article['hierarchy_level'], 1)
            
            # Check regulation info
            self.assertEqual(article['regulation'], 'UU 2/2004')
            self.assertEqual(article['category'], 'industrial_dispute_law')

    def test_pasal_number_extraction(self):
        """Test pasal number extraction"""
        articles = parse_uu2_articles(self.sample_content)
        
        # Check pasal numbers
        pasal_numbers = [article['pasal_number'] for article in articles]
        expected_pasal = ['1', '7']
        self.assertEqual(pasal_numbers, expected_pasal)

class TestFileOperations(unittest.TestCase):
    
    def test_load_sample_data_file_structure(self):
        """Test that load_sample_data handles file paths correctly"""
        sample_data = load_sample_data()
        
        # If file exists, should return content
        if sample_data:
            self.assertIsInstance(sample_data, str)
            self.assertGreater(len(sample_data), 0)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)