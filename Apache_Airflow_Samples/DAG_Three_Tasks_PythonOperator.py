from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
default_args = {
        'owner': 'xp',
        'retries': 5,
        'retry_delay': timedelta(minutes=2)
        }

def welcome():
    print("Welcome to Python!")

with DAG(
    dag_id='our_xp_dag',  # Changed to use underscores
    description='This is our lab DAG',  # Corrected spelling of 'DAG'
    start_date=datetime(2025, 4, 1, 2),  # Corrected the assignment
    schedule_interval='@daily',  # Corrected spelling from 'scheduler_interval'
    default_args=default_args  # Added default_args here
) as dag:
    task1 = PythonOperator(
        task_id='first_task',
        python_callable=welcome
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo hey, this is the second task, and it should run after the first task"

    )

    task3 = BashOperator(
        task_id='third_task',
        bash_command="echo wlecome to the third job!"
    )

    task1.set_downstream(task2)
    task1.set_downstream(task3)
