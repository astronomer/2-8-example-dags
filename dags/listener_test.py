"""

"""

from airflow import Dataset
from airflow.decorators import dag, task
from airflow.io.path import ObjectStoragePath
from pendulum import datetime
import requests


URI = "file://include/bears"
MY_DATASET = Dataset(URI)


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["Listeners"],
)
def listener_test():
    @task(
        outlets=[MY_DATASET],
    )
    def get_bear():
        print("hi")

    get_bear()



listener_test()
