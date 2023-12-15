"""
### Toy DAG to show the new UI features in the Trigger w/ config view. 

This DAG uses the Param model to define bounds around DAG params.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.models.param import Param


@dag(
    start_date=datetime(2023, 4, 18),
    schedule=None,
    catchup=False,
    params={
        "dog_name": Param("Avery", type="string", maxLength=50),
        "number_of_treats": Param(5, type="integer", minimum=3),
        "dog_is_happy_pre_treats": Param(False, type="boolean"),
    },
    doc_md=__doc__,
    tags=["UI", "2-8", "core"],
)
def trigger_with_params():
    @task
    def give_treats(**context):
        dog = context["params"]["dog_name"]
        num = context["params"]["number_of_treats"]

        print(f"{dog} is getting {num} treats!")

    @task
    def assess_dog_state(**context):
        pre_treats_dog_state = context["params"]["dog_is_happy_pre_treats"]
        dog = context["params"]["dog_name"]
        if pre_treats_dog_state:
            print(f"{dog} even happier now!")
        else:
            print(f"{dog} is happy now!")

    give_treats() >> assess_dog_state()


trigger_with_params()
