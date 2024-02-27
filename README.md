# Example DAGs for Apache Airflow 2.8

This repository contains example DAGs showing features released in Apache Airflow 2.8. 

Aside from core Apache Airflow this project uses:
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) to run Airflow locally (version 1.20.1).
- The [Amazon Airflow provider](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest) with the `s3fs` extra installed.
- The [Slack Airflow provider](https://registry.astronomer.io/providers/apache-airflow-providers-slack/versions/latest).
- The [Common IO Airflow provider](https://registry.astronomer.io/providers/apache-airflow-providers-common-io/versions/latest).
- The [scikit-learn](https://scikit-learn.org/stable/) package.

For pinned versions of the provider packages see the `requirements.txt` file.

# How to use this repository

This section explains how to run this repository with Airflow. 

> [!NOTE]  
> Some DAGs in this repository require additional connections or tools. The `on_dataset_changed` listener uses a [Slack Webhook connection](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/connections/slack-incoming-webhook.html) with the ID `slack_webhook_conn` Some of the ObjectStorage example DAGs (tag: `ObjectStorage`) are using a connection to AWS S3 with the connection ID `my_aws_conn`. If you use a different object provider you will need to adjust the connection name and URI in the relevant DAGs.
> You can define these connection in the Airflow UI under **Admin > Connections** or by using the `.env` file with the format shown in `.env.example`.

See the [Manage Connections in Apache Airflow](https://docs.astronomer.io/learn/connections) guide for further instructions on Airflow connections. 

DAGs with the tag `core` work without any additional connections or tools.

## Steps to run this repository

Download the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) to run Airflow locally in Docker. `astro` is the only package you will need to install.

1. Run `git clone https://github.com/astronomer/2-8-example-dags.git` on your computer to create a local clone of this repository.
2. Install the Astro CLI by following the steps in the [Astro CLI documentation](https://docs.astronomer.io/astro/cli/install-cli). Docker Desktop/Docker Engine is a prerequisite, but you don't need in-depth Docker knowledge to run Airflow with the Astro CLI.
3. Run `astro dev start` in your cloned repository.
4. After your Astro project has started. View the Airflow UI at `localhost:8080`.

# DAGs

The following sections list the DAGs shown sorted by the feature that they showcase. You can filter DAGs in the UI by their `tags`.

### AIP58_object_storage

- `object_storage_FileTransferOperator`: uses the `FileTransferOperator` to transfer files from one location in S3 to another.
- `object_storage_ftp_backend`: attaches a custom FTP backend to the `ObjectStoragePath` class to interact with an FTP server.
- `object_storage_list_read_remote`: simple example of a pipeline using several methods of the `ObjectStoragePath` class to list, read and write files to an object storage.
- `object_storage_load_file_to_duckdb`: loads a local parquet file into a [DuckDB](https://duckdb.org/) database using the `ObjectStoragePath` class.
- `object_storage_showcase`: shows several methods and attributes of the `ObjectStoragePath` class.
- `object_storage_use_case`: simple ML pipeline that trains a model and uses the Object Storage feature to move training data between different locations.

### Other 

- `branching_example`: shows the new `@task.branch_external_python` and `@task.branch_virtualenv` decorators.
- `html_example`: contains raw HTML in the DAG Docs and [Airflow Params](https://docs.astronomer.io/learn/airflow-params) description, which is rendered in the UI if because `AIRFLOW__WEBSERVER__ALLOW_RAW_HTML_DESCRIPTIONS` is set to `True` in the Dockerfile.
- `params_example`: a DAG using several Airflow params to show the new `Trigger DAG` UI.
- `pool_example`: a DAG using a pool called `my_garden_pool` to limit the number of tasks running in parallel. You will need to create this pool in the Airflow UI under **Admin > Pools** to run this DAG.
- `producer_example`: produces to a Dataset to show the `on_dataset_changed` listener. Note that the `on_dataset_changed` listener uses a [Slack Webhook connection](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/connections/slack-incoming-webhook.html) with the ID `slack_webhook_conn`. You will need to create this connection in the Airflow UI under **Admin > Connections** to get Slack notifications from the listener.
- `xcom_tab_example`: DAG that pushes several XComs to show the new XCom tab in the UI.
- `deltalake_example`: Shows [Delta Lake](https://delta.io/) table serialization.
- `literal_wrapper_example`: Shows the `literal` function used to disable Jinja templating in a task parameter.

### Helpers 

DAGs that are here to support another DAG.

- `consumer_dag`: DAG that is triggered by the Dataset updated by the `producer_dag`.

## Useful links

- [Object Storage Basic tutorial](https://docs.astronomer.io/learn/airflow-object-storage-tutorial).
- [Object Storage OSS Docs tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/objectstorage.html#object-storage).
- [Object Storage OSS Docs guide](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html#object-storage).
- [Branching Guide](https://docs.astronomer.io/learn/airflow-branch-operator).
- [Listeners OSS Docs](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/listeners.html#listeners).
- [Datasets guide](https://docs.astronomer.io/learn/airflow-datasets).
- [Airflow Config reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html).

# Project Structure

This repository contains the following files and folders:

- `.astro`: files necessary for Astro CLI commands.
-  `dags`: all DAGs in your Airflow environment. Files in this folder will be parsed by the Airflow scheduler when looking for DAGs to add to your environment. You can add your own dagfiles in this folder.
- `include`: supporting files that will be included in the Airflow environment. Among other files contains the code for the listener plugin in `include/listeners.py`.
- `plugins`: folder to place Airflow plugins. Contains a listener plugin.
- `tests`: folder to place pytests running on DAGs in the Airflow instance. Contains default tests.
- `.astro-registry.yaml`: file to configure DAGs being uploaded to the [Astronomer registry](https://registry.astronomer.io/). Can be ignored for local development.
- `.dockerignore`: list of files to ignore for Docker.
- `.env.example`: example environment variables for the DAGs in this repository. Copy this file to `.env` and replace the values with your own credentials.
- `.gitignore`: list of files to ignore for git.
- `Dockerfile`: the Dockerfile using the Astro CLI. Sets environment variables to change Airflow webserver settings.
- `packages.txt`: system-level packages to be installed in the Airflow environment upon building of the Docker image. Empty.
- `README.md`: this Readme.
- `requirements.txt`: python packages to be installed to be used by DAGs upon building of the Docker image.
