from airflow import Dataset
from airflow.listeners import hookimpl
from airflow.providers.slack.notifications.slack import send_slack_notification


@hookimpl
def on_dataset_changed(dataset: Dataset):
    """Execute when dataset change is registered."""
    print("I am always listening for any Dataset changes and I heard that!")
    print("Posting to Slack...")
    send_slack_notification(
        slack_conn_id="my_slack_conn",
        text=f"Dataset {dataset.uri} was changed!",
        channel="#alerts"
    )
    print(10/0)
    print("Done!")
    if dataset.uri == "s3://my-bucket/my-dataset.csv":
        # failure condition
        print("This is a dataset I am interested in!")
        print("Let's do something else...")
        print("Done!")
