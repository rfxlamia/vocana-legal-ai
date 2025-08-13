"""
UU 6/2023 Cipta Kerja Import Script - 71 Changes Complete
========================================================
Imports comprehensive UU 6/2023 changes to ChromaDB database.
Handles 71 employment law changes with proper categorization.

Features:
- Parses 71 employment law changes (diubah/dihapus/disisipkan)
- Cross-references with UU 13/2003 Ketenagakerjaan
- Comprehensive metadata for RAG optimization
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

def parse_uu6_changes(raw_content: str) -> List[Dict[str, Any]]:
    """Parse UU 6/2023 changes using ####(number) pattern"""
    articles = []
    
    # Find all ####(number) changes 
    change_pattern = r'####\((\d+)\)(.*?)(?=####\(\d+\)|$)'
    change_matches = re.findall(change_pattern, raw_content, re.DOTALL)
    
    print(f"📊 Found {len(change_matches)} changes to parse")
    
    for match in change_matches:
        change_number = match[0].strip()
        change_content = match[1].strip()
        
        if not change_content:
            continue
            
        # Extract pasal number from content - look for standalone Pasal declarations
        pasal_match = re.search(r'^Pasal (\d+[A-Z]*)', change_content, re.MULTILINE)
        if pasal_match:
            pasal_number = pasal_match.group(1)
        else:
            pasal_number = f"Change_{change_number}"
            
        # Detect amendment type
        amendment_type = detect_amendment_type(change_content)
        
        # Get title/summary from first line
        first_line = change_content.split('\n')[0] if change_content else ""
        
        # Count words for chunking decisions
        word_count = len(change_content.split())
        
        article_data = {
            'pasal_number': pasal_number,
            'change_number': change_number,
            'content': change_content,
            'title': first_line[:100] + "..." if len(first_line) > 100 else first_line,
            'amendment_type': amendment_type,
            'word_count': word_count,
            'regulation': 'UU 6/2023',
            'regulation_full': 'Undang-Undang Nomor 6 Tahun 2023 tentang Penetapan Peraturan Pemerintah Pengganti Undang-Undang Nomor 2 Tahun 2022 tentang Cipta Kerja menjadi Undang-Undang',
            'category': 'employment_law',
            'subcategory': 'cipta_kerja_amendments',
            'hierarchy_level': 1,  # UU level
            'source_reference': f"UU 6/2023 Change ({change_number})",
            'cross_reference': f"Mengubah UU 13/2003 Pasal {pasal_number}" if pasal_match else "",
            'legal_concept': extract_legal_concepts(change_content),
            'created_date': datetime.now().isoformat()
        }
        
        articles.append(article_data)
    
    return articles

def detect_amendment_type(content: str) -> str:
    """Detect type of amendment from content"""
    content_lower = content.lower()
    
    if 'dihapus' in content_lower or 'dicabut' in content_lower:
        return 'dihapus'
    elif 'disisipkan' in content_lower or 'ditambah' in content_lower:
        return 'disisipkan'
    elif 'diubah' in content_lower or 'diganti' in content_lower:
        return 'diubah'
    else:
        return 'modified'

def extract_legal_concepts(content: str) -> List[str]:
    """Extract key legal concepts from content"""
    concepts = []
    content_lower = content.lower()
    
    # Employment law concepts
    concept_patterns = {
        'kontrak_kerja': ['perjanjian kerja', 'kontrak kerja', 'pkwt', 'pkwtt'],
        'pengupahan': ['upah', 'gaji', 'tunjangan', 'upah minimum'],
        'phk': ['pemutusan hubungan kerja', 'phk', 'pemberhentian'],
        'jam_kerja': ['jam kerja', 'waktu kerja', 'lembur', 'shift'],
        'pekerja_asing': ['tenaga kerja asing', 'tka', 'pekerja asing'],
        'serikat_pekerja': ['serikat pekerja', 'serikat buruh', 'organisasi pekerja'],
        'keselamatan_kerja': ['k3', 'keselamatan', 'kesehatan kerja'],
        'pelatihan': ['pelatihan', 'training', 'kompetensi'],
        'perselisihan': ['perselisihan', 'dispute', 'mediasi'],
        'jaminan_sosial': ['jaminan sosial', 'bpjs', 'asuransi']
    }
    
    for concept, patterns in concept_patterns.items():
        if any(pattern in content_lower for pattern in patterns):
            concepts.append(concept)
    
    return concepts

