"""
### DAG that passes a Delta Lake table through native XCom

This DAG creates a Delta Lake table and passes it through native XCom using
the Airflow 2.8 Delta Lake table serialization.
Learn more about Delta Lake: delta.io
"""


from airflow.decorators import dag, task
from pendulum import datetime
from deltalake.table import DeltaTable
from deltalake import write_deltalake
import pandas as pd
import os
import shutil


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=["deltalake", "2-8", "core"],
)
def deltalake_example():
    @task
    def create_deltalake_table():
        df = pd.DataFrame(
            {"id": [1, 2, 3, 4], "value": ["mercury", "venus", "earth", "mars"]}
        )
        write_deltalake("include/deltalake_table", df)
        deltalake_table = DeltaTable("include/deltalake_table")

        return deltalake_table

    @task
    def print_deltalake_table(deltalake_table):
        df = deltalake_table.to_pandas()
        print(df)

    @task
    def delete_deltalake_table():
        for filename in os.listdir("include/deltalake_table"):
            file_path = os.path.join("include/deltalake_table", filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    (
        print_deltalake_table(deltalake_table=create_deltalake_table())
        >> delete_deltalake_table()
    )


deltalake_example()
