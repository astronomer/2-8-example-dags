"""
## Interact with remote object storage using the Airflow 2.8 Object Storage feature

This DAG shows examples of methods and properties of the Airflow 2.8 Object Storage 
feature, including how to read the content of a file and rename a file in remote
object storage.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.io.path import ObjectStoragePath
from airflow.models.baseoperator import chain

OBJECT_STORAGE = "s3" 
CONN_ID = "aws_s3_webinar_conn"  
PATH = "ce-2-8-examples-bucket/poems"

base = ObjectStoragePath(f"{OBJECT_STORAGE}://{PATH}", conn_id=CONN_ID)


@dag(
    start_date=datetime(2023, 12, 1),
    schedule="0 0 * * *",
    catchup=False,
    doc_md=__doc__,
    tags=["ObjectStorage", "2-8", "webinar"],
)
def object_storage_showcase():
    @task
    def list_files(base_path: ObjectStoragePath) -> list[ObjectStoragePath]:
        """List files in remote object storage."""
        path = base_path / ""
        files = [f for f in path.iterdir() if f.is_file()]
        return files

    @task
    def read_file_content(file: ObjectStoragePath):
        """Read a file from remote object storage and return utf-8 decoded text."""
        bytes = file.read_block(offset=0, length=None)
        text = bytes.decode("utf-8")
        return text

    @task
    def print_properties_methods_file(file: ObjectStoragePath):
        """Print object storage properties of a file."""

        # You can mostly use the same API as https://github.com/fsspec/universal_pathlib 
        # https://docs.python.org/3/library/pathlib.html
        # with the ObjectStoragePath class.
        # Plus some Extensions: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html#extensions 
        # Sometimes there are limits due to the backend. 

        print("_____________________________________________________________")
        print(f"File: {file}")
        print("_____________________________________________________________")
        print("Properties:")
        print(f".container: {file.container}")
        print(f".bucket: {file.bucket}")
        print(f".key: {file.key}")
        print(f".path: {file.path}")
        print("_____________________________________________________________")
        print("Methods:")
        print(f".stat(): {file.stat()}")
        try:
            print(
                f".samefile(file): {file.samefile(file)}"
            )  # returns True if the file is the same as the given file
        except:
            print("Samefile not supported by this backend.")
        print(f".cwd(): {file.cwd()}")
        print(f".home(): {file.home()}")
        print("_____________________________________________________________")
        print("Extended operations:")
        print(f".ukey() (Hash of the file properties): {file.ukey()}")
        print(f".checksum() (Checksum of the file at this path): {file.checksum()}")
        # try:
        #     print(f".sign() (create a signed URL): {file.sign()}")
        # except:
        #     print("Sign not supported by this backend.")
        print(f".size: {file.size()}")  # size in bytes
        print("_____________________________________________________________")
        print("Serialization:")
        print(f".serialize(): {file.serialize()}")
        print("_____________________________________________________________")
        print("Some pathlib methods and properties:")
        print(f".exists(): {file.exists()}")
        print(f".is_file(): {file.is_file()}")
        print(f".is_dir(): {file.is_dir()}")
        print(f".parts: {file.parts}")
        print(f".drive: {file.drive}")
        print(f".root: {file.root}")
        print(f".anchor: {file.anchor}")
        print(f".parent: {file.parent}")
        print(f".name: {file.name}")
        print(f".suffix: {file.suffix}")
        print(f".suffixes: {file.suffixes}")
        print(f".stem: {file.stem}")
        print(f".as_posix(): {file.as_posix()}")
        print(f".as_uri(): {file.as_uri()}")
        print(
            f".is_symlink(): {file.is_symlink()}"
        )  # Return True if the path points to a symbolic link, False otherwise.

    @task
    def rename_file(file: ObjectStoragePath):
        """Rename a file in remote object storage."""
        file_name = file.path.split("/")[-1]
        file_path = file.path.strip(file_name)

        print(f"Full remote file path: {file.path}")
        print(f"File path without file (cwd): {file_path}")
        print(f"File name: {file_name}")

        if file_name[0] == "0":
            print("Target path: " + file_name.strip("0_"))
            file.replace(target=file_name.strip("0_"))
            print("Ran file.replace(target=file_name.strip('0_'))")
        else:
            print("Target path: " + "0_" + file_name)
            file.replace(target="0_" + file_name)
            print("Ran file.replace(target='0_' + file_name)")

    @task
    def create_new_file(base_path: ObjectStoragePath):
        """Create a new file in remote object storage."""
        new_file = base_path / "new_poem.txt"
        new_file.touch()
        print(f"Created new file: {new_file}")

    @task
    def write_to_new_file(base_path: ObjectStoragePath):
        """Write to a new file in remote object storage."""
        new_file = base_path / "new_poem.txt"
        new_file.write_text("This is a new poem.")
        # Alternatively you can write bytes directly:
        # file.write_bytes(b"This is a new poem.")
        print(f"Wrote to new file: {new_file}")

    @task
    def delete_file(base_path: ObjectStoragePath):
        """Delete a file in remote object storage."""
        file = base_path / "new_poem.txt"
        file.unlink()

    files_s3 = list_files(base_path=base)
    files_renamed = rename_file.expand(file=files_s3)

    chain(
        [
            read_file_content.expand(file=files_s3),
            print_properties_methods_file.expand(file=files_s3),
        ],
        files_renamed,
        create_new_file(base_path=base),
        write_to_new_file(base_path=base),
        delete_file(base_path=base),
    )


object_storage_showcase()
