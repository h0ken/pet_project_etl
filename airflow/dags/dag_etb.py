from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import subprocess

# Определяем DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    'spacex_pipeline',
    default_args=default_args,
    description='Pipeline для обработки данных SpaceX и отправки информации через Telegram-бота',
    schedule_interval=None,  # Запуск только вручную, без темпа
    start_date=days_ago(1),
    catchup=False,
)

# Функции для запуска скриптов
def run_script_1():
    subprocess.run(['python', '/opt/airflow/scripts/pars.py'], check=True)

def run_script_2():
    try:
        result = subprocess.run(['python', '/opt/airflow/scripts/process_launch.py'], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении process_launch.py: {e.stderr}")
        raise

def run_script_3():
    try:
        result = subprocess.run(
            ['python', '/opt/airflow/scripts/tg_bot.py'],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        raise


task1 = PythonOperator(
    task_id='fetch_launch_data',
    python_callable=run_script_1,
    dag=dag,
)

task2 = PythonOperator(
    task_id='process_launch_data',
    python_callable=run_script_2,
    dag=dag,
)

task3 = PythonOperator(
    task_id='send_launch_data',
    python_callable=run_script_3,
    dag=dag,
)

task1 >> task2 >> task3 