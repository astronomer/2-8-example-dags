from airflow import Dataset
from airflow.listeners import hookimpl


@hookimpl
def on_dataset_created(
    dataset: Dataset,
):
    """Execute when a new dataset is created."""
    print(f"Dataset {dataset} created.")


@hookimpl
def on_dataset_changed(
    dataset: Dataset,
):
    """Execute when dataset change is registered."""
    print(f"Dataset {dataset} changed.")
