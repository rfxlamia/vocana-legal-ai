"""
PP 35/2021 PKWT & PHK Import Script - 336 Articles Complete
==========================================================
Imports comprehensive PP 35/2021 articles about employment contracts,
outsourcing, working hours, and termination procedures to ChromaDB.

Features:
- Parses 336 employment regulation articles
- PKWT (fixed-term contract) regulations
- Outsourcing and working hours rules
- PHK (termination) procedures
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
    """Load sample PP 35/2021 data from external file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, '..', 'sample_data', 'pp35_sample.txt')
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Sample data file not found: pp35_sample.txt")
        print("💡 Please provide PP 35/2021 content in the sample_data folder")
        return None

def parse_pp35_articles(raw_content: str) -> List[Dict[str, Any]]:
    """Parse PP 35/2021 articles using pattern matching"""
    articles = []
    
    # Find all articles using multiple patterns
    patterns = [
        r'#{4,5} Pasal (\d+[A-Z]*)(.*?)(?=#{4,5} Pasal \d+|$)',  # Main pattern
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
        
        # Count words for chunking decisions
        word_count = len(article_content.split())
        
        # Extract key employment concepts
        employment_concepts = extract_employment_concepts(article_content)
        
        # Determine article category based on content
        category = categorize_pp35_content(article_content)
        
        article_data = {
            'pasal_number': pasal_number,
            'content': article_content,
            'title': f"Pasal {pasal_number} - {category}",
            'word_count': word_count,
            'regulation': 'PP 35/2021',
            'regulation_full': 'Peraturan Pemerintah Nomor 35 Tahun 2021 tentang Perjanjian Kerja Waktu Tertentu, Alih Daya, Waktu Kerja dan Waktu Istirahat, dan Pemutusan Hubungan Kerja',
            'category': 'employment_regulation',
            'subcategory': category,
            'hierarchy_level': 2,  # PP level
            'chapter_context': chapter_context,
            'source_reference': f"PP 35/2021 Pasal {pasal_number}",
            'implements_regulation': 'UU 11/2020 (Cipta Kerja)',
            'related_uu': 'UU 13/2003 (Ketenagakerjaan)',
            'employment_concepts': employment_concepts,
            'created_date': datetime.now().isoformat()
        }
        
        articles.append(article_data)
    
    return articles

def extract_chapter_context(raw_content: str, pasal_number: str) -> str:
    """Extract chapter/section context for the article"""
    # Look for chapter headings before the article
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
            return matches[-1].strip()  # Get the last (closest) match
    
    return "General"

def categorize_pp35_content(content: str) -> str:
    """Categorize PP 35/2021 content by topic"""
    content_lower = content.lower()
    
    if any(term in content_lower for term in ['pkwt', 'perjanjian kerja waktu tertentu', 'kontrak']):
        return 'pkwt'
    elif any(term in content_lower for term in ['alih daya', 'outsourcing', 'pemborongan']):
        return 'alih_daya'
    elif any(term in content_lower for term in ['waktu kerja', 'jam kerja', 'shift', 'lembur']):
        return 'waktu_kerja'
    elif any(term in content_lower for term in ['phk', 'pemutusan hubungan kerja', 'pemberhentian']):
        return 'phk'
    elif any(term in content_lower for term in ['istirahat', 'cuti', 'libur']):
        return 'waktu_istirahat'
    else:
        return 'umum'

def extract_employment_concepts(content: str) -> List[str]:
    """Extract key employment concepts from PP 35/2021 content"""
    concepts = []
    content_lower = content.lower()
    
    # PP 35/2021 specific concepts
    concept_patterns = {
        'pkwt': ['pkwt', 'perjanjian kerja waktu tertentu', 'kontrak tetap'],
        'pkwtt': ['pkwtt', 'perjanjian kerja waktu tidak tertentu', 'permanent'],
        'alih_daya': ['alih daya', 'outsourcing', 'pemborongan pekerjaan'],
        'waktu_kerja': ['waktu kerja', 'jam kerja', 'shift kerja'],
        'lembur': ['lembur', 'kerja lembur', 'overtime'],
        'istirahat': ['waktu istirahat', 'istirahat kerja', 'break'],
        'cuti': ['cuti', 'leave', 'libur'],
        'phk': ['phk', 'pemutusan hubungan kerja', 'termination'],
        'pesangon': ['pesangon', 'uang pesangon', 'severance'],
        'skorsing': ['skorsing', 'suspend', 'pemberhentian sementara'],
        'pelanggaran': ['pelanggaran', 'violation', 'kesalahan'],
        'peringatan': ['surat peringatan', 'warning', 'teguran'],
        'prosedur': ['prosedur', 'tata cara', 'procedure']
    }
    
    for concept, patterns in concept_patterns.items():
        if any(pattern in content_lower for pattern in patterns):
            concepts.append(concept)
    
    return concepts

def main():
    """Main import function"""
    print("=" * 70)
    print("🚀 PP 35/2021 PKWT & PHK IMPORT - 336 ARTICLES")
    print("=" * 70)
    
    # Load content from external file
    raw_content = load_sample_data()
    if not raw_content:
        return
    
    print("📋 Parsing PP 35/2021 employment regulations...")
    print(f"📊 Raw content length: {len(raw_content):,} characters")
    
    # Parse articles
    articles = parse_pp35_articles(raw_content)
    
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
        print(f"   Concepts: {', '.join(sample['employment_concepts'][:3])}")
    
    # Initialize ChromaDB
    db_path = get_db_path()
    client = chromadb.PersistentClient(path=db_path)
    
    print(f"\n📊 Importing to ChromaDB...")
    
    # Create/get collection
    collection_name = "vocana_legal_pp35_2021_complete"
    
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={
            "description": "PP 35/2021 - PKWT, Alih Daya, Waktu Kerja & PHK",
            "regulation": "PP 35/2021",
            "total_articles": len(articles),
            "import_date": datetime.now().isoformat(),
            "version": "complete_336_articles"
        }
    )
    
    print(f"✅ Created collection: {collection_name}")
    
    # Process in batches
    batch_size = 20
    print(f"\n📋 PROCESSING {len(articles)} ARTICLES:")
    print("=" * 60)
    
    category_stats = {}
    
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

