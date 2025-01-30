import os
import pandas as pd
from sqlalchemy import create_engine, text

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
    engine = create_engine(DATABASE_URI)
    
    with engine.connect() as connection:
        connection.execute(text(CREATE_SCHEMA_SQL))
        connection.execute(text(CREATE_TABLE_SQL))
    
    data = pd.read_csv(CSV_FILE)

    data['flight_success_rate'] = data['flight_success_rate'].replace("No information available", None)

    data['flight_success_rate'] = data['flight_success_rate'].map({'true': True, 'false': False, None: None})
    
    data.to_sql("flights", engine, schema="space_missions", if_exists="append", index=False)


if __name__ == "__main__":
    main()