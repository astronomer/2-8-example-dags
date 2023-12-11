"""
## 
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.io.path import ObjectStoragePath


OBJECT_STORAGE = "s3"  # "file"
CONN_ID = "my_aws_conn"  # None
PATH = "ce-2-8-examples-bucket/poems/"

base = ObjectStoragePath(f"{OBJECT_STORAGE}://{PATH}", conn_id=CONN_ID)
#base = ObjectStoragePath("file://include/poems/")
#base = ObjectStoragePath("s3://my_aws_conn@ce-2-8-examples-bucket/poems/")

@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["ObjectStorage"],
    doc_md=__doc__,
)
def object_storage_test():
    @task
    def list_files() -> list[ObjectStoragePath]:
        files = [f for f in base.iterdir()]
        return files

    list_files()

    @task
    def read_file_content():
        """Read a file from remote object storage and return utf-8 decoded text."""
        file=base / "the_raven_poe.txt"
        bytes = file.read_block(offset=0, length=None)
        text = bytes.decode("utf-8")
        return text
    
    read_file_content()

object_storage_test()
