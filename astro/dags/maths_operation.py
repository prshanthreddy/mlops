"""
 We will create a DAG that will perform some basic mathematical operations.
    The DAG will have following tasks:
    Task 1: Start with a number
    Task 2: Add 5 to the number
    Task 3: Multiply the result by 2
    Task 4: Subtract 10 from the result
    Task 5: Compute the square of the result
    Task 6: Display the final result
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

 # Define Each Task :
def start(**context):
    context['ti'].xcom_push(key='current_value', value=10)
    print("Starting with number 10")

def add_5(**context):
    current_value=context['ti'].xcom_pull(key='current_value', task_ids='start_task')
    new_value=current_value+5
    context['ti'].xcom_push(key='current_value', value=new_value)
    print("Adding 5 to the number")

def multiply_by_2(**context):
    current_value=context['ti'].xcom_pull(key='current_value', task_ids='add_task')
    new_value=current_value*2
    context['ti'].xcom_push(key='current_value', value=new_value)
    print("Multiplying the result by 2")

def subtract_10(**context):
    current_value=context['ti'].xcom_pull(key='current_value', task_ids='multiply_task')
    new_value=current_value-10
    context['ti'].xcom_push(key='current_value', value=new_value)
    print("Subtracting 10 from the result")

def square(**context):
    current_value=context['ti'].xcom_pull(key='current_value', task_ids='subtract_task')
    new_value=current_value**2
    context['ti'].xcom_push(key='current_value', value=new_value)
    print("Computing the square of the result")

def display_result(**context):
    current_value=context['ti'].xcom_pull(key='current_value', task_ids='square_task')
    print(f"Final result is {current_value}")


# Define the DAG:
with DAG('maths_operations', start_date=datetime(2024, 1, 1), schedule_interval='@once') as dag:
    # Define the tasks:
    start_task = PythonOperator(
        task_id='start_task',
        python_callable=start,
        provide_context=True
    )

    add_task = PythonOperator(
        task_id='add_task',
        python_callable=add_5,
        provide_context=True
    )

    multiply_task = PythonOperator(
        task_id='multiply_task',
        python_callable=multiply_by_2,
        provide_context=True

    )

    subtract_task = PythonOperator(
        task_id='subtract_task',
        python_callable=subtract_10,
        provide_context=True

    )

    square_task = PythonOperator(
        task_id='square_task',
        python_callable=square,
        provide_context=True
    )

    display_task = PythonOperator(
        task_id='display_task',
        python_callable=display_result,
        provide_context=True
    )

    # Define the task dependencies using the bitshift operator:
    start_task >> add_task >> multiply_task >> subtract_task >> square_task >> display_task 
    