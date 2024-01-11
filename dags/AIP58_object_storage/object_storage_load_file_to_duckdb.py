"""
## Use Object Storage to read a parquet file and ingest it into a duckdb database

This DAG create and reads a local parquet file from remote object storage using 
the Airflow 2.8 Object Storage feature.
"""

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.io.path import ObjectStoragePath
from pendulum import datetime
import pandas as pd
import duckdb

base_path = ObjectStoragePath("file://include/")


@dag(
    start_date=datetime(2023, 12, 1),
    schedule="0 0 * * *",
    catchup=False,
    doc_md=__doc__,
    tags=["ObjectStorage", "2-8", "core"],
)
def object_storage_load_file_to_duckdb():
    @task
    def create_parquet_file(base):
        """Create a table about ducks and save it as a parquet file."""
        data = {
            "name": ["Mallard", "Pekin", "Muscovy", "Rouen", "Indian Runner"],
            "country_of_origin": [
                "North America",
                "China",
                "South America",
                "France",
                "India",
            ],
            "job": [
                "Friend",
                "Friend, Eggs",
                "Friend, Pest Control",
                "Friend, Show",
                "Eggs, Friend",
            ],
            "num": [3, 5, 6, 2, 3],
            "num_quacks_per_hour": [10, 20, 25, 5, 44],
        }

        df = pd.DataFrame(data)
        df_parquet = df.to_parquet()

        file = base / "duck_info.parquet"
        file.touch()
        file.write_bytes(df_parquet)

    @task
    def ingest_to_duckdb(base):
        "Ingest the parquet file into a duckdb database."
        conn = duckdb.connect(database="include/duckdb.db")
        file = base / "duck_info.parquet"
        conn.register_filesystem(file.fs)
        conn.execute(
            f"CREATE OR REPLACE TABLE ducks_table AS SELECT * FROM read_parquet('{file}')"
        )
        conn.close()

    @task
    def read_from_duckdb():
        """Read and return the duckdb table."""
        conn = duckdb.connect(database="include/duckdb.db")
        ducks_info = conn.execute(
            f"SELECT * FROM ducks_table WHERE num_quacks_per_hour > 15"
        ).fetchdf()
        print(ducks_info)

    chain(
        create_parquet_file(base=base_path),
        ingest_to_duckdb(base=base_path),
        read_from_duckdb(),
    )


object_storage_load_file_to_duckdb()
