FROM quay.io/astronomer/astro-runtime-dev:10.0.0-alpha9

USER root

RUN apt-get update && apt-get install -y patch patchutils

RUN set -ex; \
curl -o /tmp/36247.patch https://patch-diff.githubusercontent.com/raw/apache/airflow/pull/36247.patch; \
cd /usr/local/lib/python3.11/site-packages/airflow; \
filterdiff -p1 -i 'airflow*' /tmp/36247.patch | patch -u -p 2; \
rm /tmp/36247.patch

USER astro

ENV AIRFLOW__WEBSERVER__ALLOW_RAW_HTML_DESCRIPTIONS=True
ENV AIRFLOW__WEBSERVER__NAVBAR_COLOR="#377030"
ENV AIRFLOW__WEBSERVER__NAVBAR_TEXT_COLOR="#bf0000"