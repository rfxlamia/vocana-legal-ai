# vocana_chroma_db_first_test_documentations

```jsx
D:_db>python 3_test_search.py
🚀 VOCANA SEARCH TESTING & VALIDATION
============================================================
1️⃣ COLLECTION OVERVIEW
📊 COLLECTION STATISTICS
——————————
Total documents: 19
Sample metadata fields: [‘section’, ‘created_date’, ‘document_type’, ‘legal_domain’, ‘chunk_index’, ‘chunk_id’, ‘source’, ‘language’]
Document types: {‘legal_compilation’: 5}
Sections found: 1
Sample sections: [‘General’]…
2️⃣ SEMANTIC SEARCH TESTS
🧪 VOCANA SEMANTIC SEARCH TESTING
============================================================
🎯 Running 7 test queries…
🔍 TEST 1/7
🔍 Query: ‘PKWT maksimal berapa tahun?’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.354)
📍 Section: General
📜 Pasal: Pasal 4
💬 Content: Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).
…
📄 Result #2 (Relevance: 0.347)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
📄 Result #3 (Relevance: 0.334)
📍 Section: General
📋 Regulation: P P
💬 Content: memerinci keadaan ketika pekerja tetap berhak atas upah meski tidak bekerja, misalnya sakit, menikah, menjalankan ibadah, menjalankan tugas serikat pekerja, atau melaksanakan hak istirahat.
3. PP …
✅ PASS: Found 3/3 expected topics
============================================================
🔍 TEST 2/7
🔍 Query: ‘uang kompensasi PKWT cara menghitung’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.482)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
📄 Result #2 (Relevance: 0.359)
📍 Section: General
📋 Regulation: P P
💬 Content: PHK hanya dikenal untuk PKWTT; PKWT putus dengan sendirinya ketika jangka waktu berakhir. PP 35/2021 mewajibkan pengusaha memberi kompensasi PHK berupa pesangon, uang penghargaan masa kerja (UPMK)/uan…
📄 Result #3 (Relevance: 0.300)
📍 Section: General
📋 Regulation: P P, U U
💬 Content: PP 35/2021 memperpanjang PKWT berdasarkan jangka waktu menjadi paling lama 5 tahun (berbeda dengan batas 3 tahun dalam UU Ketenagakerjaan).
Uang Kompensasi PKWT
✅ PASS: Found 3/3 expected topics
============================================================
🔍 TEST 3/7
🔍 Query: ‘masa percobaan PKWT boleh tidak?’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.197)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
📄 Result #2 (Relevance: 0.190)
📍 Section: General
📜 Pasal: Pasal 4
💬 Content: Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).
…
📄 Result #3 (Relevance: 0.075)
📍 Section: General
📋 Regulation: P P
💬 Content: memerinci keadaan ketika pekerja tetap berhak atas upah meski tidak bekerja, misalnya sakit, menikah, menjalankan ibadah, menjalankan tugas serikat pekerja, atau melaksanakan hak istirahat.
3. PP …
⚠️ PARTIAL: Query returned results but may need tuning
============================================================
🔍 TEST 4/7
🔍 Query: ‘upah minimum 2025 naik berapa persen?’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.356)
📍 Section: General
💬 Content: ## 5. Peraturan Menteri Ketenagakerjaan No. 16 Tahun 2024
Peraturan ini menetapkan formula kenaikan upah minimum tahun 2025. Regulasi ini menaikkan upah minimum provinsi (UMP) dan kabupaten/kota (UMK…
📄 Result #2 (Relevance: 0.310)
📍 Section: General
📋 Regulation: P P, P P
💬 Content: ## 4. PP No. 36 Tahun 2021 tentang Pengupahan
Definisi Hubungan Kerja dan Upah
PP 36/2021 menegaskan bahwa hubungan kerja adalah hubungan antara pengusaha dan pekerja berdasarkan perjanjian kerja…
📄 Result #3 (Relevance: 0.267)
📍 Section: General
📜 Pasal: Pasal 23, Pasal 39
📋 Regulation: P P
💬 Content: Pasal 23 ayat 3 PP 36/2021 melarang pengusaha membayar upah lebih rendah dari upah minimum.
Upah Lembur
Pasal 39 menegaskan bahwa upah lembur wajib dibayar kepada pekerja yang bekerja melebihi wa…
✅ PASS: Found 2/3 expected topics
============================================================
🔍 TEST 5/7
🔍 Query: ‘pekerja caddy status PKWTT atau PKWT?’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.252)
📍 Section: General
📜 Pasal: Pasal 59, Pasal 61
📋 Regulation: U U
💬 Content: Para penggugat adalah caddy yang mulai bekerja sejak 1987. Mereka mengajukan gugatan karena merasa hubungan kerja diakhiri sepihak dan menuntut status sebagai pekerja tetap, gaji minimum, tunjangan da…
📄 Result #2 (Relevance: 0.225)
📍 Section: General
📜 Pasal: Pasal 4
💬 Content: Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).
…
📄 Result #3 (Relevance: 0.153)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
✅ PASS: Found 2/3 expected topics
============================================================
🔍 TEST 6/7
🔍 Query: ‘upah lembur perhitungan’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.318)
📍 Section: General
📜 Pasal: Pasal 23, Pasal 39
📋 Regulation: P P
💬 Content: Pasal 23 ayat 3 PP 36/2021 melarang pengusaha membayar upah lebih rendah dari upah minimum.
Upah Lembur
Pasal 39 menegaskan bahwa upah lembur wajib dibayar kepada pekerja yang bekerja melebihi wa…
📄 Result #2 (Relevance: -0.013)
📍 Section: General
📋 Regulation: P P, P P
💬 Content: ## 4. PP No. 36 Tahun 2021 tentang Pengupahan
Definisi Hubungan Kerja dan Upah
PP 36/2021 menegaskan bahwa hubungan kerja adalah hubungan antara pengusaha dan pekerja berdasarkan perjanjian kerja…
📄 Result #3 (Relevance: -0.033)
📍 Section: General
📋 Regulation: P P
💬 Content: PHK hanya dikenal untuk PKWTT; PKWT putus dengan sendirinya ketika jangka waktu berakhir. PP 35/2021 mewajibkan pengusaha memberi kompensasi PHK berupa pesangon, uang penghargaan masa kerja (UPMK)/uan…
⚠️ PARTIAL: Query returned results but may need tuning
============================================================
🔍 TEST 7/7
🔍 Query: ‘penyelesaian sengketa bipartit mediasi’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.188)
📍 Section: General
📜 Pasal: Pasal 3
💬 Content: Pasal 3 mewajibkan pihak yang berselisih untuk menyelesaikan perselisihan melalui perundingan bipartit terlebih dahulu selama 30 hari. Bila perundingan gagal, salah satu pihak dapat mendaftarkan perse…
📄 Result #2 (Relevance: 0.147)
📍 Section: General
📜 Pasal: Pasal 4
💬 Content: Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).
…
📄 Result #3 (Relevance: 0.054)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
✅ PASS: Found 1/3 expected topics
============================================================
📊 TEST SUMMARY
Total tests: 7
Passed: 5
Success rate: 71.4%
⚠️ SEARCH FUNCTIONALITY: NEEDS TUNING
🎯 FINAL STATUS
——————–
⚠️ Database needs optimization before production use
📋 Recommended actions:
• Review search results above
• Consider adjusting chunking strategy
• Add more diverse legal content
D:_db>python 3_test_search.py
🚀 VOCANA SEARCH TESTING & VALIDATION
============================================================
1️⃣ COLLECTION OVERVIEW
📊 COLLECTION STATISTICS
——————————
Total documents: 19
Sample metadata fields: [‘document_type’, ‘language’, ‘chunk_id’, ‘source’, ‘section’, ‘legal_domain’, ‘created_date’, ‘chunk_index’]
Document types: {‘legal_compilation’: 5}
Sections found: 1
Sample sections: [‘General’]…
2️⃣ SEMANTIC SEARCH TESTS
🧪 VOCANA SEMANTIC SEARCH TESTING
============================================================
🎯 Running 7 test queries…
🔍 TEST 1/7
🔍 Query: ‘PKWT maksimal berapa tahun?’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.354)
📍 Section: General
📜 Pasal: Pasal 4
💬 Content: Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).
…
📄 Result #2 (Relevance: 0.347)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
📄 Result #3 (Relevance: 0.334)
📍 Section: General
📋 Regulation: P P
💬 Content: memerinci keadaan ketika pekerja tetap berhak atas upah meski tidak bekerja, misalnya sakit, menikah, menjalankan ibadah, menjalankan tugas serikat pekerja, atau melaksanakan hak istirahat.
3. PP …
✅ PASS: Found 3/3 expected topics
============================================================
🔍 TEST 2/7
🔍 Query: ‘uang kompensasi PKWT cara menghitung’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.482)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
📄 Result #2 (Relevance: 0.359)
📍 Section: General
📋 Regulation: P P
💬 Content: PHK hanya dikenal untuk PKWTT; PKWT putus dengan sendirinya ketika jangka waktu berakhir. PP 35/2021 mewajibkan pengusaha memberi kompensasi PHK berupa pesangon, uang penghargaan masa kerja (UPMK)/uan…
📄 Result #3 (Relevance: 0.300)
📍 Section: General
📋 Regulation: P P, U U
💬 Content: PP 35/2021 memperpanjang PKWT berdasarkan jangka waktu menjadi paling lama 5 tahun (berbeda dengan batas 3 tahun dalam UU Ketenagakerjaan).
Uang Kompensasi PKWT
✅ PASS: Found 3/3 expected topics
============================================================
🔍 TEST 3/7
🔍 Query: ‘masa percobaan PKWT boleh tidak?’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.197)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
📄 Result #2 (Relevance: 0.190)
📍 Section: General
📜 Pasal: Pasal 4
💬 Content: Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).
…
📄 Result #3 (Relevance: 0.075)
📍 Section: General
📋 Regulation: P P
💬 Content: memerinci keadaan ketika pekerja tetap berhak atas upah meski tidak bekerja, misalnya sakit, menikah, menjalankan ibadah, menjalankan tugas serikat pekerja, atau melaksanakan hak istirahat.
3. PP …
⚠️ PARTIAL: Query returned results but may need tuning
============================================================
🔍 TEST 4/7
🔍 Query: ‘upah minimum 2025 naik berapa persen?’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.356)
📍 Section: General
💬 Content: ## 5. Peraturan Menteri Ketenagakerjaan No. 16 Tahun 2024
Peraturan ini menetapkan formula kenaikan upah minimum tahun 2025. Regulasi ini menaikkan upah minimum provinsi (UMP) dan kabupaten/kota (UMK…
📄 Result #2 (Relevance: 0.310)
📍 Section: General
📋 Regulation: P P, P P
💬 Content: ## 4. PP No. 36 Tahun 2021 tentang Pengupahan
Definisi Hubungan Kerja dan Upah
PP 36/2021 menegaskan bahwa hubungan kerja adalah hubungan antara pengusaha dan pekerja berdasarkan perjanjian kerja…
📄 Result #3 (Relevance: 0.267)
📍 Section: General
📜 Pasal: Pasal 23, Pasal 39
📋 Regulation: P P
💬 Content: Pasal 23 ayat 3 PP 36/2021 melarang pengusaha membayar upah lebih rendah dari upah minimum.
Upah Lembur
Pasal 39 menegaskan bahwa upah lembur wajib dibayar kepada pekerja yang bekerja melebihi wa…
✅ PASS: Found 2/3 expected topics
============================================================
🔍 TEST 5/7
🔍 Query: ‘pekerja caddy status PKWTT atau PKWT?’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.252)
📍 Section: General
📜 Pasal: Pasal 59, Pasal 61
📋 Regulation: U U
💬 Content: Para penggugat adalah caddy yang mulai bekerja sejak 1987. Mereka mengajukan gugatan karena merasa hubungan kerja diakhiri sepihak dan menuntut status sebagai pekerja tetap, gaji minimum, tunjangan da…
📄 Result #2 (Relevance: 0.225)
📍 Section: General
📜 Pasal: Pasal 4
💬 Content: Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).
…
📄 Result #3 (Relevance: 0.153)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
✅ PASS: Found 2/3 expected topics
============================================================
🔍 TEST 6/7
🔍 Query: ‘upah lembur perhitungan’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.318)
📍 Section: General
📜 Pasal: Pasal 23, Pasal 39
📋 Regulation: P P
💬 Content: Pasal 23 ayat 3 PP 36/2021 melarang pengusaha membayar upah lebih rendah dari upah minimum.
Upah Lembur
Pasal 39 menegaskan bahwa upah lembur wajib dibayar kepada pekerja yang bekerja melebihi wa…
📄 Result #2 (Relevance: -0.013)
📍 Section: General
📋 Regulation: P P, P P
💬 Content: ## 4. PP No. 36 Tahun 2021 tentang Pengupahan
Definisi Hubungan Kerja dan Upah
PP 36/2021 menegaskan bahwa hubungan kerja adalah hubungan antara pengusaha dan pekerja berdasarkan perjanjian kerja…
📄 Result #3 (Relevance: -0.033)
📍 Section: General
📋 Regulation: P P
💬 Content: PHK hanya dikenal untuk PKWTT; PKWT putus dengan sendirinya ketika jangka waktu berakhir. PP 35/2021 mewajibkan pengusaha memberi kompensasi PHK berupa pesangon, uang penghargaan masa kerja (UPMK)/uan…
⚠️ PARTIAL: Query returned results but may need tuning
============================================================
🔍 TEST 7/7
🔍 Query: ‘penyelesaian sengketa bipartit mediasi’
📊 Found: 3 relevant documents
————————————————–
📄 Result #1 (Relevance: 0.188)
📍 Section: General
📜 Pasal: Pasal 3
💬 Content: Pasal 3 mewajibkan pihak yang berselisih untuk menyelesaikan perselisihan melalui perundingan bipartit terlebih dahulu selama 30 hari. Bila perundingan gagal, salah satu pihak dapat mendaftarkan perse…
📄 Result #2 (Relevance: 0.147)
📍 Section: General
📜 Pasal: Pasal 4
💬 Content: Pasal 4 menetapkan bahwa setelah bipartit gagal, para pihak dapat memilih konsiliasi atau arbitrase (untuk perselisihan kepentingan) atau mediasi (apabila tidak memilih atau untuk perselisihan hak).
…
📄 Result #3 (Relevance: 0.054)
📍 Section: General
📋 Regulation: P P
💬 Content: PP 35/2021 memperkenalkan uang kompensasi bagi pekerja PKWT. Pengusaha wajib membayar kompensasi pada akhir kontrak (masa kerja minimal 1 bulan). Rumus: masa kerja/12 × upah sebulan.
PHK dan Pesa…
✅ PASS: Found 1/3 expected topics
============================================================
📊 TEST SUMMARY
Total tests: 7
Passed: 5
Success rate: 71.4%
⚠️ SEARCH FUNCTIONALITY: NEEDS TUNING
🎯 FINAL STATUS
——————–
⚠️ Database needs optimization before production use
📋 Recommended actions:
• Review search results above
• Consider adjusting chunking strategy
• Add more diverse legal content
```