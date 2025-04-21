from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.email import send_email
from datetime import datetime
import requests
import pandas as pd
import json
import os

# Paths
BRONZE_PATH = '/opt/airflow/data/bronze/breweries.json'
SILVER_PATH = '/opt/airflow/data/silver/breweries.parquet'
GOLD_PATH_1 = '/opt/airflow/data/gold/breweries_type.csv'
GOLD_PATH_2 = '/opt/airflow/data/gold/city_country.csv'

# Configurações de e-mail
EMAIL_TO = 'pedroresd1@gmail.com'

def failure_alert(context):
    """Callback function that sends an email on task failure."""
    task_instance = context.get('task_instance')
    subject = f"Airflow Task Failed: {task_instance.dag_id}.{task_instance.task_id}"
    body = f"""
    Olá,

    A task {task_instance.task_id} falhou no DAG {task_instance.dag_id}.

    Logs: {task_instance.log_url}
    Tentativa: {task_instance.try_number}
    """
    send_email(to=EMAIL_TO, subject=subject, html_content=body)

# Bronze Data
def extract_data():
    url = "https://api.openbrewerydb.org/v1/breweries"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        os.makedirs(os.path.dirname(BRONZE_PATH), exist_ok=True)
        with open(BRONZE_PATH, 'w') as f:
            json.dump(data, f)
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

# Silver Data
def transform_data():
    os.makedirs(os.path.dirname(SILVER_PATH), exist_ok=True)
    df = pd.read_json(BRONZE_PATH)
    df.to_parquet(SILVER_PATH)

# Gold Data
def aggregate_data():
    os.makedirs(os.path.dirname(GOLD_PATH_1), exist_ok=True)
    df = pd.read_parquet(SILVER_PATH)

    breweries_type = df.groupby('brewery_type').size().reset_index(name='count')
    breweries_type.to_csv(GOLD_PATH_1, index=False)

    city_country = df.groupby(['city', 'country']).size().reset_index(name='count')
    city_country.to_csv(GOLD_PATH_2, index=False)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 16),
    'on_failure_callback': failure_alert,  
}

# Dag
with DAG('brewery_data_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    extract = PythonOperator(task_id='extract_data', python_callable=extract_data)
    transform = PythonOperator(task_id='transform_data', python_callable=transform_data)
    aggregate = PythonOperator(task_id='aggregate_data', python_callable=aggregate_data)

    extract >> transform >> aggregate