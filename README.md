# Dampak IKN terhadap Ekonomi & Migrasi Penduduk Kalimantan Timur

Analisis Business Intelligence untuk menguji apakah pembangunan Ibu Kota Nusantara (IKN) berdampak nyata terhadap pertumbuhan ekonomi dan migrasi penduduk di wilayah sekitarnya, dibandingkan dengan wilayah lain di Kalimantan Timur.

**[🔗 Lihat Dashboard Interaktif]()** &nbsp;|&nbsp; **[📊 LinkedIn Post]()**

---

## Latar Belakang

Sejak IKN diumumkan pada 2019, muncul ekspektasi luas bahwa Kalimantan Timur — khususnya Penajam Paser Utara (PPU) dan Kutai Kartanegara (Kukar) sebagai lokasi kawasan inti — akan mengalami akselerasi pertumbuhan ekonomi dan menjadi tujuan migrasi baru. Project ini menguji hipotesis tersebut secara kuantitatif menggunakan data resmi BPS, membandingkan kondisi **sebelum** (2016–2018) dan **sesudah** (2021–2024) pengumuman IKN.

## Pertanyaan Riset

1. Apakah pertumbuhan penduduk di wilayah IKN Inti benar-benar lebih cepat dibanding wilayah lain?
2. Apakah pertumbuhan ekonomi (PDRB) mengikuti pola yang sama?
3. Apakah dampaknya konsisten di semua indikator, atau ada yang dipengaruhi tren umum (bukan spesifik IKN)?

## Kategorisasi Wilayah

Alih-alih membandingkan 10 kabupaten/kota satu-satu, wilayah dikelompokkan berdasarkan **keterkaitan fungsional** dengan IKN (bukan hanya kedekatan geografis):

| Kategori | Wilayah | Dasar Pertimbangan |
|---|---|---|
| **IKN Inti** | Penajam Paser Utara, Kutai Kartanegara | Lokasi fisik kawasan inti pembangunan IKN |
| **Penyangga** | Balikpapan, Samarinda, Paser | Balikpapan = akses logistik utama (bandara/pelabuhan); Samarinda = pusat pemerintahan provinsi; Paser = berbatasan langsung |
| **Non-IKN** | Kutai Barat, Kutai Timur, Berau, Bontang, Mahakam Ulu | Wilayah dengan keterkaitan fungsional lebih jauh dari aktivitas IKN |

## Sumber Data

