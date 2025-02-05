from pyspark.sql import SparkSession
from pyspark.sql.functions import col, coalesce, lit, when
import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

spark = SparkSession.builder.appName("SpaceX Launches").getOrCreate()

JSON_PATH = "/opt/synthetic_data/all_launches.json"
TEMP_CSV_PATH = "/opt/synthetic_data/temp_csv"
FINAL_CSV_PATH = "/opt/synthetic_data/launches_filtered.csv"

try:
    logging.info("Чтение JSON-файла")
    launches_df = spark.read.option("multiline", "true").json(JSON_PATH)
    
    logging.info("Обработка данных")
    launches_filtered_df = launches_df.select(
        coalesce(col("date_utc"), lit("No information available")).alias("flight_date"),
        coalesce(col("name"), lit("No information available")).alias("ship_name"),
        coalesce(
            when(col("success").isNotNull(), col("success").cast("string")),
            lit("No information available")
        ).alias("flight_success_rate"),
        coalesce(col("links.webcast"), lit("No information available")).alias("link_to_youtube")
    )
    
    logging.info("Сохранение данных во временный CSV")
    launches_filtered_df.coalesce(1).write.option("header", "true").mode("overwrite").csv(TEMP_CSV_PATH)
    
    # Поиск созданного CSV-файла и перемещение его в нужное место
    temp_files = [f for f in os.listdir(TEMP_CSV_PATH) if f.endswith(".csv")]
    if temp_files:
        os.rename(os.path.join(TEMP_CSV_PATH, temp_files[0]), FINAL_CSV_PATH)
        logging.info(f"Файл сохранен: {FINAL_CSV_PATH}")
    else:
        logging.warning("CSV-файл не найден в временной папке")
    
    # Удаление временной папки
    shutil.rmtree(TEMP_CSV_PATH, ignore_errors=True)
    
    logging.info(f"Данные успешно сохранены в файл {FINAL_CSV_PATH}")

except Exception as e:
    logging.exception(f"Ошибка: {e}")

finally:
    logging.info("Остановка Spark-сессии")
    spark.stop()

