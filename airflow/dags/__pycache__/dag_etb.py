from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

dag = DAG(
    "spacex_pipeline",
    default_args=default_args,
    description="Pipeline для обработки данных SpaceX и отправки информации через Telegram-бота",
    schedule_interval=None,  # вручную
    start_date=days_ago(0),
    catchup=False,
)

# Указываем путь к директории со скриптами
SCRIPTS_DIR = "/opt/airflow/scripts"

def run_script(script_name):
    """
    Универсальная функция для запуска Python-скриптов.
    Логирует stdout и stderr.
    """
    script_path = os.path.join(SCRIPTS_DIR, script_name)

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Скрипт {script_name} не найден по пути {script_path}")

    try:
        result = subprocess.run(
            ["python", script_path], check=True, capture_output=True, text=True
        )
        logging.info(f"Скрипт {script_name} выполнен успешно!")
        logging.info(f"stdout:\n{result.stdout}")
        if result.stderr:
            logging.warning(f"stderr:\n{result.stderr}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при выполнении {script_name}: {e.stderr}")
        raise

# задачи
task_fetch_data = PythonOperator(
    task_id="fetch_launch_data",
    python_callable=run_script,
    op_args=["pars.py"],
    dag=dag,
)

task_process_data = PythonOperator(
    task_id="process_launch_data",
    python_callable=run_script,
    op_args=["process_launch.py"],
    dag=dag,
)

task_load_db = PythonOperator(
    task_id="load_data_to_db",
    python_callable=run_script,
    op_args=["load_db.py"],
    dag=dag,
)

task_send_data = PythonOperator(
    task_id="send_launch_data",
    python_callable=run_script,
    op_args=["tg_bot.py"],
    dag=dag,
)

task_fetch_data >> task_process_data >> task_load_db >> task_send_data
