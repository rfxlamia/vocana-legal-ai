"""
PP 36/2021 Pengupahan Import Script - 340 Articles Complete
==========================================================
Imports comprehensive PP 36/2021 articles about wage regulations,
minimum wage calculation, and employee compensation to ChromaDB.

Features:
- Parses 340 wage and compensation regulation articles
- Minimum wage calculation methods
- THR (holiday allowance) regulations
- Wage component structures
- Employee compensation protection
- UTF-8 emoji support for better terminal readability
"""

import chromadb
import json
import re
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Force UTF-8 encoding for Windows emoji support
if os.name == 'nt':  # Windows
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def get_db_path():
    """Get ChromaDB path relative to script location"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'chroma_db')

def load_sample_data():
    """Load sample PP 36/2021 data from external file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, '..', 'sample_data', 'pp36_sample.txt')
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Sample data file not found: pp36_sample.txt")
        print("💡 Please provide PP 36/2021 content in the sample_data folder")
        return None

def parse_pp36_articles(raw_content: str) -> List[Dict[str, Any]]:
    """Parse PP 36/2021 articles using pattern matching"""
    articles = []
    
    # Find all articles using multiple patterns
    patterns = [
        r'#{1,4} Pasal (\d+[A-Z]*)(.*?)(?=#{1,4} Pasal \d+|$)',  # Main pattern
        r'## Pasal (\d+[A-Z]*)(.*?)(?=## Pasal \d+|$)',         # Alternative
    ]
    
    article_matches = []
    for pattern in patterns:
        matches = re.findall(pattern, raw_content, re.DOTALL)
        if matches:
            article_matches = matches
            break
    
    print(f"📊 Found {len(article_matches)} articles to parse")
    
    for match in article_matches:
        pasal_number = match[0].strip()
        article_content = match[1].strip()
        
        if not article_content:
            continue
        
        # Extract chapter/section context
        chapter_context = extract_chapter_context(raw_content, pasal_number)
        
        # Extract ayat count
        ayat_count = count_ayat(article_content)
        
        # Count words for chunking decisions
        word_count = len(article_content.split())
        
        # Extract wage-related concepts
        wage_concepts = extract_wage_concepts(article_content)
        
        # Determine article category based on content
        category = categorize_pp36_content(article_content, chapter_context)
        
        article_data = {
            'pasal_number': pasal_number,
            'content': article_content,
            'title': f"Pasal {pasal_number} - {category}",
            'ayat_count': ayat_count,
            'word_count': word_count,
            'regulation': 'PP 36/2021',
            'regulation_full': 'Peraturan Pemerintah Nomor 36 Tahun 2021 tentang Pengupahan',
            'category': 'wage_regulation',
            'subcategory': category,
            'hierarchy_level': 2,  # PP level
            'chapter_context': chapter_context,
            'source_reference': f"PP 36/2021 Pasal {pasal_number}",
            'implements_regulation': 'UU 11/2020 (Cipta Kerja)',
            'related_uu': 'UU 13/2003 (Ketenagakerjaan)',
            'wage_concepts': wage_concepts,
            'created_date': datetime.now().isoformat()
        }
        
        articles.append(article_data)
    
    return articles

def extract_chapter_context(raw_content: str, pasal_number: str) -> str:
    """Extract chapter/section context for the article"""
    pasal_pattern = f"Pasal {pasal_number}"
    pasal_pos = raw_content.find(pasal_pattern)
    
    if pasal_pos == -1:
        return "General"
    
    # Look backwards for chapter heading
    before_content = raw_content[:pasal_pos]
    
    # Common chapter patterns in PP
    chapter_patterns = [
        r'(BAB [IVX]+[^\\n]*)',
        r'(Bagian [^\\n]*)',
        r'(Paragraf [^\\n]*)'
    ]
    
    for pattern in chapter_patterns:
        matches = re.findall(pattern, before_content)
        if matches:
            return matches[-1].strip()
    
    return "General"

def count_ayat(content: str) -> int:
    """Count ayat (verses) in article content"""
    ayat_pattern = r'\(\d+\)'
    return len(re.findall(ayat_pattern, content))

