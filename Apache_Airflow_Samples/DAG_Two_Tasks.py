from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
        'owner': 'xp',
        'retries': 5,
        'retry_delay': timedelta(minutes=2)
        }

with DAG(
    dag_id='our_xp_dag',  # Changed to use underscores
    description='This is our lab DAG',  # Corrected spelling of 'DAG'
    start_date=datetime(2025, 4, 1, 2),  # Corrected the assignment
    schedule_interval='@daily',  # Corrected spelling from 'scheduler_interval'
    default_args=default_args  # Added default_args here
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo Hello world! come together, this is the first task!"  # Added 'echo' for command
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo hey, this is the second task, and it should run after the first task"

    )

    task1.set_downstream(task2)
