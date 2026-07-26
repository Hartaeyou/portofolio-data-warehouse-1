"""
Sama seperti load_to_postgres.py, tapi didesain untuk dijalankan DI DALAM
Docker network (bukan dari host) - supaya tidak lewat port forwarding host
yang bermasalah di beberapa setup Docker Desktop Linux.

Perbedaan: host = "postgres" (nama service di docker-compose.yml),
bukan "localhost"/"127.0.0.1", dan port = 5432 (port internal container,
bukan 5433 yang di-expose ke host).
"""

import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://ikn_user:ikn_pass@postgres:5432/ikn_kaltim"

def main():
    engine = create_engine(DB_URL)

    dim = pd.read_csv("data/processed/dim_kabupaten_kota.csv")
    fact = pd.read_csv("data/processed/fact_regional_indicator.csv")

    dim.to_sql("dim_kabupaten_kota", engine, if_exists="append", index=False)
    print(f"[OK] {len(dim)} baris masuk ke dim_kabupaten_kota")

    fact.to_sql("fact_regional_indicator", engine, if_exists="append", index=False)
    print(f"[OK] {len(fact)} baris masuk ke fact_regional_indicator")

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