import os
import pandas as pd
from sqlalchemy import create_engine, text

# Конфигурация подключения к PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "airflow")

# Путь к CSV-файлу
CSV_FILE = "/opt/synthetic_data/launches_filtered.csv"

# Строка подключения к PostgreSQL
DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# SQL для создания схемы и таблицы
CREATE_SCHEMA_SQL = "CREATE SCHEMA IF NOT EXISTS space_missions;"
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS space_missions.flights (
    flight_date TIMESTAMP,
    ship_name VARCHAR(255),
    flight_success_rate BOOLEAN,
    link_to_youtube TEXT
);
"""

def main():
    # Создаем соединение с PostgreSQL
    engine = create_engine(DATABASE_URI)
    
    with engine.connect() as connection:
        # Создаем схему
        connection.execute(text(CREATE_SCHEMA_SQL))
        print("Схема space_missions создана (если отсутствовала).")
        
        # Создаем таблицу
        connection.execute(text(CREATE_TABLE_SQL))
        print("Таблица flights создана (если отсутствовала).")
    
    # Загружаем CSV в DataFrame
    data = pd.read_csv(CSV_FILE)
    print("Данные из CSV загружены.")

     # Заменяем "No information available" на None для flight_success_rate
    data['flight_success_rate'] = data['flight_success_rate'].replace("No information available", None)

    # Преобразуем значения в boolean
    data['flight_success_rate'] = data['flight_success_rate'].map({'true': True, 'false': False, None: None})
    
    # Загружаем данные в PostgreSQL
    data.to_sql("flights", engine, schema="space_missions", if_exists="append", index=False)
    print("Данные успешно загружены в таблицу flights.")

if __name__ == "__main__":
    main()