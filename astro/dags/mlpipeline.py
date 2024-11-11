from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

## Define task 1:
def preprocess_data():
    print('Data preprocessing done')

## Define task 2:
def train_model():
    print('Model training done')

## Define task 3:
def evaluate_model():
    print('Model evaluation done')

## Define the DAG:
with DAG('ml_pipeline', start_date=datetime(2024, 1, 1), schedule_interval='@weekly') as dag:
    ## Define the tasks:
    preprocess_data = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data
    )

    train_model = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )

    evaluate_model = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model
    )

    ## Define the task dependencies using the bitshift operator: Order of tasks is important // Bitshift operator is used to define the order of tasks in the DAG
    preprocess_data >> train_model >> evaluate_model

