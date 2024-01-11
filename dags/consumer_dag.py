"""
## Helper DAG

This DAG runs on updates to the `include/bears` dataset and prints a message to the logs.
"""

from airflow.datasets import Dataset
from airflow.decorators import dag, task
from pendulum import datetime
import time

URI = "file://include/bears"
MY_DATASET = Dataset(URI)


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=[MY_DATASET],
    catchup=False,
    doc_md=__doc__,
    tags=["helper", "2-8", "core", "webinar"],
)
def consumer_dag():
    @task
    def celebrate_bears():
        time.sleep(20)
        print("Yay Bears!!")

    celebrate_bears()


consumer_dag()