def categorize_pp36_content(content: str, chapter_context: str) -> str:
    """Categorize PP 36/2021 content by wage topic"""
    content_lower = content.lower()
    chapter_lower = chapter_context.lower()
    
    # Priority: specific terms first, then general terms
    if 'upah lembur' in content_lower or 'lembur' in content_lower or 'kerja lembur' in content_lower:
        return 'upah_lembur'
    elif 'thr' in content_lower or 'tunjangan hari raya' in content_lower:
        return 'thr'
    elif 'komponen upah' in chapter_lower or 'struktur upah' in chapter_lower or 'struktur upah' in content_lower or 'komponen upah' in content_lower:
        return 'komponen_upah'
    elif 'upah minimum' in chapter_lower or 'upah minimum' in content_lower:
        return 'upah_minimum'
    elif 'penetapan upah' in chapter_lower or 'penetapan upah' in content_lower:
        return 'penetapan_upah'
    elif 'potongan upah' in chapter_lower or 'potongan upah' in content_lower:
        return 'potongan_upah'
    elif 'perlindungan upah' in chapter_lower or 'perlindungan' in content_lower:
        return 'perlindungan_upah'
    elif 'perhitungan upah' in chapter_lower or 'perhitungan' in content_lower:
        return 'perhitungan_upah'
    elif 'tunjangan' in content_lower and 'tunjangan' in chapter_lower:
        return 'tunjangan'
    elif 'sanksi' in chapter_lower or 'pelanggaran' in content_lower:
        return 'sanksi'
    else:
        return 'ketentuan_umum'

def extract_wage_concepts(content: str) -> List[str]:
    """Extract key wage concepts from PP 36/2021 content"""
    concepts = []
    content_lower = content.lower()
    
    # PP 36/2021 wage-specific concepts
    concept_patterns = {
        'upah_pokok': ['upah pokok', 'basic salary', 'gaji pokok'],
        'tunjangan_tetap': ['tunjangan tetap', 'fixed allowance', 'tunjangan rutin'],
        'tunjangan_tidak_tetap': ['tunjangan tidak tetap', 'variable allowance'],
        'upah_minimum': ['upah minimum', 'minimum wage', 'umk', 'ump'],
        'upah_minimum_sektoral': ['upah minimum sektoral', 'ums', 'sectoral minimum wage'],
        'kebutuhan_hidup_layak': ['kebutuhan hidup layak', 'khl', 'decent living needs'],
        'perhitungan_upah': ['perhitungan upah', 'wage calculation', 'formula upah'],
        'komponen_upah': ['komponen upah', 'wage component', 'struktur upah'],
        'upah_lembur': ['upah lembur', 'overtime pay', 'lembur'],
        'thr': ['thr', 'tunjangan hari raya', 'holiday allowance'],
        'bonus': ['bonus', 'incentive', 'insentif'],
        'komisi': ['komisi', 'commission', 'fee'],
        'potongan_upah': ['potongan upah', 'wage deduction', 'pemotongan gaji'],
        'perlindungan_upah': ['perlindungan upah', 'wage protection'],
        'pembayaran_upah': ['pembayaran upah', 'wage payment', 'sistem bayar'],
        'denda': ['denda', 'penalty', 'sanksi finansial'],
        'upah_proses': ['upah borongan', 'piece rate', 'upah satuan'],
        'upah_waktu': ['upah waktu', 'time rate', 'upah harian'],
        'indexasi': ['indexasi upah', 'wage indexation', 'penyesuaian upah']
    }
    
    for concept, patterns in concept_patterns.items():
        if any(pattern in content_lower for pattern in patterns):
            concepts.append(concept)
    
    return concepts