{article['content']}

Employment Concepts: {', '.join(article['employment_concepts'])}
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
                'word_count': str(article['word_count']),
                'hierarchy_level': str(article['hierarchy_level']),
                'chapter_context': article['chapter_context'],
                'employment_concepts': ','.join(article['employment_concepts']),
                'implements_regulation': article['implements_regulation']
            }
            
            metadatas.append(metadata)
            ids.append(f"pp35_2021_pasal_{article['pasal_number']}")
            
            # Progress indicator with category
            category_icon = {
                'pkwt': '📝', 'alih_daya': '🔄', 'waktu_kerja': '⏰',
                'phk': '❌', 'waktu_istirahat': '😴', 'umum': '📋'
            }.get(article['subcategory'], '📄')
            
            category_stats[article['subcategory']] = category_stats.get(article['subcategory'], 0) + 1
            
            print(f"{category_icon} Pasal {article['pasal_number']:>3} | {article['subcategory']:<12} | {article['word_count']:4d} words | {article['chapter_context'][:20]}...")
        
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
    
    for category, count in category_stats.items():
        icon = {'pkwt': '📝', 'alih_daya': '🔄', 'waktu_kerja': '⏰', 'phk': '❌', 'waktu_istirahat': '😴', 'umum': '📋'}.get(category, '📄')
        print(f"   {icon} {category}: {count} articles")
    
    print(f"\n💪 TOTAL: {len(articles)} articles | {total_words:,} words | Complete PP 35/2021 dataset")
    
    print(f"\n🎉 PP 35/2021 PKWT & PHK import successful!")
    print(f"   📝 PKWT: Contract regulations")
    print(f"   🔄 Alih Daya: Outsourcing rules") 
    print(f"   ⏰ Waktu Kerja: Working hours")
    print(f"   ❌ PHK: Termination procedures")
    print(f"   🔍 Ready for employment law RAG queries")

if __name__ == "__main__":
    main()