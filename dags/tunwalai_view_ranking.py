import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import date, datetime, timedelta

def run(playwright):
    # Launch browser
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Navigate to the target website
    page.goto("https://www.tunwalai.com/story/type/topview?period=daily")

    # Wait for a specific element to load if needed
    page.wait_for_selector('div')

    # Extract data (e.g., page title or content)
    top3_content = page.query_selector_all('div.item.top3')

    current_date = date.today()

    # rank:int, name:string, author:string, category:string, date:datetime
    novel_list = []
    for content in top3_content:
        rank = len(novel_list)+1
        name = content.query_selector('div.content-main-text').inner_text()
        author = content.query_selector('div.one-line-text.content-sub-text').inner_text()
        category = content.query_selector('div.one-line-text.content-sub-sub-text').inner_text()
        novel_list.append({"rank": rank, "name": name, "author": author,\
                            "category": category, "date": current_date})

    other_content = page.query_selector_all('div.item.pt-16.pb-16.d-flex')
    for content in other_content:
        rank = content.query_selector('div.ranking-number').inner_text()
        name = content.query_selector('div.content-main-text').inner_text()
        author = content.query_selector('div.one-line-text.content-sub-text').inner_text()
        category = content.query_selector('div.one-line-text.content-sub-sub-text').inner_text()
        novel_list.append({"rank": rank, "name": name, "author": author,\
                            "category": category, "date": current_date})

    # Close the browser
    browser.close()
    return novel_list

def get_tunwalai_daily_most_view():
    with sync_playwright() as playwright:
        return run(playwright)

# Define your ETL functions

def extract(**kwargs):
    # For example, fetch data from an API or database.
    # Here we just simulate extracting a dataset
    data = get_tunwalai_daily_most_view()
    df = pd.DataFrame(data)
    return df.to_dict()  # Pass the dataframe as a dictionary to XCom

def transform(**kwargs):
    # Retrieve data from XCom
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract')
    
    # Convert the dict back to a pandas DataFrame
    df = pd.DataFrame(extracted_data)
    
    # Send transformed data to XCom
    return df.to_dict()

def load(**kwargs):
    # Retrieve the transformed data from XCom
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract')

    # Establish PostgreSQL connection
    conn = psycopg2.connect(
        host="localhost",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    # Insert data into the users table
    insert_query = "INSERT INTO novels (rank, name, author, category, date) VALUES (%s, %s, %s, %s, %s)"
    cur.executemany(insert_query, extracted_data)

    # Commit and close the connection
    conn.commit()
    cur.close()
    conn.close()



# Define the DAG
default_args = {
    'owner': 'lLab-sy',
    'start_date': datetime.today(),
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# Set task dependencies

with DAG(
    dag_id='tunwalai_view_ranking',
    default_args=default_args,
    description='this dag load daily most view from tunwalai',
    schedule='@daily'
) as dag:
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
        dag=dag,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        dag=dag,
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
        dag=dag,
    )

    extract_task >> transform_task >> load_task 