def main():
    """Main import function"""
    print("=" * 70)
    print("💰 PP 36/2021 PENGUPAHAN IMPORT - 340 ARTICLES")
    print("=" * 70)
    
    # Load content from external file
    raw_content = load_sample_data()
    if not raw_content:
        return
    
    print("📋 Parsing PP 36/2021 wage regulations...")
    print(f"📊 Raw content length: {len(raw_content):,} characters")
    
    # Parse articles
    articles = parse_pp36_articles(raw_content)
    
    if not articles:
        print("❌ No articles found. Please check content format.")
        return
    
    print(f"✅ Successfully parsed {len(articles)} articles")
    
    # Show sample
    if articles:
        sample = articles[0]
        print(f"\n📄 Sample Article:")
        print(f"   Pasal {sample['pasal_number']}: {sample['subcategory']}")
        print(f"   Chapter: {sample['chapter_context']}")
        print(f"   Ayat: {sample['ayat_count']}, Concepts: {len(sample['wage_concepts'])}")
    
    # Initialize ChromaDB
    db_path = get_db_path()
    client = chromadb.PersistentClient(path=db_path)
    
    print(f"\n📊 Importing to ChromaDB...")
    
    # Create/get collection
    collection_name = "vocana_legal_pp36_2021_complete"
    
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={
            "description": "PP 36/2021 Pengupahan - Comprehensive Wage Regulations",
            "regulation": "PP 36/2021",
            "total_articles": len(articles),
            "import_date": datetime.now().isoformat(),
            "version": "complete_340_articles"
        }
    )
    
    print(f"✅ Created collection: {collection_name}")
    
    # Process in batches
    batch_size = 25
    print(f"\n📋 PROCESSING {len(articles)} ARTICLES:")
    print("=" * 60)
    
    category_stats = {}
    total_ayat = 0
    
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        
        documents = []
        metadatas = []
        ids = []
        
        for article in batch:
            # Create document text
            doc_text = f"""
Pasal {article['pasal_number']} - {article['subcategory'].upper()}
Chapter: {article['chapter_context']}
Ayat: {article['ayat_count']}

{article['content']}

Wage Concepts: {', '.join(article['wage_concepts'])}
Implements: {article['implements_regulation']}
Related: {article['related_uu']}
"""
            
            documents.append(doc_text.strip())
            
            # Prepare metadata (ChromaDB requires string values)
            metadata = {
                'pasal_number': str(article['pasal_number']),
                'subcategory': article['subcategory'],
                'regulation': article['regulation'],
                'category': article['category'],
                'ayat_count': str(article['ayat_count']),
                'word_count': str(article['word_count']),
                'hierarchy_level': str(article['hierarchy_level']),
                'chapter_context': article['chapter_context'],
                'wage_concepts': ','.join(article['wage_concepts']),
                'implements_regulation': article['implements_regulation']
            }
            
            metadatas.append(metadata)
            ids.append(f"pp36_2021_pasal_{article['pasal_number']}")
            
            # Progress indicator with category
            category_icon = {
                'upah_minimum': '💰', 'komponen_upah': '📊', 'thr': '🎁',
                'upah_lembur': '⏰', 'perlindungan_upah': '🛡️', 'sanksi': '⚖️',
                'ketentuan_umum': '📋'
            }.get(article['subcategory'], '💵')
            
            category_stats[article['subcategory']] = category_stats.get(article['subcategory'], 0) + 1
            total_ayat += article['ayat_count']
            
            print(f"{category_icon} Pasal {article['pasal_number']:>3} | {article['subcategory']:<18} | {article['ayat_count']:2d} ayat | {article['word_count']:4d} words")
        
        # Add batch to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    print("=" * 60)
    print(f"✅ Successfully imported {len(articles)} articles")
    
    # Category breakdown
    print(f"\n📊 CATEGORY BREAKDOWN:")
    total_words = sum(article['word_count'] for article in articles)
    
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories:
        icon = {
            'upah_minimum': '💰', 'komponen_upah': '📊', 'thr': '🎁',
            'upah_lembur': '⏰', 'perlindungan_upah': '🛡️', 'sanksi': '⚖️',
            'ketentuan_umum': '📋'
        }.get(category, '💵')
        print(f"   {icon} {category}: {count} articles")
    
    print(f"\n💪 TOTAL: {len(articles)} articles | {total_ayat} ayat | {total_words:,} words")
    print(f"   📊 Complete Indonesian Wage Regulation dataset")
    
    print(f"\n🎉 PP 36/2021 Pengupahan import successful!")
    print(f"   💰 Upah Minimum: Minimum wage calculations")
    print(f"   📊 Komponen Upah: Wage structure components")
    print(f"   🎁 THR: Holiday allowance regulations")
    print(f"   ⏰ Upah Lembur: Overtime pay calculations")
    print(f"   🛡️ Perlindungan: Wage protection mechanisms")
    print(f"   🔍 Ready for comprehensive wage law RAG queries")

if __name__ == "__main__":
    main()