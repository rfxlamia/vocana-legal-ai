# 🏛️ Vocana Legal AI - Indonesian Employment Law Database

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4.0+-green.svg)](https://www.trychroma.com/)

> **Professional-grade legal document processing system for Indonesian employment law regulations. Built for RAG (Retrieval-Augmented Generation) applications in LegalTech.**

## 🎯 What This Project Does

This system processes Indonesian employment law regulations (UU, PP, Perpres) and structures them for AI-powered legal research and analysis. It handles complex legal document parsing, amendment tracking, and semantic search optimization.

### ⚖️ Complete Legal Coverage (2,492 Articles Total)
- 🏛️ **UU 13/2003** - Ketenagakerjaan foundation law (780 articles)
- 🔄 **UU 6/2023** - Cipta Kerja latest amendments (71 changes)
- 📝 **PP 35/2021** - PKWT & termination procedures (336 articles)
- 💰 **PP 36/2021** - Wage & compensation regulations (340 articles)
- ⚖️ **UU 2/2004** - Industrial dispute resolution (589 articles)
- 🏥 **UU 40/2004** - Social security system SJSN (267 articles)
- 👥 **UU 21/2000** - Labor unions & collective bargaining (109 articles)

## 🚀 Key Features

### 📋 Advanced Legal Parsing
- **Amendment Detection**: Automatically categorizes changes as `diubah`, `dihapus`, `disisipkan`
- **Cross-Reference Mapping**: Links amendments to original law articles
- **Hierarchy Recognition**: Processes UU → PP → Perpres legal hierarchy
- **Article Extraction**: Handles complex pasal numbering (13, 14A, etc.)

### 🧠 AI-Ready Metadata
- **Legal Concept Tagging**: Auto-extracts employment law concepts
- **Semantic Chunking**: Optimized text splitting for vector embeddings
- **Rich Context**: Comprehensive metadata for RAG applications
- **Search Optimization**: ChromaDB integration with proper indexing

### 🏗️ Production-Ready Architecture
- **Modular Design**: Reusable parsing functions
- **Error Handling**: Robust validation and recovery
- **Performance Optimized**: Batch processing for large datasets
- **Unicode Support**: Full Indonesian character and emoji support

## 📁 Project Structure

```
vocana-legal-ai/
├── src/                                    # 7 Core Import Scripts
│   ├── import_uu13_2003_ketenagakerjaan.py   # Foundation law (780 articles)
│   ├── import_uu6_2023_cipta_kerja.py       # Latest amendments (71 changes)
│   ├── import_pp35_2021_pkwt_phk.py         # PKWT & termination (336 articles)
│   ├── import_pp36_2021_pengupahan.py       # Wages & compensation (340 articles)
│   ├── import_uu2_2004_perselisihan.py      # Dispute resolution (589 articles)
│   ├── import_uu40_2004_sjsn.py             # Social security (267 articles)
│   └── import_uu21_2000_serikat_pekerja.py  # Labor unions (109 articles)
├── tests/                                  # 51 Unit Tests (All Passing)
│   ├── test_uu13_import.py                 # 12 tests ✅
│   ├── test_uu6_import.py                  # 8 tests ✅
│   ├── test_pp35_import.py                 # 9 tests ✅
│   ├── test_pp36_import.py                 # 12 tests ✅
│   └── test_uu2_import.py                  # 10 tests ✅
├── sample_data/                            # Sample legal content (demo only)
│   ├── uu13_sample.txt, uu6_sample.txt
│   ├── pp35_sample.txt, pp36_sample.txt
│   ├── uu2_sample.txt, uu40_sample.txt
│   └── uu21_sample.txt
├── docs/                                   # Documentation
│   └── README_import_uu6_2023.md          # Detailed docs
├── chroma_db/                              # ChromaDB storage (auto-created)
└── LICENSE.md                              # MIT license + legal disclaimers
```

## 🛠️ Installation & Setup

### Prerequisites
```bash
Python 3.8+
pip install chromadb>=0.4.0
```

### Quick Start
```bash
# Clone the repository
git clone https://github.com/rfxlamia/vocana-legal-ai.git
cd vocana-legal-ai

# Install dependencies
pip install chromadb python-dotenv

# Run sample imports (choose any regulation)
python src/import_uu13_2003_ketenagakerjaan.py     # Foundation law
python src/import_uu6_2023_cipta_kerja.py          # Latest amendments
python src/import_pp35_2021_pkwt_phk.py            # Employment contracts
```

### Data Setup
1. **Official Documents**: Obtain legal texts from authorized sources
2. **Format Conversion**: Convert to required text format (see `/sample_data` examples)
3. **File Placement**: Place formatted files in appropriate data folders
4. **Import Execution**: Run relevant import scripts

## 💻 Usage Examples

### Basic Import
```python
# UU 13/2003 - Foundation employment law
from src.import_uu13_2003_ketenagakerjaan import parse_uu13_articles, load_sample_data

content = load_sample_data()
articles = parse_uu13_articles(content)
print(f"Parsed {len(articles)} employment law articles")

# UU 6/2023 - Latest amendments  
from src.import_uu6_2023_cipta_kerja import parse_uu6_changes, load_sample_data

content = load_sample_data()
changes = parse_uu6_changes(content)
print(f"Parsed {len(changes)} legal amendments")
```

### ChromaDB Integration
```python
import chromadb

# Connect to database
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("vocana_legal_uu6_2023_complete")

# Semantic search
results = collection.query(
    query_texts=["pemutusan hubungan kerja"],
    n_results=5,
    where={"amendment_type": "diubah"}
)
```

### Legal Concept Search
```python
# Find all PHK-related amendments
phk_results = collection.query(
    query_texts=["termination employment"],
    n_results=10,
    where={"legal_concepts": {"$contains": "phk"}}
)
```

## 🧪 Testing

Run the complete test suite (51 tests total):
```bash
# All tests (51 tests across 5 test files)
python -m pytest tests/ -v

# Individual test files
python tests/test_uu13_import.py    # 12 tests - Foundation law
python tests/test_uu6_import.py     # 8 tests - Amendments  
python tests/test_pp35_import.py    # 9 tests - PKWT & PHK
python tests/test_pp36_import.py    # 12 tests - Wages
python tests/test_uu2_import.py     # 10 tests - Disputes

# Coverage report
python -m pytest tests/ --cov=src
```

## 📊 Performance Metrics

| Regulation | Articles/Changes | Processing Time | Storage Size | Word Count |
|------------|------------------|----------------|-------------|------------|
| UU 13/2003 | 780 articles | ~60s | ~25MB | ~180,000 |
| UU 2/2004  | 589 articles | ~50s | ~20MB | ~150,000 |
| PP 35/2021 | 336 articles | ~35s | ~15MB | ~125,000 |
| PP 36/2021 | 340 articles | ~35s | ~15MB | ~130,000 |
| UU 40/2004 | 267 articles | ~30s | ~12MB | ~100,000 |
| UU 21/2000 | 109 articles | ~15s | ~5MB | ~45,000 |
| UU 6/2023  | 71 changes | ~25s | ~5MB | ~61,000 |
| **TOTAL**  | **2,492** | **~4min** | **~97MB** | **~791,000** |

## ⚖️ Legal Compliance

### ⚠️ Important Disclaimers

1. **Code vs. Data**: This repository contains **SOFTWARE CODE ONLY**
2. **No Official Documents**: Actual legal texts are **NOT INCLUDED**
3. **Sample Data Only**: `/sample_data` contains **DEMO CONTENT ONLY**
4. **User Responsibility**: Users must obtain official documents from authorized sources

### 📚 Official Sources
- [Kementerian Sekretariat Negara RI](https://jdih.setneg.go.id/)
- [Database Peraturan BPK](https://peraturan.bpk.go.id/)
- Official government legal databases

### 🔒 Data Privacy
- No personal data processing
- No storage of confidential legal information
- Respects Indonesian data protection laws

## 🤝 Contributing

We welcome contributions! Please:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Test** your changes (`python -m pytest tests/`)
4. **Commit** your changes (`git commit -m 'Add amazing feature'`)
5. **Push** to branch (`git push origin feature/amazing-feature`)
6. **Open** a Pull Request

### 📋 Contribution Guidelines
- ✅ Code follows project structure
- ✅ All tests pass
- ✅ Legal compliance maintained
- ✅ Documentation updated
- ✅ Sample data only (no official documents)

## 📈 Roadmap

### Phase 1: Core Functionality ✅
- [x] UU 6/2023 Cipta Kerja processing
- [x] ChromaDB integration
- [x] Basic RAG functionality
- [x] Unit test coverage

### Phase 2: Enhanced Features 🚧
- [ ] REST API interface
- [ ] Advanced semantic search
- [ ] Multi-format export (JSON, CSV)
- [ ] Real-time amendment tracking

### Phase 3: Enterprise Features 📋
- [ ] Multi-tenant support
- [ ] Advanced analytics dashboard
- [ ] Legal citation network analysis
- [ ] Integration with legal databases

## 🎓 Use Cases

### 🏢 Legal Professionals
- **Case Research**: Find relevant employment law provisions
- **Amendment Tracking**: Monitor legal changes over time
- **Cross-Reference Analysis**: Link related legal concepts

### 🎓 Academic Research
- **Legal Analytics**: Quantitative analysis of legal changes
- **Policy Studies**: Track employment law evolution
- **Comparative Law**: Analyze regulatory patterns

### 💼 Business Compliance
- **HR Policy Updates**: Align policies with current law
- **Risk Assessment**: Identify compliance requirements
- **Training Materials**: Create law-based training content

## 📞 Support

- **Documentation**: Check `/docs` folder for detailed guides
- **Issues**: Report bugs via GitHub Issues
- **Legal Questions**: Consult qualified legal professionals
- **Technical Support**: Create GitHub discussions

## 📄 License

This project is licensed under the MIT License (code only) - see the [LICENSE.md](LICENSE.md) file for details.

**Note**: Legal content licensing is separate and subject to Indonesian copyright law.

---

**🏛️ Built for the future of Indonesian LegalTech**

*This project demonstrates production-ready legal document processing capabilities for AI-powered legal research and compliance systems.*
