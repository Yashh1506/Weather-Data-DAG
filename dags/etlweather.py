import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd

def fetch_and_insert_weather_data():
    """
    Fetches weather data from Open-Meteo API and inserts it into PostgreSQL database
    using PostgresHook for connection management.
    """
    # Fetch data from weather API
    api = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,precipitation_probability,rain"
    response = requests.get(api)
    weather_dict = response.json()
    
    # Convert to DataFrame
    weather_dataframe = pd.DataFrame(weather_dict['hourly'])
    
    # Get PostgreSQL connection using PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    engine = postgres_hook.get_sqlalchemy_engine()
    
    # Insert data into PostgreSQL table
    weather_dataframe.to_sql('new_dag_data', engine, if_exists='replace', index=False)
    
    # Log row count for monitoring
    row_count = len(weather_dataframe)
    print(f"Inserted {row_count} rows of weather data into database")
    
    return row_count

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 7),
    'retries': 1
}

with DAG(
    'etlweather',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='ETL pipeline for weather data using PostgresHook',
    tags=['weather', 'example']
) as dag:
    
    load_data = PythonOperator(
        task_id = "load_dataframe",
        python_callable=fetch_and_insert_weather_data
    )

    load_data