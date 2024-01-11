"""
## Example DAG demonstrating the usage of the branching TaskFlow API decorators.

It shows how to use standard Python ``@task.branch`` as well as the external Python
version ``@task.branch_external_python`` which calls an external Python interpreter and
the ``@task.branch_virtualenv`` which builds a temporary Python virtual environment.

`@task.branch_external_python` and `@task.branch_virtualenv` were added in Airflow 2.8.
"""

from __future__ import annotations

import random
import sys
import tempfile

import pendulum

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.edgemodifier import Label
from airflow.utils.trigger_rule import TriggerRule
from airflow.models.param import Param


PATH_TO_PYTHON_BINARY = sys.executable


@dag(
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule="0 0 * * *",
    catchup=False,
    params={
        "my_number": Param(
            23, type="number", description="Hello! Pick a number, any number!"
        ),
    },
    orientation="TB",
    doc_md=__doc__,
    tags=["@task.branch_external_python", "@task.branch_virtualenv", "2-8", "core"],
)
def new_branching_decorators_example():
    run_this_first = EmptyOperator(task_id="run_this_first", pool="my_garden_pool")

    options = ["a", "b", "c", "d"]

    @task.branch()
    def branching(choices: list[str]) -> str:
        return f"branch_{random.choice(choices)}"

    random_choice_instance = branching(choices=options)

    run_this_first >> random_choice_instance

    join = EmptyOperator(
        task_id="join", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    for option in options:

        @task(task_id=f"branch_{option}")
        def some_task():
            print("doing something in Python")

        t = some_task()
        empty = EmptyOperator(task_id=f"follow_{option}")

        # Label is optional here, but it can help identify more complex branches
        random_choice_instance >> Label(option) >> t >> empty >> join

    @task.branch_external_python(python=PATH_TO_PYTHON_BINARY)
    def branching_ext_python(choices) -> str:
        import random

        return f"ext_py_{random.choice(choices)}"

    random_choice_ext_py = branching_ext_python(choices=options)

    join >> random_choice_ext_py

    join_ext_py = EmptyOperator(
        task_id="join_ext_py", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    for option in options:

        @task.external_python(task_id=f"ext_py_{option}", python=PATH_TO_PYTHON_BINARY)
        def some_ext_py_task():
            print("doing something in external Python")

        t = some_ext_py_task()

        # Label is optional here, but it can help identify more complex branches
        random_choice_ext_py >> Label(option) >> t >> join_ext_py

    VENV_CACHE_PATH = tempfile.gettempdir()

    @task.branch_virtualenv(
        requirements=["numpy~=1.24.4"], venv_cache_path=VENV_CACHE_PATH
    )
    def branching_virtualenv(choices) -> str:
        import random

        import numpy as np

        print(f"Some numpy stuff: {np.arange(6)}")
        return f"venv_{random.choice(choices)}"

    random_choice_venv = branching_virtualenv(choices=options)

    join_ext_py >> random_choice_venv

    join_venv = EmptyOperator(
        task_id="join_venv", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    for option in options:

        @task.virtualenv(
            task_id=f"venv_{option}",
            requirements=["numpy~=1.24.4"],
            venv_cache_path=VENV_CACHE_PATH,
        )
        def some_venv_task():
            import numpy as np

            print(f"Some numpy stuff: {np.arange(6)}")

        t = some_venv_task()

        random_choice_venv >> Label(option) >> t >> join_venv


new_branching_decorators_example()
