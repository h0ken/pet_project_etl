import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "airflow")

CSV_FILE = "/opt/synthetic_data/launches_filtered.csv"

DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

CREATE_SCHEMA_SQL = "CREATE SCHEMA IF NOT EXISTS space_missions;"
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS space_missions.flights (
    flight_date TIMESTAMP,
    ship_name VARCHAR(255),
    flight_success_rate BOOLEAN,
    link_to_youtube TEXT
);
"""

def main() -> None:
    """
    Загружает данные из CSV в базу данных PostgreSQL.

    Функция:
    1. Создает соединение с PostgreSQL.
    2. Создает схему и таблицу, если они не существуют.
    3. Читает данные из CSV-файла.
    4. Обрабатывает колонку `flight_success_rate`:
       - Заменяет "No information available" на None.
       - Преобразует значения 'true' и 'false' в соответствующие boolean значения.
    5. Загружает данные в таблицу `flights` схемы `space_missions`.

    Возвращает:
    - None
    """
    # Проверка существования CSV-файла
    if not os.path.exists(CSV_FILE):
        logging.error(f"Файл {CSV_FILE} не найден.")
        return

    try:
        engine = create_engine(DATABASE_URI)

        with engine.connect() as connection:
            logging.info("Создание схемы и таблицы, если они не существуют.")
            with connection.begin():  # Используем транзакцию
                connection.execute(text(CREATE_SCHEMA_SQL))
                connection.execute(text(CREATE_TABLE_SQL))

        logging.info(f"Чтение данных из файла {CSV_FILE}.")
        data = pd.read_csv(CSV_FILE)

        logging.info("Обработка колонки `flight_success_rate`.")
        data['flight_success_rate'] = data['flight_success_rate'].replace(
            "No information available", None
        )
        data['flight_success_rate'] = data['flight_success_rate'].map(
            {'true': True, 'false': False, None: None}
        )

        logging.info("Загрузка данных в таблицу `flights`.")
        with engine.begin() as connection:
            data.to_sql(
                "flights",
                con=connection,
                schema="space_missions",
                if_exists="append",
                index=False,
                method="multi"
            )

        logging.info("Данные успешно загружены в базу данных.")

    except Exception as e:
        logging.exception(f"Ошибка при выполнении программы: {e}")

    finally:
        # Закрытие соединения с базой данных
        if 'engine' in locals():
            engine.dispose()
        logging.info("Соединение с базой данных закрыто.")

if __name__ == "__main__":
    main()