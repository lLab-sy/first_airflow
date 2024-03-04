from datetime import datetime, timedelta
import pytz
from airflow import DAG
from airflow.operators.bash import BashOperator


def getCurrentTime(nHours = 0, nMinutes = 0):
    # Get the current time in UTC
    current_time_utc = datetime.utcnow()

    # Define the UTC+7 timezone
    timezone_utc7 = pytz.timezone('Asia/Bangkok')

    # Convert the current time to UTC+7 timezone
    current_time_utc7 = current_time_utc.astimezone(timezone_utc7)

    # Calculate the future time
    future_time_utc7 = current_time_utc7 + timedelta(minutes=nMinutes) + timedelta(hours=nHours)

    return future_time_utc7

default_args = {
    'owner': 'lLab-sy',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='my_first_dag',
    default_args=default_args,
    description='this is my first time write dag on airflow',
    start_date=getCurrentTime(),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is my first task in dag on airflow"
    )
    
    task1