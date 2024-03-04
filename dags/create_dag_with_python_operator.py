from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'lLab-sy',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(mName, ti):
    name = ti.xcom_pull(task_ids='get_name')
    pokemon2 = ti.xcom_pull(task_ids='get_name', key='pokemon2')
    print(f'Hello {name} and {pokemon2}~! My name is {mName}!!')

def getName(ti):
    ti.xcom_push(key='pokemon2', value='Lizadon')
    return 'Pikachu'

with DAG(
    dag_id='dag_with_python_operator_v3',
    default_args=default_args,
    description='this is my first time write dag on airflow with python operator',
    start_date=datetime(2024, 3, 1),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id = "greet",
        python_callable=greet,
        op_kwargs={'mName': "Satoshi"}
    )

    task2 = PythonOperator(
        task_id = "get_name",
        python_callable=getName
    )

    task2 >> task1