"""
This file contains the listener hooks that are implemented as an Airflow Plugin.

Learn more about listeners: 
https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/listeners.html#listeners
"""

from airflow.datasets import Dataset
from airflow.listeners import hookimpl
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import TaskInstanceState
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
from sqlalchemy.orm.session import Session
from datetime import datetime

SLACK_CONN_ID = "slack_webhook_conn"


@hookimpl
def on_dataset_changed(dataset: Dataset):
    """Execute if a dataset is updated."""
    print("I am always listening for any Dataset changes and I heard that!")
    print("Posting to Slack...")
    hook = SlackWebhookHook(slack_webhook_conn_id=SLACK_CONN_ID)
    hook.send(text=f"A dataset was changed!")
    print("Done!")
    if dataset.uri == "file://include/bears":
        print("Oh! This is the bears dataset!")
        print("Bears are great :)")
        start_date = datetime.now().date()
        end_date = datetime(2024, 10, 4).date()
        days_until = (end_date - start_date).days
        print(f"Only approximately {days_until} days until fat bear week!")


@hookimpl
def on_task_instance_running(
    previous_state: TaskInstanceState | None,
    task_instance: TaskInstance,
    session: Session | None,
):
    """Execute when task state changes to running."""
    print(
        "I am always listening for any TaskInstance to start running and I heard that!"
    )
