"""
## 
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.io.path import ObjectStoragePath
from airflow.models.baseoperator import chain

OBJECT_STORAGE_INGEST = "s3"
CONN_ID_INGEST = "my_aws_conn"
PATH_INGEST = "ce-2-8-examples-bucket/use_case_object_storage/"

OBJECT_STORAGE_TRAIN = "file"  # "gcs"
CONN_ID_TRAIN = None  # "my_gcs_conn"
PATH_TRAIN = "include/train/"  # "ce-2-8-examples-bucket/use_case_object_storage/train"

OBJECT_STORAGE_ARCHIVE = "file"
CONN_ID_ARCHIVE = None
PATH_ARCHIVE = "include/archive/"


base_path_ingest = ObjectStoragePath(
    f"{OBJECT_STORAGE_INGEST}://{PATH_INGEST}", conn_id=CONN_ID_INGEST
)

base_path_train = ObjectStoragePath(
    f"{OBJECT_STORAGE_TRAIN}://{PATH_TRAIN}", conn_id=CONN_ID_TRAIN
)

base_path_archive = ObjectStoragePath(
    f"{OBJECT_STORAGE_ARCHIVE}://{PATH_ARCHIVE}", conn_id=CONN_ID_ARCHIVE
)


@dag(
    start_date=datetime(2023, 12, 1),
    schedule=None,
    catchup=False,
    tags=["ObjectStorage"],
    doc_md=__doc__,
)
def object_storage_use_case():
    @task
    def list_files_ingest(base: ObjectStoragePath) -> list[ObjectStoragePath]:
        """List files in remote object storage including subdirectories."""

        labels = [obj for obj in base.iterdir() if obj.is_dir()]
        files = [f for label in labels for f in label.iterdir() if f.is_file()]
        return files

    @task
    def copy_files_ingest_to_train(src: ObjectStoragePath, dst: ObjectStoragePath):
        """Copy a file from one remote system to another.
        The file is streamed in chunks using shutil.copyobj"""

        src.copy(dst=dst)

    @task
    def list_files_train(base: ObjectStoragePath) -> list[ObjectStoragePath]:
        """List files in remote object storage."""

        files = [f for f in base.iterdir() if f.is_file()]
        return files

    @task
    def get_text_from_file(file: ObjectStoragePath) -> dict:
        """Read files in remote object storage."""

        bytes = file.read_block(offset=0, length=None)
        text = bytes.decode("utf-8")

        key = file.key

        print(key)
        return {"label": key.split("/")[-2], "text": text}

    @task
    def train_model(train_data: list[dict]):
        """Train a Naive Bayes Classifier using the files in the train folder."""

        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.pipeline import make_pipeline
        from sklearn.model_selection import train_test_split

        text_data = [d["text"] for d in train_data]
        labels = [d["label"] for d in train_data]

        X_train, X_test, y_train, y_test = train_test_split(
            text_data, labels, test_size=0.2, random_state=42
        )

        model = make_pipeline(CountVectorizer(), MultinomialNB())

        model.fit(X_train, y_train)

        model_params = model.get_params()

        return model_params

    @task
    def copy_files_train_to_archive(src: ObjectStoragePath, dst: ObjectStoragePath):
        """Copy a file from a remote system to local storage."""

        src.copy(dst=dst)

    files_ingest = list_files_ingest(base=base_path_ingest)
    files_copied = copy_files_ingest_to_train.partial(dst=base_path_train).expand(
        src=files_ingest
    )
    files_train = list_files_train(base=base_path_train)
    train_data = get_text_from_file.expand(file=files_train)
    model_params = train_model(train_data=train_data)

    chain(files_copied, files_train)


object_storage_use_case()
