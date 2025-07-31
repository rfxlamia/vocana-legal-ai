"""
VOCANA DATABASE SETUP - Step 3: Test Semantic Search
Test semantic search functionality dengan legal queries yang realistic
"""

import chromadb
from typing import List, Dict, Any
import json

class VocanaSearchTester:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./vocana_chroma_db")
        self.collection = self.client.get_collection("vocana_legal_corpus")
        
    def search_legal_query(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """
        Perform semantic search dengan legal query
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            return {
                "query": query,
                "results_found": len(results["documents"][0]),
                "documents": results["documents"][0],
                "metadatas": results["metadatas"][0],
                "distances": results["distances"][0]
            }
            
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "results_found": 0
            }
    
    def format_search_result(self, result: Dict[str, Any]) -> str:
        """
        Format search result untuk display yang readable
        """
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        output = []
        output.append(f"🔍 Query: '{result['query']}'")
        output.append(f"📊 Found: {result['results_found']} relevant documents")
        output.append("-" * 50)
        
        for i, (doc, metadata, distance) in enumerate(zip(
            result["documents"], 
            result["metadatas"], 
            result["distances"]
        )):
            output.append(f"\n📄 Result #{i+1} (Relevance: {1-distance:.3f})")
            
            # Show key metadata
            if metadata.get("section"):
                output.append(f"   📍 Section: {metadata['section']}")
            if metadata.get("pasal_references"):
                output.append(f"   📜 Pasal: {metadata['pasal_references']}")
            if metadata.get("regulation_references"):
                output.append(f"   📋 Regulation: {metadata['regulation_references']}")
                
            # Show document excerpt (first 200 chars)
            doc_excerpt = doc[:200] + "..." if len(doc) > 200 else doc
            output.append(f"   💬 Content: {doc_excerpt}")
            output.append("")
        
        return "\n".join(output)
    
    def run_comprehensive_tests(self):
        """
        Run comprehensive test suite dengan real-world legal queries
        """
        print("🧪 VOCANA SEMANTIC SEARCH TESTING")
        print("=" * 60)
        
        # Test queries yang realistic untuk employment law
        test_queries = [
            {
                "query": "PKWT maksimal berapa tahun?",
                "expected_topics": ["durasi PKWT", "PP 35/2021", "5 tahun"]
            },
            {
                "query": "uang kompensasi PKWT cara menghitung",
                "expected_topics": ["kompensasi", "masa kerja/12", "upah sebulan"]
            },
            {
                "query": "masa percobaan PKWT boleh tidak?",
                "expected_topics": ["Pasal 58", "masa percobaan", "batal demi hukum"]
            },
            {
                "query": "upah minimum 2025 naik berapa persen?",
                "expected_topics": ["Permenaker 16/2024", "6,5%", "UMP"]
            },
            {
                "query": "pekerja caddy status PKWTT atau PKWT?",
                "expected_topics": ["PHI Semarang", "caddy", "PKWTT"]
            },
            {
                "query": "upah lembur perhitungan",
                "expected_topics": ["1,5x", "2x", "jam kerja"]
            },
            {
                "query": "penyelesaian sengketa bipartit mediasi",
                "expected_topics": ["UU 2/2004", "30 hari", "PHI"]
            }
        ]
        
        print(f"🎯 Running {len(test_queries)} test queries...\n")
        
        all_results = []
        passed_tests = 0
        
        for i, test in enumerate(test_queries, 1):
            print(f"🔍 TEST {i}/{len(test_queries)}")
            
            # Perform search
            result = self.search_legal_query(test["query"])
            all_results.append(result)
            
            # Display result
            formatted_result = self.format_search_result(result)
            print(formatted_result)
            
            # Simple relevance check
            if result["results_found"] > 0:
                # Check if any expected topics are found in results
                all_content = " ".join(result["documents"]).lower()
                found_topics = sum(1 for topic in test["expected_topics"] 
                                 if topic.lower() in all_content)
                
                if found_topics > 0:
                    print(f"✅ PASS: Found {found_topics}/{len(test['expected_topics'])} expected topics")
                    passed_tests += 1
                else:
                    print(f"⚠️  PARTIAL: Query returned results but may need tuning")
            else:
                print("❌ FAIL: No results found")
            
            print("\n" + "="*60 + "\n")
        
        # Summary
        print("📊 TEST SUMMARY")
        print(f"   Total tests: {len(test_queries)}")
        print(f"   Passed: {passed_tests}")
        print(f"   Success rate: {passed_tests/len(test_queries)*100:.1f}%")
        
        if passed_tests >= len(test_queries) * 0.8:  # 80% threshold
            print("\n✅ SEARCH FUNCTIONALITY: READY FOR PRODUCTION")
            return True
        else:
            print("\n⚠️  SEARCH FUNCTIONALITY: NEEDS TUNING")
            return False
    
    def get_collection_stats(self):
        """
        Display collection statistics
        """
        try:
            count = self.collection.count()
            
            # Get sample documents to check variety
            sample = self.collection.peek(limit=5)
            
            print("📊 COLLECTION STATISTICS")
            print("-" * 30)
            print(f"Total documents: {count}")
            print(f"Sample metadata fields: {list(sample['metadatas'][0].keys()) if sample['metadatas'] else 'None'}")
            
            # Check document types distribution
            if sample['metadatas']:
                document_types = {}
                sections = set()
                
                for metadata in sample['metadatas']:
                    doc_type = metadata.get('document_type', 'unknown')
                    document_types[doc_type] = document_types.get(doc_type, 0) + 1
                    
                    if metadata.get('section'):
                        sections.add(metadata['section'])
                
                print(f"Document types: {document_types}")
                print(f"Sections found: {len(sections)}")
                print(f"Sample sections: {list(sections)[:3]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return False

def main():
    print("🚀 VOCANA SEARCH TESTING & VALIDATION")
    print("=" * 60)
    
    try:
        tester = VocanaSearchTester()
        
        # Get collection stats first
        print("1️⃣ COLLECTION OVERVIEW")
        tester.get_collection_stats()
        print("\n")
        
        # Run comprehensive search tests
        print("2️⃣ SEMANTIC SEARCH TESTS")
        search_success = tester.run_comprehensive_tests()
        
        # Final recommendation
        print("🎯 FINAL STATUS")
        print("-" * 20)
        if search_success:
            print("✅ Vocana database is READY for n8n integration!")
            print("📋 Next steps:")
            print("   • Connect to n8n workflows")
            print("   • Test Claude API integration")
            print("   • Begin user testing")
        else:
            print("⚠️  Database needs optimization before production use")
            print("📋 Recommended actions:")
            print("   • Review search results above")
            print("   • Consider adjusting chunking strategy")
            print("   • Add more diverse legal content")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        print("   Make sure previous setup steps completed successfully")

if __name__ == "__main__":
    main()