"""
## List files in remote object storage and copy them to local storage

This DAG shows the basic use of the Airflow 2.8 Object Storage feature.
It lists files in remote object storage and copies them to local storage.
To be able to run this DAG you need to install the relevant provider package
for your object storage and define an Airflow connection to is.

- `apache-airflow-providers-amazon[s3fs]>=8.12.0` for S3
- `apache-airflow-providers-google>=10.12.0` for Google Cloud Storage
- `apache-airflow-providers-microsoft-azure>=8.3.0` for Azure Blob Storage

`file://` for local object storage is always available.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.io.path import ObjectStoragePath

OBJECT_STORAGE_SRC = "s3"
CONN_ID_SRC = "aws_s3_webinar_conn"
KEY_SRC = "ce-2-8-examples-bucket"

OBJECT_STORAGE_DST = "file"
CONN_ID_DST = None
KEY_DST = "include/poems/"

base_src = ObjectStoragePath(f"{OBJECT_STORAGE_SRC}://{KEY_SRC}", conn_id=CONN_ID_SRC)
base_dst = ObjectStoragePath(f"{OBJECT_STORAGE_DST}://{KEY_DST}", conn_id=CONN_ID_DST)


@dag(
    start_date=datetime(2023, 12, 1),
    schedule="0 0 * * *",
    catchup=False,
    doc_md=__doc__,
    tags=["ObjectStorage", "webinar", "2-8"],
)
def object_storage_list_read_remote():
    @task
    def list_files(base_path: ObjectStoragePath) -> list[ObjectStoragePath]:
        """List files in remote object storage."""
        path = base_path / "poems/"
        files = [f for f in path.iterdir() if f.is_file()]
        return files  # list of ObjectStoragePath objects, serializeable!

    @task
    def copy_file_to_local(dst: ObjectStoragePath, file: ObjectStoragePath):
        """Copy a file from remote to local storage.
        The file is streamed in chunks using shutil.copyobj"""

        file.copy(dst=dst)

    @task
    def read_file_content(file: ObjectStoragePath):
        """Read a file from remote object storage and return utf-8 decoded text."""
        bytes = file.read_block(offset=0, length=None)
        text = bytes.decode("utf-8")
        return text

    files_s3 = list_files(base_path=base_src)
    copy_file_to_local.partial(dst=base_dst).expand(file=files_s3)
    read_file_content.expand(file=files_s3)


object_storage_list_read_remote()
