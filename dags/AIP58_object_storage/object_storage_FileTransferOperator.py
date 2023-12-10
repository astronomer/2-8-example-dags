"""
## Move a file from one remote object storage to another using the FileTransferOperator

The FileTransferOperator was added in Airflow 2.8 and is a generic operator to move files
between different object storage systems.
"""

from airflow.decorators import dag
from pendulum import datetime

# from airflow.providers.common.io.operators.file_transfer import FileTransferOperator
from include.operators.file_transfer import FileTransferOperator

SRC_CONN = "my_aws_conn"
DST_CONN = "my_aws_conn"
PATH_SRC = "s3://ce-2-8-examples-bucket/lyrics/mensch.txt"
PATH_DST = "s3://ce-2-8-examples-bucket/lyrics_copy/mensch_copy.txt"

# Alternatively you can use the FileTransferOperator with ObjectStoragePath
# from airflow.io.path import ObjectStoragePath
# PATH_SRC = ObjectStoragePath("s3://ce-2-8-examples-bucket/lyrics/mensch.txt", conn_id="my_aws_conn")
# PATH_DST = ObjectStoragePath("s3://ce-2-8-examples-bucket/lyrics_copy/mensch_copy.txt", conn_id="my_aws_conn")


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["ObjectStorage"],
)
def object_storage_FileTransferOperator():
    f = FileTransferOperator(
        task_id="test",
        source_conn_id=SRC_CONN,
        src=PATH_SRC,
        dest_conn_id=DST_CONN,
        dst=PATH_DST,
    )


object_storage_FileTransferOperator()
