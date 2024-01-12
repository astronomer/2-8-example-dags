"""
## Example DAG demonstrating the @task.branch_virtualenv decorator

This DAG shows how to use the @task.branch_virtualenv decorator to create a temporary
Python virtual environment and run a task in it which decides what path to take.
"""

from __future__ import annotations
import random
import pendulum
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.models.baseoperator import chain


@dag(
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule="0 0 * * *",
    catchup=False,
    doc_md=__doc__,
    tags=[
        "@task.branch_external_python",
        "@task.branch_virtualenv",
        "2-8",
        "core",
        "webinar",
    ],
)
def simple_venv_branching_example():
    start = EmptyOperator(task_id="start")

    @task.branch
    def decide_on_base_food() -> str:
        choices = ["rice", "noodles", "potatoes"]
        my_base_food = random.choice(choices)
        return f"buy_{my_base_food}"

    @task
    def buy_rice():
        print("Buying rice")

    @task
    def buy_noodles():
        print("Buying noodles")

    @task
    def buy_potatoes():
        print("Buying potatoes")

    start_cooking = EmptyOperator(
        task_id="start_cooking", trigger_rule="none_failed_min_one_success"
    )

    @task.branch_virtualenv(requirements=["numpy==1.24.4"])
    def decide_on_vegetable() -> str:
        import numpy as np

        choices = ["spinach", "broccoli", "tomatoes"]
        my_vegetable = np.random.choice(choices, 1)

        return f"buy_{my_vegetable[0]}"

    @task
    def buy_tomatoes():
        print("Buying tomatoes")

    @task
    def buy_broccoli():
        print("Buying broccoli")

    @task
    def buy_spinach():
        print("Buying spinach")

    end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")

    chain(
        start,
        decide_on_base_food(),
        [buy_noodles(), buy_rice(), buy_potatoes()],
        start_cooking,
        decide_on_vegetable(),
        [buy_tomatoes(), buy_broccoli(), buy_spinach()],
        end,
    )


simple_venv_branching_example()