Seluruh data bersumber dari **Badan Pusat Statistik Provinsi Kalimantan Timur** ([kaltim.bps.go.id](https://kaltim.bps.go.id)), periode 2015–2024:

| Indikator | Tabel BPS |
|---|---|
| PDRB Per Kapita (ADHB & ADHK) | Menurut Kabupaten/Kota |
| Tingkat Pengangguran Terbuka (TPT) | Menurut Kabupaten/Kota, Sakernas Agustus |
| Tingkat Partisipasi Angkatan Kerja (TPAK) | Menurut Kabupaten/Kota, Sakernas Agustus |
| Jumlah Penduduk & Laju Pertumbuhan | Menurut Kabupaten/Kota |

## Arsitektur & Tech Stack

```
BPS Kaltim (Excel)  →  Python (Pandas)  →  PostgreSQL (Docker)  →  Metabase
     Extract              Transform            Load                Visualize
```

- **ETL**: Python + Pandas + openpyxl — lihat [`etl_pipeline.py`](./etl_pipeline.py)
- **Database**: PostgreSQL 16 (star schema — `fact_regional_indicator` + `dim_kabupaten_kota`), dijalankan via Docker
- **Dashboard**: Metabase, dikoneksikan langsung ke PostgreSQL

## Metodologi

- **PDRB** menggunakan **Atas Dasar Harga Konstan (ADHK)**, bukan Harga Berlaku, untuk menghilangkan efek inflasi — sehingga kenaikan yang terlihat mencerminkan pertumbuhan volume ekonomi riil, bukan sekadar kenaikan harga.
- **Growth rate** (penduduk & PDRB) dihitung ulang secara manual dari angka absolut (`pct_change` per kabupaten/kota per tahun), bukan menggunakan kolom laju pertumbuhan bawaan BPS, karena basis perhitungan resminya berubah-ubah antar periode (lihat bagian Keterbatasan Data).
- **Tahun 2020 dikecualikan** dari perhitungan rata-rata growth rate karena terjadi lonjakan/penurunan tidak wajar di hampir semua kategori wilayah, konsisten dengan pembaruan basis proyeksi Sensus Penduduk 2020 (bukan perubahan riil).
- **Periode "sebelum"** dihitung dari rata-rata 2016–2018 (2015 dikecualikan karena tidak ada data pembanding tahun sebelumnya untuk menghitung growth rate).

## Temuan Utama

**1. Pertumbuhan penduduk IKN Inti melonjak drastis pasca-pengumuman IKN**

| Kategori | Sebelum (2016–2018) | Sesudah (2021–2024) |
|---|---|---|
| IKN Inti | 1,73% | **6,74%** |
| Non-IKN | 1,97% | 1,30% |
| Penyangga | 1,88% | 0,99% |

Sebelum IKN diumumkan, ketiga kategori tumbuh dengan kecepatan serupa. Setelah IKN, IKN Inti melonjak ~4x lipat, sementara dua kategori lain justru sedikit melambat — mengindikasikan kemungkinan pergeseran konsentrasi penduduk ke wilayah IKN Inti.

**2. Pola serupa terlihat pada pertumbuhan ekonomi (PDRB)**

| Kategori | Sebelum | Sesudah |
|---|---|---|
| IKN Inti | -0,85% | **4,43%** |
| Non-IKN | -0,35% | 2,59% |
| Penyangga | 0,67% | 3,74% |

IKN Inti berubah paling drastis, dari pertumbuhan negatif menjadi yang tertinggi di antara ketiga kategori.

**3. Namun, TPAK (partisipasi angkatan kerja) naik merata di semua kategori** — tidak spesifik di IKN Inti. Ini mengindikasikan peningkatan partisipasi kerja lebih dipengaruhi tren ekonomi Kaltim secara umum, bukan efek spesifik IKN — sebuah temuan kontras yang penting agar analisis tidak overclaim bahwa "semua indikator positif disebabkan oleh IKN."

## Keterbatasan & Catatan Data Quality

Ditemukan dan ditangani selama proses ETL:

- **Data 2020 tidak reliable** untuk perhitungan growth rate akibat pembaruan basis Sensus Penduduk 2020 (SP2020) — dikecualikan dari rata-rata.
- **TPT breakdown per kabupaten/kota tidak dipublikasikan BPS untuk 2016** (hanya tersedia di level provinsi) — data kosong dibiarkan sebagai *missing value*, bukan diisi paksa.
- **Kesalahan input di sumber**: jumlah penduduk Samarinda 2021 tercatat 83,1 ribu (seharusnya ~831 ribu) — diperbaiki dengan interpolasi linear dari 2020 & 2022.
- **Urutan kolom TPT/TPAK berbeda antar file** BPS (file 2015–2018 vs 2019–2024) — ETL mendeteksi indikator berdasarkan teks judul tabel, bukan asumsi posisi kolom, untuk menghindari data tertukar.
- Data agregat tingkat kabupaten/kota **tidak dapat memastikan mekanisme migrasi** (migrasi antar-daerah vs tren demografi nasional vs faktor ekonomi lokal lain) — diperlukan data migrasi *origin-destination* untuk konfirmasi lebih lanjut.
- Data realisasi investasi per kabupaten/kota **tidak tersedia secara konsisten** di sumber terbuka manapun yang dicoba (Satu Data Kaltim, DPMPTSP, Sipintar) — variabel investasi tidak dimasukkan ke analisis granular.

## Cara Menjalankan Ulang

```bash
# 1. Jalankan database
docker compose up -d
docker exec -i ikn_kaltim_db psql -U ikn_user -d ikn_kaltim < schema.sql

# 2. Jalankan ETL (baca data mentah di data/raw/, hasil ke data/processed/)
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 etl_pipeline.py

# 3. Load ke database
docker run --rm --network project-ikn-kaltim_default -v "$(pwd)":/app -w /app python:3.10-slim \
  bash -c "pip install pandas sqlalchemy psycopg2-binary --quiet && python load_to_postgres_docker.py"

# 4. Buka Metabase di localhost:3000, hubungkan ke database ikn_kaltim
```

## Struktur Project

```
project-ikn-kaltim/
├── data/
│   ├── raw/              # Data mentah dari BPS (tidak diedit langsung)
│   └── processed/        # Hasil ETL, siap di-load ke database
├── etl_pipeline.py        # Script Extract-Transform-Load
├── schema.sql              # Skema star schema PostgreSQL
├── docker-compose.yml      # Definisi service Postgres + Metabase
└── load_to_postgres_docker.py
```

---

*Dibuat oleh Rayhan Raya Farabi sebagai bagian dari portofolio Business Intelligence. Data bersumber dari BPS Provinsi Kalimantan Timur.*