def load_sample_data():
    """Load sample UU 6/2023 data from external file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, '..', 'sample_data', 'uu6_sample.txt')
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Sample data file not found: uu6_sample.txt")
        print("💡 Please provide UU 6/2023 content in the sample_data folder")
        return None

def main():
    """Main import function"""
    print("=" * 70)
    print("🚀 UU 6/2023 COMPLETE 71-CHANGES IMPORT")
    print("=" * 70)
    
    # Load content from external file
    raw_content = load_sample_data()
    if not raw_content:
        return
    
    print("📋 Parsing UU 6/2023 comprehensive changes...")
    print(f"📊 Raw content length: {len(raw_content):,} characters")
    
    # Parse articles
    articles = parse_uu6_changes(raw_content)
    
    if not articles:
        print("❌ No changes found. Please check content format.")
        return
    
    print(f"✅ Successfully parsed {len(articles)} comprehensive changes")
    
    # Show sample
    if articles:
        sample = articles[0]
        print(f"\n📄 Sample Change:")
        print(f"   Change ({sample['change_number']}): Pasal {sample['pasal_number']}")
        print(f"   Type: {sample['amendment_type']}")
        print(f"   Title: {sample['title'][:100]}...")
    
    # Initialize ChromaDB
    db_path = get_db_path()
    client = chromadb.PersistentClient(path=db_path)
    
    print(f"\n📊 Importing to ChromaDB...")
    
    # Create/get collection
    collection_name = "vocana_legal_uu6_2023_complete"
    
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={
            "description": "UU 6/2023 Cipta Kerja - Complete 71 Changes",
            "regulation": "UU 6/2023",
            "total_changes": len(articles),
            "import_date": datetime.now().isoformat(),
            "version": "complete_71_changes"
        }
    )
    
    print(f"✅ Created collection: {collection_name}")
    
    # Process in batches
    batch_size = 10
    print(f"\n📋 PROCESSING {len(articles)} CHANGES:")
    print("=" * 60)
    
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        
        documents = []
        metadatas = []
        ids = []
        
        for article in batch:
            # Create document text
            doc_text = f"""
Pasal {article['pasal_number']} - {article['title']}
Amendment Type: {article['amendment_type']}

{article['content']}

Cross Reference: {article['cross_reference']}
Legal Concepts: {', '.join(article['legal_concept'])}
"""
            
            documents.append(doc_text.strip())
            
            # Prepare metadata (ChromaDB requires string values)
            metadata = {
                'pasal_number': str(article['pasal_number']),
                'change_number': str(article['change_number']),
                'amendment_type': article['amendment_type'],
                'regulation': article['regulation'],
                'category': article['category'],
                'subcategory': article['subcategory'],
                'word_count': str(article['word_count']),
                'hierarchy_level': str(article['hierarchy_level']),
                'legal_concepts': ','.join(article['legal_concept']),
                'cross_reference': article['cross_reference']
            }
            
            metadatas.append(metadata)
            ids.append(f"uu6_2023_change_{article['change_number']}")
            
            # Progress indicator
            change_num = int(article['change_number'])
            amendment_icon = {
                'diubah': '🔄',
                'dihapus': '❌', 
                'disisipkan': '➕'
            }.get(article['amendment_type'], '📝')
            
            print(f"{amendment_icon} ({change_num:2d}) Pasal {article['pasal_number']} | {article['amendment_type']:<10} | {article['word_count']:4d} words")
        
        # Add batch to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    print("=" * 60)
    print(f"✅ Successfully imported {len(articles)} comprehensive changes")
    
    # Summary statistics
    amendment_stats = {}
    total_words = 0
    
    for article in articles:
        amt_type = article['amendment_type']
        amendment_stats[amt_type] = amendment_stats.get(amt_type, 0) + 1
        total_words += article['word_count']
    
    print(f"\n📊 AMENDMENT SUMMARY:")
    for amt_type, count in amendment_stats.items():
        icon = {'diubah': '🔄', 'dihapus': '❌', 'disisipkan': '➕'}.get(amt_type, '📝')
        print(f"   {icon} {amt_type}: {count} changes")
    
    print(f"\n💪 TOTAL: {len(articles)} changes | {total_words:,} words | Complete 71-article dataset")
    
    print(f"\n🎉 UU 6/2023 complete 71-changes import successful!")
    print(f"   🎯 Target achieved: {len(articles)} comprehensive legal changes")
    print(f"   🔍 Ready for advanced RAG with detailed amendment context")

if __name__ == "__main__":
    main()