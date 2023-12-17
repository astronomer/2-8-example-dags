"""
### DAG to show the literal wrapper

This DAG shows how to use the literal wrapper to ignore jinja templating.
"""

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from pendulum import datetime
from airflow.models.param import Param
from airflow.utils.template import literal


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    params={
        "the_best_number": Param(
            231942, description="Enter your favorite number", type="number"
        )
    },
    doc_md=__doc__,
    tags=["literal", "2-8", "core"],
)
def literal_wrapper_example():
    BashOperator(
        task_id="echo_a_jinja_template",
        bash_command="echo {{ params.the_best_number }}",
    )

    BashOperator(
        task_id="use_literal_wrapper_to_ignore_jinja_template",
        bash_command=literal("echo {{ params.the_best_number }}"),
    )


literal_wrapper_example()
