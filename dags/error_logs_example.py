"""
## Cause an OOM ERROR and Zombie in the scheduler to showcase error log forwarding

CAVE: This DAG will cause an OOM error in the task causing the scheduler to kill it as a zombie. 
It is only meant to showcase error log forwarding with the `task_context_logger`. 
Run this DAG at your own risk!
Currently forwarded errors are: zombie, externally killed and task stuck in the Celery queue.
"""

from airflow.decorators import dag, task
import numpy as np


@dag(
    start_date=None,  # In Airflow 2.8 you don't have to provide a start_date if the schedule is None
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=["Error Logs", "2-8", "core", "webinar"],
)
def error_logs_example():
    @task
    def memory_intensive_task():
        big_array = []
        while True:
            big_array.append(np.zeros((1000, 1000)))

    memory_intensive_task()


error_logs_example()
