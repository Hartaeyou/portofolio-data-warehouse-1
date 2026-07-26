-- Star Schema: Dampak IKN terhadap Ekonomi & Migrasi Penduduk Kaltim

DROP TABLE IF EXISTS fact_regional_indicator;
DROP TABLE IF EXISTS dim_kabupaten_kota;

CREATE TABLE dim_kabupaten_kota (
    kabupaten_kota      VARCHAR(50) PRIMARY KEY,
    kategori_wilayah    VARCHAR(20) NOT NULL  -- 'IKN Inti' | 'Penyangga' | 'Non-IKN'
);

CREATE TABLE fact_regional_indicator (
    id                          SERIAL PRIMARY KEY,
    kabupaten_kota              VARCHAR(50) REFERENCES dim_kabupaten_kota(kabupaten_kota),
    tahun                       INT NOT NULL,
    pdrb_adhb_juta_rp           NUMERIC(12, 2),
    pdrb_adhk_juta_rp           NUMERIC(12, 2),
    tpak_persen                 NUMERIC(5, 2),
    tpt_persen                  NUMERIC(5, 2),
    jumlah_penduduk_ribu        NUMERIC(10, 1),
    kepadatan_penduduk_km2      NUMERIC(10, 1),
    rasio_jenis_kelamin         NUMERIC(6, 2),
    laju_pertumbuhan_persen     NUMERIC(6, 2),
    pdrb_growth_persen          NUMERIC(6, 2),
    kategori_wilayah            VARCHAR(20),
    periode_ikn                 VARCHAR(20),
    UNIQUE (kabupaten_kota, tahun)
);

CREATE INDEX idx_fact_tahun ON fact_regional_indicator(tahun);
CREATE INDEX idx_fact_kabkota ON fact_regional_indicator(kabupaten_kota);