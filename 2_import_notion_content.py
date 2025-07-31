"""
VOCANA DATABASE SETUP - Step 2: Import Notion Legal Content
Import existing legal content dari Notion ke ChromaDB dengan proper chunking dan embeddings
"""

import chromadb
import re
from typing import List, Dict, Any
import hashlib

class VocanaContentImporter:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./vocana_chroma_db")
        self.collection = self.client.get_collection("vocana_legal_corpus")
        
    def chunk_legal_text(self, text: str, chunk_size: int = 300) -> List[Dict[str, Any]]:
        """
        Chunk legal text dengan mempertahankan struktur legal (pasal, ayat, etc)
        """
        chunks = []
        
        # Split berdasarkan struktur legal documents
        sections = re.split(r'(\n#{1,3}\s+.*?\n|\nPasal \d+|\nAyat \(\d+\))', text)
        
        current_chunk = ""
        current_metadata = {
            "section": "General",
            "document_part": "Unknown"
        }
        
        for section in sections:
            if not section.strip():
                continue
                
            # Detect legal structure markers
            if re.match(r'^#{1,3}\s+', section):
                current_metadata["section"] = section.strip()
            elif re.match(r'^Pasal \d+', section):
                current_metadata["pasal"] = section.strip()
            elif re.match(r'^Ayat \(\d+\)', section):
                current_metadata["ayat"] = section.strip()
            
            # Add to current chunk
            if len(current_chunk + section) > chunk_size:
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "metadata": current_metadata.copy(),
                        "chunk_id": hashlib.md5(current_chunk.encode()).hexdigest()[:8]
                    })
                current_chunk = section
            else:
                current_chunk += section
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": current_metadata.copy(),
                "chunk_id": hashlib.md5(current_chunk.encode()).hexdigest()[:8]
            })
        
        return chunks
    
    def import_legal_content(self):
        """
        Import comprehensive legal content dari Notion document
        """
        print("📂 Importing Vocana Legal Content...")
        print("=" * 50)
        
        # Legal content dari Notion document yang sudah comprehensive
        legal_content = """
## 1. Undang-Undang No. 2 Tahun 2004 tentang Penyelesaian Perselisihan Hubungan Industrial (PPHI)

Peraturan ini menjadi dasar pembentukan Pengadilan Hubungan Industrial (PHI) dan prosedur penyelesaian sengketa.

### Jenis Perselisihan
Pasal 2 mengelompokkan perselisihan hubungan industrial menjadi:
1) perselisihan hak
2) perselisihan kepentingan  
3) perselisihan PHK
4) perselisihan antara serikat pekerja/serikat buruh

### Kewajiban Bipartit
Pasal 3 mewajibkan pihak yang berselisih untuk menyelesaikan perselisihan melalui perundingan bipartit terlebih dahulu selama 30 hari. Bila perundingan gagal, salah satu pihak dapat mendaftarkan perselisihan ke dinas ketenagakerjaan.

### Pilihan Penyelesaian Selanjutnya
Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).

## 2. Undang-Undang No. 13 Tahun 2003 tentang Ketenagakerjaan

### PKWT vs PKWTT
Pasal 56 menyatakan bahwa perjanjian kerja dapat dibuat untuk waktu tertentu (PKWT) atau waktu tidak tertentu (PKWTT).

#### Ketentuan PKWT:
- Harus dibuat tertulis dan berbahasa Indonesia (Pasal 57)
- Tidak boleh mensyaratkan masa percobaan (Pasal 58)
- Hanya boleh untuk pekerjaan yang sekali selesai/bersifat musiman/ditaksir selesai dalam waktu tertentu
- Tidak boleh untuk pekerjaan bersifat tetap (Pasal 59 ayat 1-2)
- Durasi PKWT: paling lama 2 tahun dan dapat diperpanjang sekali untuk 1 tahun
- Pembaruan hanya boleh dilakukan setelah jeda 30 hari dan paling lama 2 tahun

#### Ketentuan PKWTT:
- Boleh mensyaratkan masa percobaan maksimal 3 bulan (Pasal 60)
- Perjanjian lisan harus diikuti surat pengangkatan berisi identitas pekerja, tanggal mulai, jenis pekerjaan dan besarnya upah

### Berakhirnya Hubungan Kerja
Pasal 61 menyatakan bahwa perjanjian kerja berakhir bila:
- pekerja meninggal dunia
- jangka waktu PKWT berakhir
- ada putusan pengadilan/lembaga penyelesaian perselisihan yang berkekuatan tetap
- keadaan tertentu dalam perjanjian kerja/peraturan perusahaan

### Ketentuan Pengupahan
Pasal 88 ayat 1-2 menetapkan setiap pekerja berhak memperoleh penghasilan yang memenuhi penghidupan layak.

#### Upah Minimum
Pasal 88 ayat 4-Pasal 89 mengatur bahwa pemerintah menetapkan upah minimum berdasarkan kebutuhan hidup layak, produktivitas dan pertumbuhan ekonomi. Pengusaha dilarang membayar di bawah upah minimum (Pasal 90).

#### Upah Selama Tidak Bekerja  
Pasal 93 memerinci keadaan ketika pekerja tetap berhak atas upah meski tidak bekerja, misalnya sakit, menikah, menjalankan ibadah, menjalankan tugas serikat pekerja, atau melaksanakan hak istirahat.

## 3. PP No. 35 Tahun 2021 tentang PKWT, Alih Daya, Waktu Kerja dan PHK

### Durasi PKWT Diperpanjang
PP 35/2021 memperpanjang PKWT berdasarkan jangka waktu menjadi paling lama 5 tahun (berbeda dengan batas 3 tahun dalam UU Ketenagakerjaan).

### Uang Kompensasi PKWT
PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.

### PHK dan Pesangon
PHK hanya dikenal untuk PKWTT; PKWT putus dengan sendirinya ketika jangka waktu berakhir. PP 35/2021 mewajibkan pengusaha memberi kompensasi PHK berupa pesangon, uang penghargaan masa kerja (UPMK)/uang pisah, dan penggantian hak.

### Waktu Kerja dan Upah Lembur
Pasal 21 ayat 2 PP 35/2021 menyatakan waktu kerja seminggu 40 jam (8 jam × 5 hari atau 7 jam × 6 hari). Pasal 31 mewajibkan pengusaha yang mempekerjakan pekerja melebihi waktu kerja membayar upah lembur: 1,5× upah sejam untuk jam pertama dan 2× upah sejam untuk jam berikutnya.

## 4. PP No. 36 Tahun 2021 tentang Pengupahan

### Definisi Hubungan Kerja dan Upah
PP 36/2021 menegaskan bahwa hubungan kerja adalah hubungan antara pengusaha dan pekerja berdasarkan perjanjian kerja yang mempunyai unsur pekerjaan, upah dan perintah.

### Larangan Membayar di Bawah Upah Minimum
Pasal 23 ayat 3 PP 36/2021 melarang pengusaha membayar upah lebih rendah dari upah minimum.

### Upah Lembur
Pasal 39 menegaskan bahwa upah lembur wajib dibayar kepada pekerja yang bekerja melebihi waktu kerja, pada waktu istirahat mingguan atau hari libur.

## 5. Peraturan Menteri Ketenagakerjaan No. 16 Tahun 2024

Peraturan ini menetapkan formula kenaikan upah minimum tahun 2025. Regulasi ini menaikkan upah minimum provinsi (UMP) dan kabupaten/kota (UMK) sebesar 6,5% dari upah minimum 2024.

## 6. Putusan Pengadilan Hubungan Industrial (PHI)

### Kasus Nomor 38/Pdt.Sus-PHI/2024/PN Semarang
Para penggugat adalah caddy yang mulai bekerja sejak 1987. Mereka mengajukan gugatan karena merasa hubungan kerja diakhiri sepihak dan menuntut status sebagai pekerja tetap, gaji minimum, tunjangan dan pesangon.

PHI memeriksa bukti adanya hubungan kerja (unsur pekerjaan, upah, perintah). Kasus ini mempertegas penerapan Pasal 59 dan Pasal 61 UU Ketenagakerjaan—pekerja yang bekerja lama tanpa perjanjian tertulis tidak bisa dianggap PKWT; hubungan kerja beralih menjadi PKWTT.

### Kasus Nomor 56/Pdt.Sus-PHI/2024/PN Semarang  
Para penggugat telah bekerja sebagai caddy sejak 1980 dan 1985 tanpa henti. PHI menilai apakah pengalihan perusahaan menyebabkan berakhirnya perjanjian kerja atau hak pekerja tetap dipertahankan.
"""

        # Process content menjadi chunks
        chunks = self.chunk_legal_text(legal_content)
        
        print(f"📋 Processing {len(chunks)} legal content chunks...")
        
        # Prepare data untuk ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk["text"])
            
            # Enhanced metadata dengan legal-specific information
            metadata = {
                "document_type": "legal_compilation",
                "source": "notion_legal_framework",
                "chunk_index": i,
                "chunk_id": chunk["chunk_id"],
                "section": chunk["metadata"].get("section", "General"),
                "created_date": "2025-07-29",
                "language": "indonesian",
                "legal_domain": "employment_law"
            }
            
            # Add specific legal references if detected
            text = chunk["text"]
            if "Pasal" in text:
                pasal_matches = re.findall(r'Pasal \d+', text)
                if pasal_matches:
                    metadata["pasal_references"] = ", ".join(pasal_matches)
            
            if "UU" in text or "PP" in text or "Permenaker" in text:
                regulation_matches = re.findall(r'(UU|PP|Permenaker)\s+[\w\/\d\-]+', text)
                if regulation_matches:
                    metadata["regulation_references"] = ", ".join([match[0] + " " + match[1] for match in regulation_matches])
            
            metadatas.append(metadata)
            ids.append(f"legal_chunk_{i:04d}")
        
        # Add ke ChromaDB collection
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Successfully imported {len(documents)} legal chunks")
            
            # Verify import
            collection_count = self.collection.count()
            print(f"📊 Total documents in collection: {collection_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error importing content: {e}")
            return False

def main():
    print("🚀 VOCANA LEGAL CONTENT IMPORT")
    print("=" * 60)
    
    try:
        importer = VocanaContentImporter()
        success = importer.import_legal_content()
        
        if success:
            print("\n✅ CONTENT IMPORT COMPLETED!")
            print("🎯 STATUS: Ready for semantic search testing")
            print("   Run: python 3_test_search.py")
        else:
            print("\n❌ Import failed - check error messages above")
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("   Make sure to run: python 1_create_collection.py first")

if __name__ == "__main__":
    main()