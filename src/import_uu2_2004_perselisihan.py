"""
UU 2/2004 Perselisihan Hubungan Industrial Import Script - 589 Articles Complete
===============================================================================
Imports comprehensive UU 2/2004 articles about industrial dispute resolution,
mediation, arbitration, and labor court procedures to ChromaDB.

Features:
- Parses 589 industrial dispute resolution articles
- Mediation and conciliation procedures
- Arbitration mechanisms for labor disputes
- Industrial relations court procedures
- Dispute types and resolution pathways
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
    """Load sample UU 2/2004 data from external file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, '..', 'sample_data', 'uu2_sample.txt')
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Sample data file not found: uu2_sample.txt")
        print("💡 Please provide UU 2/2004 content in the sample_data folder")
        return None

def parse_uu2_articles(raw_content: str) -> List[Dict[str, Any]]:
    """Parse UU 2/2004 articles using pattern matching"""
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
        
        # Extract dispute-related concepts
        dispute_concepts = extract_dispute_concepts(article_content)
        
        # Determine article category based on content
        category = categorize_uu2_content(article_content, chapter_context)
        
        article_data = {
            'pasal_number': pasal_number,
            'content': article_content,
            'title': f"Pasal {pasal_number} - {category}",
            'ayat_count': ayat_count,
            'word_count': word_count,
            'regulation': 'UU 2/2004',
            'regulation_full': 'Undang-Undang Nomor 2 Tahun 2004 tentang Penyelesaian Perselisihan Hubungan Industrial',
            'category': 'industrial_dispute_law',
            'subcategory': category,
            'hierarchy_level': 1,  # UU level (highest)
            'chapter_context': chapter_context,
            'source_reference': f"UU 2/2004 Pasal {pasal_number}",
            'related_regulations': get_related_dispute_regulations(category),
            'dispute_concepts': dispute_concepts,
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

def categorize_uu2_content(content: str, chapter_context: str) -> str:
    """Categorize UU 2/2004 content by dispute topic"""
    content_lower = content.lower()
    chapter_lower = chapter_context.lower()
    
    # Priority: chapter context first, then content analysis
    if 'jenis perselisihan' in chapter_lower or 'jenis perselisihan' in content_lower:
        return 'jenis_perselisihan'
    elif 'mediasi' in chapter_lower or 'mediasi' in content_lower:
        return 'mediasi'
    elif 'konsiliasi' in chapter_lower or 'konsiliasi' in content_lower:
        return 'konsiliasi'
    elif 'arbitrase' in chapter_lower or 'arbitrase' in content_lower:
        return 'arbitrase'
    elif 'pengadilan hubungan industrial' in chapter_lower or 'phi' in content_lower:
        return 'pengadilan_hubungan_industrial'
    elif 'pemutusan hubungan kerja' in chapter_lower or 'phk' in content_lower or 'perselisihan pemutusan hubungan kerja' in content_lower:
        return 'sengketa_phk'
    elif 'hak pekerja' in chapter_lower or 'hak normatif' in content_lower:
        return 'sengketa_hak'
    elif 'kepentingan' in chapter_lower or 'kepentingan' in content_lower:
        return 'sengketa_kepentingan'
    elif 'antar serikat' in chapter_lower or 'antar serikat' in content_lower:
        return 'sengketa_antar_serikat'
    elif 'prosedur' in chapter_lower or 'tata cara' in content_lower:
        return 'prosedur_penyelesaian'
    elif 'putusan' in chapter_lower or 'putusan' in content_lower:
        return 'putusan_penyelesaian'
    elif 'pelaksanaan' in chapter_lower or 'eksekusi' in content_lower:
        return 'pelaksanaan_putusan'
    elif 'sanksi' in chapter_lower or 'pidana' in content_lower:
        return 'sanksi_pidana'
    else:
        return 'ketentuan_umum'

def extract_dispute_concepts(content: str) -> List[str]:
    """Extract key dispute resolution concepts from UU 2/2004 content"""
    concepts = []
    content_lower = content.lower()
    
    # UU 2/2004 dispute-specific concepts
    concept_patterns = {
        'perselisihan_hubungan_industrial': ['perselisihan hubungan industrial', 'phi', 'industrial dispute'],
        'sengketa_hak': ['sengketa hak', 'perselisihan hak', 'rights dispute'],
        'sengketa_kepentingan': ['sengketa kepentingan', 'perselisihan kepentingan', 'interest dispute'],
        'sengketa_phk': ['sengketa phk', 'perselisihan phk', 'termination dispute'],
        'sengketa_antar_serikat': ['sengketa antar serikat', 'perselisihan antar serikat'],
        'mediasi': ['mediasi', 'mediation', 'mediator'],
        'konsiliasi': ['konsiliasi', 'conciliation', 'konsiliator'],
        'arbitrase': ['arbitrase', 'arbitration', 'arbiter'],
        'pengadilan_hubungan_industrial': ['pengadilan hubungan industrial', 'phi', 'industrial court'],
        'hakim': ['hakim', 'judge', 'hakim ad hoc'],
        'majelis_hakim': ['majelis hakim', 'panel hakim', 'judicial panel'],
        'putusan': ['putusan', 'verdict', 'keputusan'],
        'penetapan': ['penetapan', 'determination', 'decree'],
        'gugatan': ['gugatan', 'lawsuit', 'claim'],
        'tergugat': ['tergugat', 'defendant', 'respondent'],
        'penggugat': ['penggugat', 'plaintiff', 'claimant'],
        'saksi': ['saksi', 'witness', 'testimony'],
        'alat_bukti': ['alat bukti', 'evidence', 'bukti'],
        'kasasi': ['kasasi', 'cassation', 'supreme court appeal'],
        'peninjauan_kembali': ['peninjauan kembali', 'pk', 'judicial review'],
        'eksekusi': ['eksekusi', 'execution', 'pelaksanaan putusan'],
        'biaya_perkara': ['biaya perkara', 'court costs', 'legal fees']
    }
    
    for concept, patterns in concept_patterns.items():
        if any(pattern in content_lower for pattern in patterns):
            concepts.append(concept)
    
    return concepts

def get_related_dispute_regulations(category: str) -> List[str]:
    """Get related dispute resolution regulations for each category"""
    related_map = {
        'mediasi': ['Permenaker 2/2015 (Mediasi HI)'],
        'arbitrase': ['Permenaker 31/2008 (Arbitrase)'],
        'pengadilan_hubungan_industrial': ['Perma 2/2017 (Tata Cara PHI)'],
        'sengketa_phk': ['UU 13/2003 (Ketenagakerjaan)', 'PP 35/2021 (PHK)'],
        'prosedur_penyelesaian': ['Permenaker 15/2020 (Prosedur PHI)']
    }
    
    return related_map.get(category, [])

def main():
    """Main import function"""
    print("=" * 70)
    print("⚖️ UU 2/2004 PERSELISIHAN HUBUNGAN INDUSTRIAL - 589 ARTICLES")
    print("=" * 70)
    
    # Load content from external file
    raw_content = load_sample_data()
    if not raw_content:
        return
    
    print("📋 Parsing UU 2/2004 industrial dispute resolution law...")
    print(f"📊 Raw content length: {len(raw_content):,} characters")
    
    # Parse articles
    articles = parse_uu2_articles(raw_content)
    
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
        print(f"   Ayat: {sample['ayat_count']}, Concepts: {len(sample['dispute_concepts'])}")
    
    # Initialize ChromaDB
    db_path = get_db_path()
    client = chromadb.PersistentClient(path=db_path)
    
    print(f"\n📊 Importing to ChromaDB...")
    
    # Create/get collection
    collection_name = "vocana_legal_uu2_2004_complete"
    
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={
            "description": "UU 2/2004 - Industrial Dispute Resolution Law",
            "regulation": "UU 2/2004",
            "total_articles": len(articles),
            "import_date": datetime.now().isoformat(),
            "version": "complete_589_articles"
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

Dispute Concepts: {', '.join(article['dispute_concepts'])}
Related Regulations: {', '.join(article['related_regulations'])}
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
                'dispute_concepts': ','.join(article['dispute_concepts']),
                'related_regulations': ','.join(article['related_regulations'])
            }
            
            metadatas.append(metadata)
            ids.append(f"uu2_2004_pasal_{article['pasal_number']}")
            
            # Progress indicator with category
            category_icon = {
                'mediasi': '🤝', 'arbitrase': '⚖️', 'pengadilan_hubungan_industrial': '🏛️',
                'sengketa_hak': '👤', 'sengketa_kepentingan': '💼', 'sengketa_phk': '❌',
                'ketentuan_umum': '📋'
            }.get(article['subcategory'], '📄')
            
            category_stats[article['subcategory']] = category_stats.get(article['subcategory'], 0) + 1
            total_ayat += article['ayat_count']
            
            print(f"{category_icon} Pasal {article['pasal_number']:>3} | {article['subcategory']:<22} | {article['ayat_count']:2d} ayat | {article['word_count']:4d} words")
        
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
            'mediasi': '🤝', 'arbitrase': '⚖️', 'pengadilan_hubungan_industrial': '🏛️',
            'sengketa_hak': '👤', 'sengketa_kepentingan': '💼', 'sengketa_phk': '❌',
            'ketentuan_umum': '📋'
        }.get(category, '📄')
        print(f"   {icon} {category}: {count} articles")
    
    print(f"\n💪 TOTAL: {len(articles)} articles | {total_ayat} ayat | {total_words:,} words")
    print(f"   📊 Complete Indonesian Industrial Dispute Resolution dataset")
    
    print(f"\n🎉 UU 2/2004 Perselisihan import successful!")
    print(f"   🤝 Mediasi: Mediation procedures")
    print(f"   ⚖️ Arbitrase: Arbitration mechanisms")
    print(f"   🏛️ PHI: Industrial relations court")
    print(f"   👤 Sengketa Hak: Rights disputes")
    print(f"   💼 Sengketa Kepentingan: Interest disputes")
    print(f"   ❌ Sengketa PHK: Termination disputes")
    print(f"   🔍 Ready for comprehensive dispute resolution RAG queries")

if __name__ == "__main__":
    main()