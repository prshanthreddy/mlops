from airflow import DAG
from airflow.decorators import task
from datetime import datetime

# Define the DAG
with DAG(
    dag_id="math_operations_with_taskflowapi",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@once",
    catchup=False,
) as dag:
        @task
        def add(x: int, y: int) -> int:
            return x + y
    
        @task
        def subtract(x: int, y: int) -> int:
            return x - y
    
        @task
        def multiply(x: int, y: int) -> int:
            return x * y
    
        @task
        def divide(x: int, y: int) -> float:
            return x / y
    
        # Define the task dependencies
        result1 = add(1, 2)
        result2 = subtract(result1, 1)
        result3 = multiply(result2, 3)
        result4 = divide(result3, 2)

    
