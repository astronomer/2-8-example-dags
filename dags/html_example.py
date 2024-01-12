"""
## DAG to showcase using html in the DAG docs and Airflow params

This DAG has a DAG Doc that contains raw HTML, as well as an Airflow param
description containing raw HTML. 

As of Airflow 2.8 rendering raw HTML is turned off by 
default and needs to be enabled in the configuration by setting:

AIRFLOW__WEBSERVER__ALLOW_RAW_HTML_DESCRIPTIONS=True
"""

doc_md_DAG = """
### The Activity DAG showcasing HTML in the DAG docs and Airflow params

<b><span style='color: orange;'>Text</span> <span style='color: red;'>color</span> <span style='color: purple;'>using</span> <span style='color: blue;'>raw</span> <span style='color: green;'>HTML</span><b>

This DAG will help me decide what to do today. It uses the [BoredAPI](https://www.boredapi.com/) to do so.

Before I get to do the activity I will have to:

- Clean up the kitchen.
- Check on my pipelines.
- Water the plants.

Here are some happy plants with a picture formatted using raw HTML:

<img src="https://www.publicdomainpictures.net/pictures/80000/velka/succulent-roses-echeveria.jpg" alt="plants" width="300"/>

This is only possible because AIRFLOW__WEBSERVER__ALLOW_RAW_HTML_DESCRIPTIONS=True is set in the Airflow configuration.
"""

from airflow.decorators import task, dag
from pendulum import datetime
import requests
from airflow.models.param import Param


@dag(
    start_date=None,  # In Airflow 2.8 you don't have to provide a start_date if the schedule is None
    schedule=None,
    catchup=False,
    params={
        "num_participants": Param(
            1,
            description_md="This is a markdown param description containing <span style='color: red;'>raw html</span>.",
            type="number",
        )
    },
    doc_md=doc_md_DAG,
    tags=["HTML DAG Docs", "2-8", "core", "webinar"],
)
def docs_example_dag():
    @task
    def tell_me_what_to_do(**context):
        num_participants = context["params"]["num_participants"]
        response = requests.get(
            f"https://www.boredapi.com/api/activity?participants={num_participants}"
        )
        return response.json()["activity"]

    tell_me_what_to_do()


docs_example_dag()
