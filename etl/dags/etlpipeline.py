from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from datetime import datetime
import json

## Define DAG
with DAG(
    dag_id="nasa_apod_postgres",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    ## Step 1:Create table in Postgres if not exists
    @task
    def create_table():
        ## initialize PostgresHook
        pg_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        ## create table query
        create_table_query = """
            CREATE TABLE IF NOT EXISTS nasa_apod (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                explanation TEXT,
                url TEXT,
                date DATE,
                media_type VARCHAR(255)
            );
        """
        ## execute query
        pg_hook.run(create_table_query)

    ## Step 2: Fetch data from NASA API(Astronomy Picture of the Day) [Extract]
    # https://api.nasa.gov/planetary/apod?api_key=oemAAOPfhFfpurSt2joMvy0eaGLUONgkNS9Q6PCe

    extract_apod = SimpleHttpOperator(
        task_id="extract_apod",
        http_conn_id="nasa_api",  ## Connection ID Defined In Airflow For NASA API
        endpoint="planetary/apod",  ## NASA API enpoint for APOD
        method="GET",  ## GET request
        data={
            "api_key": "{{ conn.nasa_api.extra_dejson.api_key }}"
        },  ## Use the API Key from the connection
        response_filter=lambda response: response.json(),  ## Convert response to json format
    )

    ## Step 3: Transform data (Pick the information we need o save in Postgres)
    @task
    def transform_apod_data(response):
        apod_data = {
            "title": response.get("title", ""),
            "explanation": response.get("explanation", ""),
            "url": response.get("url", ""),
            "date": response.get("date", ""),
            "media_type": response.get("media_type", ""),
        }
        return apod_data

    ## Step 4: Load data into Postgres [Load]
    @task
    def load_apod_data(apod_data):
        pg_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        insert_query = """
            INSERT INTO nasa_apod (title, explanation, url, date, media_type)
            VALUES (%s, %s, %s, %s, %s);
        """
        pg_hook.run(
            insert_query,
            parameters=(
                apod_data["title"],
                apod_data["explanation"],
                apod_data["url"],
                apod_data["date"],
                apod_data["media_type"],
            ),
        )

    
    ## Step 5: Define the task dependencies
    ## Extract
    create_table() >> extract_apod ## ENSURE CREATE TABLE TASK RUNS BEFORE EXTRACT TASK
    api_response=extract_apod.output

    ## Transform
    transformed_data=transform_apod_data(api_response)
    
    ## Load
    load_apod_data(transformed_data)

    ## Step 6: Verify data by using DBViewer in Airflow UI

