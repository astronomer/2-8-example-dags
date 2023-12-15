"""
## DAG to showcase Airflow pools

This DAG uses a simple pool to limit the number of concurrent tasks.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.models.param import Param
import time

MY_POOL_NAME = "my_garden_pool"


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    params={
        "num_guests": Param(
            23, description="How many people are at your garden party?", type="number"
        )
    },
    doc_md=__doc__,
    tags=["Pools", "2-8", "core"],
)
def pool_example():
    @task
    def count_guests(**context):
        num_guests = context["params"]["num_guests"]
        print(f"There are {num_guests} people at my garden party!")
        print("They all want to jump into the pool!")
        return [i for i in range(num_guests)]

    @task(
        pool=MY_POOL_NAME,
    )
    def jump_into_the_pool(guest):
        print(f"Guest number {guest} is jumping into the pool!")
        print(f"Guest number {guest} is swimming in the pool!")
        swim_time = 10
        time.sleep(swim_time)
        print(
            f"After {swim_time} seconds, guest number {guest} is getting out of the pool!"
        )

    jump_into_the_pool.expand(guest=count_guests())


pool_example()
