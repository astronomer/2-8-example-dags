"""
### DAG that passes a deltalake table through native XCom

This DAG creates a deltalake table and passes it through native XCom using
the Airflow 2.8 deltalake serialization.
Learn more about deltalake: https://github.com/delta-io/delta-rs
"""


from airflow.decorators import dag, task
from pendulum import datetime
from deltalake.table import DeltaTable
from deltalake import write_deltalake
import pandas as pd


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

    print_deltalake_table(deltalake_table=create_deltalake_table())


deltalake_example()
