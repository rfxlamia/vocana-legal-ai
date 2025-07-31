"""
VOCANA DATABASE SETUP - Step 1: Create Legal Collection
Membuat ChromaDB collection untuk legal corpus Vocana
"""

import chromadb
import datetime

def create_vocana_collection():
    print("🚀 VOCANA DATABASE SETUP - Creating Legal Collection")
    print("=" * 60)
    
    try:
        # Initialize ChromaDB client (updated syntax for v1.0.15+)
        client = chromadb.PersistentClient(path="./vocana_chroma_db")
        
        print("✅ ChromaDB client initialized")
        
        # Create collection untuk legal corpus (fixed metadata)
        collection = client.create_collection(
            name="vocana_legal_corpus",
            metadata={
                "description": "Indonesian Employment Law Database for Vocana AI Assistant",
                "version": "1.0.0",
                "created_date": datetime.datetime.now().isoformat(),
                "total_documents": 0,
                "document_types": "UU,PP,Permenaker,PHI_Decisions,Legal_Analysis",  # String instead of list
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
            }
        )
        
        print("✅ Vocana legal collection created successfully!")
        print(f"   Collection name: {collection.name}")
        print(f"   Collection ID: {collection.id}")
        print(f"   Metadata: {collection.metadata}")
        
        # Verify collection exists
        collections = client.list_collections()
        print(f"\n📂 Available collections: {[c.name for c in collections]}")
        
        print("\n🎯 STATUS: Database ready for content import!")
        return True
        
    except Exception as e:
        if "already exists" in str(e):
            print("⚠️  Collection already exists - using existing collection")
            return True
        else:
            print(f"❌ Error creating collection: {e}")
            return False

if __name__ == "__main__":
    success = create_vocana_collection()
    if success:
        print("\n✅ READY FOR NEXT STEP: Import Notion content")
        print("   Run: python 2_import_notion_content.py")
    else:
        print("\n❌ Setup failed - check error messages above")