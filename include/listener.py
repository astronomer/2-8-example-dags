from airflow import Dataset
from airflow.listeners import hookimpl
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook


@hookimpl
def on_dataset_changed(dataset: Dataset):
    """Execute when dataset change is registered."""
    print("I am always listening for any Dataset changes and I heard that!")
    print("Posting to Slack...")
    hook = SlackWebhookHook(slack_webhook_conn_id="slack_webhook_conn")
    hook.send(
        text=f"A dataset was changed! {dataset.uri}."
    )
    print("Done!")
    # if dataset.uri == "dataset_to_cause_listener_error":
    #     print("Oh no! That's the dataset that causes an error!")
    #     print("I will cause an error now...")
    #     print(10 / 0)


@hookimpl
def on_task_instance_succeeding():
    """Execute when task state changes to SUCCESS. previous_state can be None."""
    print("I am always listening for any TaskInstance to succeed and I heard that!")