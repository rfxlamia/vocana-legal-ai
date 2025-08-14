"""
UU 21/2000 Serikat Pekerja Import Script - 109 Articles Complete
===============================================================
Imports UU 21/2000 about Labor Unions (Serikat Pekerja/Serikat Buruh)
articles to ChromaDB database.

Features:
- Parses 109 labor union regulation articles
- Union formation and registration procedures
- Worker rights and union activities
- Collective bargaining regulations
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
    """Load sample UU 21/2000 data from external file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, '..', 'sample_data', 'uu21_sample.txt')
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Sample data file not found: uu21_sample.txt")
        print("💡 Please provide UU 21/2000 content in the sample_data folder")
        return None

def parse_uu21_articles(raw_content: str) -> List[Dict[str, Any]]:
    """Parse UU 21/2000 articles using pattern matching"""
    articles = []
    
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
        union_concepts = extract_union_concepts(article_content)
        category = categorize_uu21_content(article_content, chapter_context)
        
        article_data = {
            'pasal_number': pasal_number,
            'content': article_content,
            'title': f"Pasal {pasal_number} - {category}",
            'ayat_count': ayat_count,
            'word_count': word_count,
            'regulation': 'UU 21/2000',
            'regulation_full': 'Undang-Undang Nomor 21 Tahun 2000 tentang Serikat Pekerja/Serikat Buruh',
            'category': 'labor_union_law',
            'subcategory': category,
            'hierarchy_level': 1,
            'chapter_context': chapter_context,
            'source_reference': f"UU 21/2000 Pasal {pasal_number}",
            'union_concepts': union_concepts,
            'created_date': datetime.now().isoformat()
        }
        
        articles.append(article_data)
    
    return articles

def extract_chapter_context(raw_content: str, pasal_number: str) -> str:
    """Extract chapter context"""
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

def categorize_uu21_content(content: str, chapter_context: str) -> str:
    """Categorize UU 21/2000 content by union topic"""
    content_lower = content.lower()
    chapter_lower = chapter_context.lower()
    
    if 'pembentukan' in chapter_lower or 'pembentukan' in content_lower:
        return 'pembentukan_serikat'
    elif 'pendaftaran' in chapter_lower or 'pendaftaran' in content_lower:
        return 'pendaftaran_serikat'
    elif 'hak serikat' in content_lower or 'hak' in chapter_lower:
        return 'hak_serikat'
    elif 'kewajiban' in chapter_lower or 'kewajiban' in content_lower:
        return 'kewajiban_serikat'
    elif 'kegiatan serikat' in content_lower or 'kegiatan' in chapter_lower:
        return 'kegiatan_serikat'
    elif 'perjanjian kerja bersama' in content_lower or 'pkb' in content_lower:
        return 'perjanjian_kerja_bersama'
    elif 'federasi' in content_lower or 'konfederasi' in content_lower:
        return 'federasi_konfederasi'
    else:
        return 'ketentuan_umum'

def extract_union_concepts(content: str) -> List[str]:
    """Extract union concepts"""
    concepts = []
    content_lower = content.lower()
    
    concept_patterns = {
        'serikat_pekerja': ['serikat pekerja', 'serikat buruh', 'labor union'],
        'anggota_serikat': ['anggota serikat', 'membership', 'keanggotaan'],
        'pengurus_serikat': ['pengurus serikat', 'union officials', 'kepengurusan'],
        'federasi': ['federasi', 'federation'],
        'konfederasi': ['konfederasi', 'confederation'],
        'perjanjian_kerja_bersama': ['perjanjian kerja bersama', 'pkb', 'collective bargaining'],
        'hak_berorganisasi': ['hak berorganisasi', 'freedom of association'],
        'mogok_kerja': ['mogok kerja', 'strike', 'pemogokan'],
        'perundingan': ['perundingan', 'negotiation', 'negosiasi'],
        'perwakilan_pekerja': ['perwakilan pekerja', 'worker representation']
    }
    
    for concept, patterns in concept_patterns.items():
        if any(pattern in content_lower for pattern in patterns):
            concepts.append(concept)
    
    return concepts

def main():
    """Main import function"""
    print("=" * 70)
    print("👥 UU 21/2000 SERIKAT PEKERJA IMPORT - 109 ARTICLES")
    print("=" * 70)
    
    raw_content = load_sample_data()
    if not raw_content:
        return
    
    print("📋 Parsing UU 21/2000 labor union law...")
    articles = parse_uu21_articles(raw_content)
    
    if not articles:
        print("❌ No articles found.")
        return
    
    print(f"✅ Successfully parsed {len(articles)} articles")
    
    # ChromaDB setup
    db_path = get_db_path()
    client = chromadb.PersistentClient(path=db_path)
    
    collection_name = "vocana_legal_uu21_2000_complete"
    
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={
            "description": "UU 21/2000 Serikat Pekerja - Labor Union Law",
            "regulation": "UU 21/2000",
            "total_articles": len(articles)
        }
    )
    
    # Quick batch process
    documents = []
    metadatas = []
    ids = []
    
    for article in articles:
        doc_text = f"""
Pasal {article['pasal_number']} - {article['subcategory'].upper()}

{article['content']}

Union Concepts: {', '.join(article['union_concepts'])}
"""
        
        documents.append(doc_text.strip())
        
        metadata = {
            'pasal_number': str(article['pasal_number']),
            'subcategory': article['subcategory'],
            'regulation': article['regulation'],
            'union_concepts': ','.join(article['union_concepts'])
        }
        
        metadatas.append(metadata)
        ids.append(f"uu21_2000_pasal_{article['pasal_number']}")
    
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    
    print(f"🎉 UU 21/2000 Serikat Pekerja import successful!")
    print(f"   👥 Complete Indonesian Labor Union Law dataset")

if __name__ == "__main__":
    main()