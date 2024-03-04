from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'lLab-sy',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(times: int):
    print("Hello Airflow!\n"*times)

with DAG(
    dag_id='dag_with_python_operator_v1',
    default_args=default_args,
    description='this is my first time write dag on airflow with python operator',
    start_date=datetime(2024, 3, 1),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id = "greet",
        python_callable=greet,
        op_kwargs={'times': 3}
    )
    task1