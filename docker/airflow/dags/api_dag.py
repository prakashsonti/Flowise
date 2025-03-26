from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from pendulum import timezone


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

stocks = ['msft', 'aapl', 'googl', 'hsy']
endpoints = ['', '/history', '/news', '/options']

@dag(
    start_date=datetime(2025, 3, 13, tzinfo=timezone("America/Chicago")),
    schedule_interval='0 1 * * *',  # 1 AM CST daily
    catchup=False
)
def multi_stock_api_dag():
    
    @task
    def call_api(**kwargs):
        stock = kwargs['stock']
        endpoint = kwargs['endpoint']
        url = f'http://stockapi:5000/api/stock/{stock}{endpoint}'
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Success for {stock}{endpoint}: {response.json()}")
        else:
            print(f"Failed for {stock}{endpoint}: {response.status_code}")

    # Create all combinations
    call_api.expand_kwargs([
        {'stock': stock, 'endpoint': endpoint}
        for stock in stocks
        for endpoint in endpoints
    ])

stock_api_dag_instance = multi_stock_api_dag()

#def stock_api_dag():
#
#    @task
#    def call_api(endpoint):
#        url = f'http://stockapi:5000/api/stock/msft{endpoint}'
#        response = requests.get(url)
#        if response.status_code == 200:
#            print(response.json())
#        else:
#            print(f"API call failed with status code: {response.status_code}")
#
#    call_api.expand(endpoint=['', '/history', '/news'])
#
#stock_api_dag()




#dag = DAG(
#    'api_call_dag',
#    default_args=default_args,
#    description='A simple DAG that calls an API',
#    schedule_interval=timedelta(days=1),
#)


#def call_api():
#    url = f'http://stockapi:5000/api/stock/msft'
#    response = requests.get(url)
#    if response.status_code == 200:
#        print(response.json())
#    else:
#        print(f"API call failed with status code: {response.status_code}")


#api_task = PythonOperator(
#    task_id='call_api_task',
#    python_callable=call_api,
#    dag=dag,
#)

