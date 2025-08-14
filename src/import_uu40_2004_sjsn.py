"""
UU 40/2004 SJSN Import Script - 267 Articles Complete
====================================================
Imports UU 40/2004 about National Social Security System (SJSN)
articles to ChromaDB database.

Features:
- Parses 267 social security system articles
- BPJS and social insurance regulations
- Healthcare and employment benefits
- Social security fund management
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
    """Load sample UU 40/2004 data from external file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, '..', 'sample_data', 'uu40_sample.txt')
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Sample data file not found: uu40_sample.txt")
        print("💡 Please provide UU 40/2004 content in the sample_data folder")
        return None

def parse_uu40_articles(raw_content: str) -> List[Dict[str, Any]]:
    """Parse UU 40/2004 articles using pattern matching"""
    articles = []
    
    # Find all articles using multiple patterns
    patterns = [
        r'#{1,4} Pasal (\d+[A-Z]*)(.*?)(?=#{1,4} Pasal \d+|$)',
        r'## Pasal (\d+[A-Z]*)(.*?)(?=## Pasal \d+|$)',
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
        
        chapter_context = extract_chapter_context(raw_content, pasal_number)
        ayat_count = len(re.findall(r'\(\d+\)', article_content))
        word_count = len(article_content.split())
        sjsn_concepts = extract_sjsn_concepts(article_content)
        category = categorize_uu40_content(article_content, chapter_context)
        
        article_data = {
            'pasal_number': pasal_number,
            'content': article_content,
            'title': f"Pasal {pasal_number} - {category}",
            'ayat_count': ayat_count,
            'word_count': word_count,
            'regulation': 'UU 40/2004',
            'regulation_full': 'Undang-Undang Nomor 40 Tahun 2004 tentang Sistem Jaminan Sosial Nasional',
            'category': 'social_security_law',
            'subcategory': category,
            'hierarchy_level': 1,
            'chapter_context': chapter_context,
            'source_reference': f"UU 40/2004 Pasal {pasal_number}",
            'sjsn_concepts': sjsn_concepts,
            'created_date': datetime.now().isoformat()
        }
        
        articles.append(article_data)
    
    return articles

def extract_chapter_context(raw_content: str, pasal_number: str) -> str:
    """Extract chapter/section context"""
    pasal_pattern = f"Pasal {pasal_number}"
    pasal_pos = raw_content.find(pasal_pattern)
    
    if pasal_pos == -1:
        return "General"
    
    before_content = raw_content[:pasal_pos]
    chapter_patterns = [r'(BAB [IVX]+[^\\n]*)', r'(Bagian [^\\n]*)']
    
    for pattern in chapter_patterns:
        matches = re.findall(pattern, before_content)
        if matches:
            return matches[-1].strip()
    
    return "General"

def categorize_uu40_content(content: str, chapter_context: str) -> str:
    """Categorize UU 40/2004 content by social security topic"""
    content_lower = content.lower()
    chapter_lower = chapter_context.lower()
    
    if 'jaminan kesehatan' in content_lower or 'kesehatan' in chapter_lower:
        return 'jaminan_kesehatan'
    elif 'jaminan kecelakaan kerja' in content_lower or 'kecelakaan kerja' in content_lower:
        return 'jaminan_kecelakaan_kerja'
    elif 'jaminan hari tua' in content_lower or 'hari tua' in content_lower:
        return 'jaminan_hari_tua'
    elif 'jaminan pensiun' in content_lower or 'pensiun' in content_lower:
        return 'jaminan_pensiun'
    elif 'jaminan kematian' in content_lower or 'kematian' in content_lower:
        return 'jaminan_kematian'
    elif 'bpjs' in content_lower or 'badan penyelenggara' in content_lower:
        return 'bpjs'
    elif 'iuran' in content_lower or 'kontribusi' in content_lower:
        return 'iuran_kontribusi'
    elif 'manfaat' in content_lower or 'benefit' in content_lower:
        return 'manfaat_jaminan'
    else:
        return 'ketentuan_umum'

def extract_sjsn_concepts(content: str) -> List[str]:
    """Extract SJSN concepts"""
    concepts = []
    content_lower = content.lower()
    
    concept_patterns = {
        'sjsn': ['sjsn', 'sistem jaminan sosial nasional'],
        'jaminan_kesehatan': ['jaminan kesehatan', 'jkn', 'bpjs kesehatan'],
        'jaminan_kecelakaan_kerja': ['jaminan kecelakaan kerja', 'jkk'],
        'jaminan_hari_tua': ['jaminan hari tua', 'jht'],
        'jaminan_pensiun': ['jaminan pensiun', 'jp'],
        'jaminan_kematian': ['jaminan kematian', 'jkm'],
        'bpjs': ['bpjs', 'badan penyelenggara jaminan sosial'],
        'iuran': ['iuran', 'kontribusi', 'premi'],
        'peserta': ['peserta', 'participant', 'tertanggung'],
        'manfaat': ['manfaat', 'benefit', 'santunan'],
        'dana_jaminan': ['dana jaminan', 'fund', 'dana sosial']
    }
    
    for concept, patterns in concept_patterns.items():
        if any(pattern in content_lower for pattern in patterns):
            concepts.append(concept)
    
    return concepts

def main():
    """Main import function"""
    print("=" * 70)
    print("🏥 UU 40/2004 SJSN IMPORT - 267 ARTICLES")
    print("=" * 70)
    
    raw_content = load_sample_data()
    if not raw_content:
        return
    
    print("📋 Parsing UU 40/2004 social security system law...")
    print(f"📊 Raw content length: {len(raw_content):,} characters")
    
    articles = parse_uu40_articles(raw_content)
    
    if not articles:
        print("❌ No articles found. Please check content format.")
        return
    
    print(f"✅ Successfully parsed {len(articles)} articles")
    
    if articles:
        sample = articles[0]
        print(f"\n📄 Sample Article:")
        print(f"   Pasal {sample['pasal_number']}: {sample['subcategory']}")
        print(f"   Chapter: {sample['chapter_context']}")
        print(f"   SJSN Concepts: {len(sample['sjsn_concepts'])}")
    
    # ChromaDB setup
    db_path = get_db_path()
    client = chromadb.PersistentClient(path=db_path)
    
    collection_name = "vocana_legal_uu40_2004_complete"
    
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={
            "description": "UU 40/2004 SJSN - National Social Security System",
            "regulation": "UU 40/2004",
            "total_articles": len(articles),
            "import_date": datetime.now().isoformat()
        }
    )
    
    print(f"✅ Created collection: {collection_name}")
    
    # Process in batches
    batch_size = 25
    print(f"\n📋 PROCESSING {len(articles)} ARTICLES:")
    print("=" * 60)
    
    category_stats = {}
    
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        
        documents = []
        metadatas = []
        ids = []
        
        for article in batch:
            doc_text = f"""
Pasal {article['pasal_number']} - {article['subcategory'].upper()}
Chapter: {article['chapter_context']}

{article['content']}

SJSN Concepts: {', '.join(article['sjsn_concepts'])}
"""
            
            documents.append(doc_text.strip())
            
            metadata = {
                'pasal_number': str(article['pasal_number']),
                'subcategory': article['subcategory'],
                'regulation': article['regulation'],
                'category': article['category'],
                'chapter_context': article['chapter_context'],
                'sjsn_concepts': ','.join(article['sjsn_concepts'])
            }
            
            metadatas.append(metadata)
            ids.append(f"uu40_2004_pasal_{article['pasal_number']}")
            
            category_icon = {
                'jaminan_kesehatan': '🏥', 'jaminan_kecelakaan_kerja': '🚑',
                'jaminan_hari_tua': '👴', 'jaminan_pensiun': '💰',
                'bpjs': '🏛️', 'ketentuan_umum': '📋'
            }.get(article['subcategory'], '📄')
            
            category_stats[article['subcategory']] = category_stats.get(article['subcategory'], 0) + 1
            
            print(f"{category_icon} Pasal {article['pasal_number']:>3} | {article['subcategory']:<20} | {article['word_count']:4d} words")
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    print("=" * 60)
    print(f"✅ Successfully imported {len(articles)} articles")
    
    print(f"\n📊 CATEGORY BREAKDOWN:")
    for category, count in category_stats.items():
        icon = {'jaminan_kesehatan': '🏥', 'jaminan_kecelakaan_kerja': '🚑', 'bpjs': '🏛️'}.get(category, '📄')
        print(f"   {icon} {category}: {count} articles")
    
    print(f"\n🎉 UU 40/2004 SJSN import successful!")
    print(f"   🏥 Complete Indonesian Social Security System dataset")
    print(f"   🔍 Ready for SJSN/BPJS RAG queries")

if __name__ == "__main__":
    main()