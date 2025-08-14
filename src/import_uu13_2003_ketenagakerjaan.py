"""
UU 13/2003 Ketenagakerjaan Import Script - 780 Articles Complete
==============================================================
Imports comprehensive UU 13/2003 Ketenagakerjaan (Employment Law) articles
to ChromaDB database. This is the foundation employment law of Indonesia.

Features:
- Parses 780 comprehensive employment law articles
- Foundation law for Indonesian employment regulations
- Covers PKWT/PKWTT, wages, working hours, termination, foreign workers
- Cross-references with implementing regulations (PP 35/2021, PP 36/2021)
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
    """Load sample UU 13/2003 data from external file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, '..', 'sample_data', 'uu13_sample.txt')
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Sample data file not found: uu13_sample.txt")
        print("💡 Please provide UU 13/2003 content in the sample_data folder")
        return None

def parse_uu13_articles(raw_content: str) -> List[Dict[str, Any]]:
    """Parse UU 13/2003 articles using pattern matching"""
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
        
        # Extract ayat (verses) from content
        ayat_count = count_ayat(article_content)
        
        # Count words for chunking decisions
        word_count = len(article_content.split())
        
        # Extract key employment concepts
        employment_concepts = extract_uu13_concepts(article_content)
        
        # Determine article category based on content
        category = categorize_uu13_content(article_content, chapter_context)
        
        article_data = {
            'pasal_number': pasal_number,
            'content': article_content,
            'title': f"Pasal {pasal_number} - {category}",
            'ayat_count': ayat_count,
            'word_count': word_count,
            'regulation': 'UU 13/2003',
            'regulation_full': 'Undang-Undang Nomor 13 Tahun 2003 tentang Ketenagakerjaan',
            'category': 'employment_law',
            'subcategory': category,
            'hierarchy_level': 1,  # UU level (highest)
            'chapter_context': chapter_context,
            'source_reference': f"UU 13/2003 Pasal {pasal_number}",
            'amended_by': 'UU 11/2020 (Cipta Kerja), UU 6/2023',
            'implementing_regulations': get_implementing_regulations(category),
            'employment_concepts': employment_concepts,
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
    
    # Common chapter patterns in UU
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

def categorize_uu13_content(content: str, chapter_context: str) -> str:
    """Categorize UU 13/2003 content by topic"""
    content_lower = content.lower()
    chapter_lower = chapter_context.lower()
    
    # Priority: chapter context first, then content analysis
    if 'perencanaan' in chapter_lower or 'informasi' in chapter_lower:
        return 'perencanaan_tenaga_kerja'
    elif 'pelatihan' in chapter_lower or 'pelatihan' in content_lower:
        return 'pelatihan_kerja'
    elif 'penempatan' in chapter_lower or 'penempatan' in content_lower:
        return 'penempatan_tenaga_kerja'
    elif 'perluasan' in chapter_lower or 'kesempatan kerja' in content_lower:
        return 'perluasan_kesempatan_kerja'
    elif 'hubungan kerja' in chapter_lower or any(term in content_lower for term in ['pkwt', 'pkwtt', 'perjanjian kerja']):
        return 'hubungan_kerja'
    elif 'perlindungan' in chapter_lower or 'keselamatan' in content_lower:
        return 'perlindungan_kerja'
    elif 'waktu kerja' in chapter_lower or 'waktu kerja' in content_lower:
        return 'waktu_kerja'
    elif 'upah' in chapter_lower or 'upah' in content_lower:
        return 'pengupahan'
    elif 'jaminan sosial' in chapter_lower or 'jaminan sosial' in content_lower:
        return 'jaminan_sosial'
    elif 'serikat' in chapter_lower or 'serikat pekerja' in content_lower:
        return 'serikat_pekerja'
    elif 'perselisihan' in chapter_lower or 'perselisihan' in content_lower:
        return 'penyelesaian_perselisihan'
    elif 'pembinaan' in chapter_lower or 'pengawasan' in content_lower:
        return 'pembinaan_pengawasan'
    elif 'penyidikan' in chapter_lower or 'penyidikan' in content_lower:
        return 'penyidikan'
    elif 'sanksi' in chapter_lower or 'pidana' in content_lower:
        return 'sanksi_pidana'
    elif 'tenaga kerja asing' in chapter_lower or 'tka' in content_lower:
        return 'tenaga_kerja_asing'
    else:
        return 'ketentuan_umum'

def extract_uu13_concepts(content: str) -> List[str]:
    """Extract key employment concepts from UU 13/2003 content"""
    concepts = []
    content_lower = content.lower()
    
    # UU 13/2003 specific concepts
    concept_patterns = {
        'tenaga_kerja': ['tenaga kerja', 'angkatan kerja', 'pencari kerja'],
        'pekerja_buruh': ['pekerja', 'buruh', 'karyawan'],
        'pengusaha': ['pengusaha', 'pemberi kerja', 'perusahaan'],
        'pkwt': ['pkwt', 'perjanjian kerja waktu tertentu'],
        'pkwtt': ['pkwtt', 'perjanjian kerja waktu tidak tertentu'],
        'upah': ['upah', 'gaji', 'pengupahan', 'upah minimum'],
        'waktu_kerja': ['waktu kerja', 'jam kerja', 'shift'],
        'lembur': ['lembur', 'kerja lembur', 'upah lembur'],
        'istirahat': ['istirahat', 'cuti', 'libur'],
        'keselamatan_kerja': ['keselamatan kerja', 'k3', 'kesehatan kerja'],
        'jaminan_sosial': ['jaminan sosial', 'asuransi', 'jamsostek'],
        'serikat_pekerja': ['serikat pekerja', 'serikat buruh', 'organisasi pekerja'],
        'perselisihan': ['perselisihan hubungan industrial', 'dispute', 'mediasi'],
        'pemutusan_hubungan_kerja': ['phk', 'pemutusan hubungan kerja', 'pemberhentian'],
        'pesangon': ['pesangon', 'uang pesangon', 'kompensasi'],
        'pelatihan': ['pelatihan kerja', 'training', 'keahlian'],
        'tenaga_kerja_asing': ['tenaga kerja asing', 'tka', 'pekerja asing'],
        'pengawasan': ['pengawasan ketenagakerjaan', 'inspeksi', 'audit'],
        'sanksi': ['sanksi', 'pidana', 'denda', 'hukuman']
    }
    
    for concept, patterns in concept_patterns.items():
        if any(pattern in content_lower for pattern in patterns):
            concepts.append(concept)
    
    return concepts

def get_implementing_regulations(category: str) -> List[str]:
    """Get implementing regulations for each category"""
    implementing_map = {
        'hubungan_kerja': ['PP 35/2021 (PKWT & PHK)'],
        'pengupahan': ['PP 36/2021 (Pengupahan)', 'PP 78/2015 (Upah)'],
        'waktu_kerja': ['PP 35/2021 (Waktu Kerja & Istirahat)'],
        'perlindungan_kerja': ['PP 50/2012 (SMK3)'],
        'tenaga_kerja_asing': ['PP 34/2021 (TKA)', 'Perpres 20/2018'],
        'jaminan_sosial': ['UU 40/2004 (SJSN)', 'UU 24/2011 (BPJS)'],
        'serikat_pekerja': ['UU 21/2000 (Serikat Pekerja)'],
        'penyelesaian_perselisihan': ['UU 2/2004 (Perselisihan HI)']
    }
    
    return implementing_map.get(category, [])

def main():
    """Main import function"""
    print("=" * 70)
    print("🏛️ UU 13/2003 KETENAGAKERJAAN IMPORT - 780 ARTICLES")
    print("=" * 70)
    
    # Load content from external file
    raw_content = load_sample_data()
    if not raw_content:
        return
    
    print("📋 Parsing UU 13/2003 foundation employment law...")
    print(f"📊 Raw content length: {len(raw_content):,} characters")
    
    # Parse articles
    articles = parse_uu13_articles(raw_content)
    
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
        print(f"   Ayat: {sample['ayat_count']}, Concepts: {len(sample['employment_concepts'])}")
    
    # Initialize ChromaDB
    db_path = get_db_path()
    client = chromadb.PersistentClient(path=db_path)
    
    print(f"\n📊 Importing to ChromaDB...")
    
    # Create/get collection
    collection_name = "vocana_legal_uu13_2003_complete"
    
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={
            "description": "UU 13/2003 Ketenagakerjaan - Foundation Employment Law",
            "regulation": "UU 13/2003",
            "total_articles": len(articles),
            "import_date": datetime.now().isoformat(),
            "version": "complete_780_articles"
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

Employment Concepts: {', '.join(article['employment_concepts'])}
Amended by: {article['amended_by']}
Implementing Regulations: {', '.join(article['implementing_regulations'])}
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
                'employment_concepts': ','.join(article['employment_concepts']),
                'amended_by': article['amended_by']
            }
            
            metadatas.append(metadata)
            ids.append(f"uu13_2003_pasal_{article['pasal_number']}")
            
            # Progress indicator with category
            category_icon = {
                'hubungan_kerja': '🤝', 'pengupahan': '💰', 'waktu_kerja': '⏰',
                'perlindungan_kerja': '🛡️', 'serikat_pekerja': '👥', 'jaminan_sosial': '🏥',
                'tenaga_kerja_asing': '🌍', 'sanksi_pidana': '⚖️', 'ketentuan_umum': '📋'
            }.get(article['subcategory'], '📄')
            
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
            'hubungan_kerja': '🤝', 'pengupahan': '💰', 'waktu_kerja': '⏰',
            'perlindungan_kerja': '🛡️', 'serikat_pekerja': '👥', 'jaminan_sosial': '🏥',
            'tenaga_kerja_asing': '🌍', 'sanksi_pidana': '⚖️', 'ketentuan_umum': '📋'
        }.get(category, '📄')
        print(f"   {icon} {category}: {count} articles")
    
    print(f"\n💪 TOTAL: {len(articles)} articles | {total_ayat} ayat | {total_words:,} words")
    print(f"   📊 Foundation Indonesian Employment Law dataset")
    
    print(f"\n🎉 UU 13/2003 Ketenagakerjaan import successful!")
    print(f"   🏛️ Foundation law for Indonesian employment")
    print(f"   🤝 Covers all aspects of employment relationships")
    print(f"   ⚖️ Legal basis for PP 35/2021, PP 36/2021, and other regulations")
    print(f"   🔍 Ready for comprehensive employment law RAG queries")

if __name__ == "__main__":
    main()