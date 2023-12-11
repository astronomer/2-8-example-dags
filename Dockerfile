FROM quay.io/astronomer/astro-runtime-dev:10.0.0-alpha4

ENV AIRFLOW__WEBSERVER__ALLOW_RAW_HTML_DESCRIPTIONS=True

USER root
RUN pip install apache-airflow-providers-amazon[s3fs]==8.13.0rc1
USER astro