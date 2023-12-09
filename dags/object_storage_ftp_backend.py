"""
## Use Object Storage to read a file from a remote FTP server

This DAG reads a file from a remote FTP server using the Airflow 2.8 Object Storage feature.
It is an example of attaching a custom backend to the Object Storage.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.io.path import ObjectStoragePath
from airflow.io.store import attach
from fsspec.implementations.ftp import FTPFileSystem

attach(protocol="ftp", fs=FTPFileSystem(host="ftp.scene.org", anon=True))
base_path = ObjectStoragePath("ftp://pub/")


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["ObjectStorage"],
    doc_md=__doc__,
)
def object_storage_ftp_backend():
    @task
    def read_remote_ftp(base):
        """Read a file from the remote FTP server."""
        index_file = base / "index.txt"
        with index_file.open("r") as f:
            text = f.read()

        return text

    read_remote_ftp(base=base_path)


object_storage_ftp_backend()
