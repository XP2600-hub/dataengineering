import pendulum

from airflow.sdk import dag
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator


def notify():
    print("Pipeline completed successfully!")


@dag(
    dag_id="mysql_to_iceberg_lab",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["lab", "mysql", "iceberg"],
)
def mysql_to_iceberg_lab():

    start = EmptyOperator(
        task_id="start",
    )

    def extract():
        print("Extracting data from MySQL...")

    extract_task = PythonOperator(
        task_id="extract_mysql",
        python_callable=extract,
    )

    def create_iceberg():
        print("Creating Iceberg table...")
        print("Writing Parquet files to S3...")

    iceberg_task = PythonOperator(
        task_id="create_iceberg_table",
        python_callable=create_iceberg,
    )

    notify_task = PythonOperator(
        task_id="notify_success",
        python_callable=notify,
    )

    finish = EmptyOperator(
        task_id="finish",
    )

    start >> extract_task >> iceberg_task >> notify_task >> finish


mysql_to_iceberg_lab()
