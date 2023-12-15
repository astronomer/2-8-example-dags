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

## Option 1: Use GitHub Codespaces

Run this Airflow project without installing anything locally.

1. Fork this repository.
2. Create a new GitHub codespaces project on your fork. Make sure it uses at least 4 cores!
3. After creating the codespaces project the Astro CLI will automatically start up all necessary Airflow components. This can take a few minutes. 
4. Once the Airflow project has started, access the Airflow UI by clicking on the **Ports** tab and opening the forward URL for port 8080.

## Option 2: Use the Astro CLI

Download the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) to run Airflow locally in Docker. `astro` is the only package you will need to install.

1. Run `git clone https://github.com/astronomer/2-7-example-dags.git` on your computer to create a local clone of this repository.
2. Install the Astro CLI by following the steps in the [Astro CLI documentation](https://docs.astronomer.io/astro/cli/install-cli). Docker Desktop/Docker Engine is a prerequisite, but you don't need in-depth Docker knowledge to run Airflow with the Astro CLI.
3. Run `astro dev start` in your cloned repository.
4. After your Astro project has started. View the Airflow UI at `localhost:8080`.

# DAGs

The following sections list the DAGs shown sorted by the feature that they showcase. You can filter DAGs in the UI by their `tags`.

### Setup/ teardown

DAGs that showcase the `setup` and `teardown` tasks added in Airflow 2.7. For further information see the [setup/ teardown guide](https://docs.astronomer.io/learn/airflow-setup-teardown).

Four use case DAGs:

- `setup_teardown_cleanup_xcom`: DAG that plays Texas Hold'em Poker. Shows hot to use a teardown task to clean up XComs. Needs a [custom XCom backend](https://docs.astronomer.io/learn/xcom-backend-tutorial) using S3 and a connection to AWS. The relevant environment variables are shown in `.env.example` and the custom XCom backend can be imported from `include/custom_xcom_backend/s3_xcom_backend.py`.
- `setup_teardown_complex_sqlite_decorators`: DAG that shows 3 nested setup/ teardown workflows modifying data about Star Trek in a SQLite database. Has a data quality check using the SQLColumnCheckOperator for which it needs a connection to the SQLite database (see `.env.example` or the DAG description).
- `setup_teardown_csv_decorators`: A setup/teardown pipeline that can be run locally which works on a CSV file. Uses decorators.
- `setup_teardown_csv_methods` A setup/teardown pipeline that can be run locally which works on a CSV file. Uses methods.

Three toy DAGs:

- `toy_setup_teardown_simple`: Shows a very simple setup/ teardown workflow to nest setup/ teardown tasks with empty `@task` tasks.
- `toy_setup_teardown_nesting`: Shows how to nest setup/ teardown tasks with empty `@task` tasks.
- `toy_setup_teardown_task_group_and_failures`: DAG that shows special behavior of teardown tasks in a task group. All tasks can be set to fail individually via params to explore the behavior of the DAG.

- `setup_teardown_csv_NO_setup_teardown`: This DAG exists as a comparison to the `setup_teardown_csv_methods` and `setup_teardown_csv_decorators` DAG. It does not use setup/ teardown tasks.

### Dependency functions

DAGs that showcase the dependency functions `chain()`, `cross_downstream()` and the dependency function added in Airflow 2.7: `chain_linear()`.

- `toy_chain_linear_vs_chain_simple`: Simple comparison between `chain()` and `chain_linear()`.
- `toy_chain_linear_vs_chain_complex`: Shows how `chain_linear()` allows dependencies between lists of different lengths.
- `toy_chain_linear_task_group`: Shows `chain_linear()` being used with tasks and task groups.
- `toy_cross_downstream`: Shows how to use `cross_downstream()` to compare to `chain_linear()` (the former can only take 2 positional arguments).

### Other

DAGs that showcase other features added in Airflow 2.7.

- `toy_apprise_provider_example`: Shows how to use the Apprise provider to send notifications. This DAG needs an apprise connection `apprise_default` to be configured.
- `toy_deferrable_operators_config`: Shows how to use the `deferrable` parameter in the `TriggerDagRunOperator` to defer the execution of a DAG. The config that was added in 2.7 is set to `True` in the Dockerfile `ENV AIRFLOW__OPERATORS__DEFAULT_DEFERRABLE=True`.
- `toy_fail_stop`: DAG that has `fail_stop` enabled with tasks that take different amounts of time to finish.

### Helpers 

DAGs that are here to support another DAG.

- `helper_dag_wait_30_seconds`: DAG that is triggered by the TriggerDagRunOperator in the `toy_deferrable_operators_config` DAG. It waits 30 seconds before completing.

## Useful links

- [Setup/ teardown](https://docs.astronomer.io/learn/airflow-setup-teardown) guide.
- [Managing task dependencies in Airflow](https://docs.astronomer.io/learn/managing-dependencies) guide.
- [Manage Airflow DAG notifications](https://docs.astronomer.io/learn/error-notifications-in-airflow) guide.
- [Deferrable operators](https://docs.astronomer.io/learn/deferrable-operators) guide.

# Project Structure

This repository contains the following files and folders:

- `.astro`: files necessary for Astro CLI commands.
- `.devcontainer`: the GH codespaces configuration.
-  `dags`: all DAGs in your Airflow environment. Files in this folder will be parsed by the Airflow scheduler when looking for DAGs to add to your environment. You can add your own dagfiles in this folder.
- `include`: supporting files that will be included in the Airflow environment.
    - `custom_xcom_backend`: folder.
        - `s3_xcom_backend.py`: contains a custom XCom backend using S3. See also [custom XCom backends](https://docs.astronomer.io/learn/xcom-backend-tutorial).
- `plugins`: folder to place Airflow plugins. Empty.
- `tests`: folder to place pytests running on DAGs in the Airflow instance. Contains default tests.
- `.astro-registry.yaml`: file to configure DAGs being uploaded to the [Astronomer registry](https://registry.astronomer.io/). Can be ignored for local development.
- `.dockerignore`: list of files to ignore for Docker.
- `.env.example`: example environment variables for the DAGs in this repository. Copy this file to `.env` and replace the values with your own credentials.
- `.gitignore`: list of files to ignore for git.
- `Dockerfile`: the Dockerfile using the Astro CLI.
- `packages.txt`: system-level packages to be installed in the Airflow environment upon building of the Dockerimage. Empty.
- `README.md`: this Readme.
- `requirements.txt`: python packages to be installed to be used by DAGs upon building of the Dockerimage.