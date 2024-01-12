"""
## Move a file from one remote object storage to another using the FileTransferOperator

The FileTransferOperator is part of the common IO provider and
uses the 2.8 Airflow features ObjectStoragePath under the hood.
"""

from airflow.decorators import dag
from pendulum import datetime
from airflow.providers.common.io.operators.file_transfer import FileTransferOperator

SRC_CONN = "aws_s3_webinar_conn"
DST_CONN = "aws_s3_webinar_conn"
PATH_SRC = "s3://ce-2-8-examples-bucket/lyrics/mensch.txt"
PATH_DST = "s3://ce-2-8-examples-bucket/lyrics_copy/mensch_copy.txt"

# Alternatively you can use the FileTransferOperator with ObjectStoragePath
# from airflow.io.path import ObjectStoragePath
# PATH_SRC = ObjectStoragePath("s3://ce-2-8-examples-bucket/lyrics/mensch.txt", conn_id="my_aws_conn")
# PATH_DST = ObjectStoragePath("s3://ce-2-8-examples-bucket/lyrics_copy/mensch_copy.txt", conn_id="my_aws_conn")

# tip: using Object Storage within the same file storage uses the optimal path, no data is passed through the worker

@dag(
    start_date=datetime(2023, 12, 1),
    schedule="0 0 * * *",
    catchup=False,
    doc_md=__doc__,
    tags=["ObjectStorage", "2-8", "webinar", "Common IO Provider"],
)
def object_storage_FileTransferOperator():
    FileTransferOperator(
        task_id="transfer_file",
        source_conn_id=SRC_CONN,
        src=PATH_SRC,
        dest_conn_id=DST_CONN,
        dst=PATH_DST,
        overwrite=True,
    )


object_storage_FileTransferOperator()
