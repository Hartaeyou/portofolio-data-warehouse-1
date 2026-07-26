"""
Load Step: masukkan data/processed/*.csv ke PostgreSQL (jalan di Docker)
=========================================================================
Prasyarat:
  1. docker compose up -d          (jalankan container Postgres)
  2. psql -h localhost -U ikn_user -d ikn_kaltim -f schema.sql
     (atau jalankan schema.sql lewat DBeaver/pgAdmin/psql, sekali saja)
  3. pip install sqlalchemy psycopg2-binary pandas --break-system-packages

Jalankan: python3 load_to_postgres.py
"""

import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://ikn_user:ikn_pass@127.0.0.1:5433/ikn_kaltim"

def main():
    engine = create_engine(DB_URL)

    dim = pd.read_csv("data/processed/dim_kabupaten_kota.csv")
    fact = pd.read_csv("data/processed/fact_regional_indicator.csv")

    # dim dulu, karena fact punya foreign key ke dim
    dim.to_sql("dim_kabupaten_kota", engine, if_exists="append", index=False)
    print(f"[OK] {len(dim)} baris masuk ke dim_kabupaten_kota")

    fact_cols = [c for c in fact.columns]  # id auto-generate, tidak perlu disertakan
    fact.to_sql("fact_regional_indicator", engine, if_exists="append", index=False)
    print(f"[OK] {len(fact)} baris masuk ke fact_regional_indicator")

    # Quick sanity check: query balik dari database
    check = pd.read_sql(
        "SELECT kabupaten_kota, tahun, pdrb_adhk_juta_rp, tpt_persen "
        "FROM fact_regional_indicator WHERE kabupaten_kota = 'Penajam Paser Utara' "
        "ORDER BY tahun",
        engine,
    )
    print("\nCek data PPU dari database:")
    print(check.to_string(index=False))


if __name__ == "__main__":
    main()