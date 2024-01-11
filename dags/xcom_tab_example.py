"""
### Query the Fruityvice API for information about a fruit

This DAG queries the [Fruityvice API](https://www.fruityvice.com/) for 
information about a fruit. It pushes the information to XCom.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.models.param import Param
import requests


@dag(
    start_date=None,
    schedule=None,
    catchup=False,
    params={
        "my_fruit": Param(
            "strawberry", description="The fruit to get info about.", type="string"
        )
    },
    doc_md=__doc__,
    tags=["XCom tab", "2-8", "core", "webinar"],
)
def xcom_tab_example():
    @task
    def get_fruit_info(**context):
        my_fruit = context["params"]["my_fruit"]

        r = requests.get(f"https://www.fruityvice.com/api/fruit/{my_fruit}").json()

        for k, v in r.items():
            context["ti"].xcom_push(key=k, value=v)

        return r

    get_fruit_info()


xcom_tab_example()
