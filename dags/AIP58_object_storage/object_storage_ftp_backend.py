"""
## Use Object Storage to read a file from a remote FTP server

This DAG reads a file from a remote FTP server using the Airflow 2.8 Object Storage feature.
It is an example of attaching a custom backend to the Object Storage.
"""

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.io.path import ObjectStoragePath
from airflow.io.store import attach
from fsspec.implementations.ftp import FTPFileSystem
from fsspec.registry import known_implementations
from pendulum import datetime

attach(protocol="ftp", fs=FTPFileSystem(host="ftp.scene.org", anon=True))
base_path = ObjectStoragePath("ftp://pub/")
# see: https://filesystem-spec.readthedocs.io/en/latest/


@dag(
    start_date=datetime(2023, 12, 1),
    schedule="0 0 * * *",
    catchup=False,
    doc_md=__doc__,
    tags=["ObjectStorage", "2-8", "core", "webinar"],
)
def object_storage_ftp_backend():
    @task
    def print_known_fsspec_implementations(known_impl):
        """Print known fsspec implementations."""
        for i in known_impl:
            print(i)

    @task
    def read_remote_ftp(base):
        """Read a file from the remote FTP server."""
        index_file = base / "index.txt"
        with index_file.open("r") as f:
            text = f.read()

        return text

    chain(
        print_known_fsspec_implementations(known_implementations),
        read_remote_ftp(base=base_path),
    )


object_storage_ftp_backend()
