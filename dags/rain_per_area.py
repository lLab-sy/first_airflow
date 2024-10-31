from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import requests
import pandas as pd
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine

# Define the DAG
default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "rain_per_area",
    default_args=default_args,
    description="A simple ETL pipeline with an API key from Airflow Variables for fetch rain data from data.go.th",
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Function to extract data from the API
    def extract_data(**kwargs):
        api_key = Variable.get("api_key")  # Fetch the API key from Airflow Variable
        url = "https://opend.data.go.th/get-ckan/datastore_search?resource_id=120aba77-b0a7-44c0-8043-91124dac45ed"  # Replace with actual API URL
        
        headers = {"api-key": api_key}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Push data to XCom for the next task to retrieve
            kwargs['ti'].xcom_push(key="extracted_data", value=data)
        else:
            raise Exception(f"Failed to fetch data, status code: {response.status_code}")

    # Function to transform the data
    def transform_data(**kwargs):
        # Retrieve data from XCom
        extracted_data = kwargs['ti'].xcom_pull(task_ids='extract', key="extracted_data")
        
        dict_data = dict(extracted_data)

        # Convert to DataFrame for processing
        df = pd.DataFrame(dict_data['result']['records'])
        
        # Example transformation: Select certain columns, add new columns, filter, etc.
        # "_id": 1,
        # "YEAR": 2018,
        # "MONTH": 1,
        # "PROV_ID": 10,
        # "PROV_N": "กรุงเทพมหานคร",
        # "MinRain": 54.29999924,
        # "MaxRain": 257.230011,
        # "AvgRain": 142.12
        ref_col_name = ['_id', 'YEAR', 'MONTH', 'PROV_ID', 'MinRain', 'MaxRain', 'AvgRain']
        new_col_name = ['id', 'year', 'month', 'prov_id', 'min_rain', 'max_rain', 'avg_rain']
        df = df[ref_col_name]  # Select specific columns
        df.rename(columns={old_name:new_name for old_name, new_name in zip(ref_col_name, new_col_name)})
        # Push transformed data to XCom
        transformed_data = df.to_json(orient="records")
        kwargs['ti'].xcom_push(key="transformed_data", value=transformed_data)

    # Function to load the data
    def load_data(**kwargs):
        transformed_data = kwargs['ti'].xcom_pull(task_ids='transform', key="transformed_data")
        df = pd.read_json(transformed_data, orient="records")
        # conn = BaseHook.get_connection("my_sql_conn")
        conn_str = Variable.get("conn_rain")
        engine = create_engine(conn_str)
        
        table_name = "rain_per_area"
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Data loaded successfully to {table_name}!")

    # Define tasks
    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
        provide_context=True
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
        provide_context=True
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_data,
        provide_context=True
    )

    # Task dependencies
    extract >> transform >> load
