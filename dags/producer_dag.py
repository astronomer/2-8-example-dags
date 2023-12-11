"""

"""

from airflow import Dataset
from airflow.decorators import dag, task
from pendulum import datetime

MY_DATASET = Dataset("my_dataset")


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["Listeners"],
)
def producer_dag():
    @task(
        outlets=[MY_DATASET],
    )
    def produce_to_a_dataset():
        """Produce a dataset."""
        return "Hello World!"

    produce_to_a_dataset()


producer_dag()
