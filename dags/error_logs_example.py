"""

"""

from airflow import Dataset
from airflow.decorators import dag, task
from pendulum import datetime

URI = "dataset_to_cause_listener_error"
MY_DATASET = Dataset(URI)


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["Error Logs", "2-8"],
)
def error_logs_example():
    @task(
        outlets=[MY_DATASET],
    )
    def update_table():
        print("Hello, world!")

    update_table()


error_logs_example()
