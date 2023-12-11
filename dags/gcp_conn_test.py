"""
## 
"""

from airflow.decorators import dag, task
from pendulum import datetime

from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator




@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["ObjectStorage"],
    doc_md=__doc__,
)
def gcp():


    f = GCSListObjectsOperator(
        task_id="test",
        bucket="ce-2-8-examples-bucket",
        gcp_conn_id="my_gcs_conn",
    )


gcp()
