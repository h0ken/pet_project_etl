from pyspark.sql import SparkSession
from pyspark.sql.functions import col, coalesce, lit, when
import os
import shutil

spark = SparkSession.builder \
    .appName("SpaceX Launches") \
    .getOrCreate()

json_path = "/opt/synthetic_data/all_launches.json"
temp_csv_path = "/opt/synthetic_data/temp_csv"
final_csv_path = "/opt/synthetic_data/launches_filtered.csv"

try:
    launches_df = spark.read.option("multiline", "true").json(json_path)
    launches_filtered_df = launches_df.select(
        coalesce(col("date_utc"), lit("No information available")).alias("Дата полета"),
        coalesce(col("name"), lit("No information available")).alias("Название корабля"),
        coalesce(
            when(col("success").isNotNull(), col("success").cast("string")).otherwise(lit("No information available")),
            lit("No information available")
        ).alias("Успешность полета"),
        coalesce(col("links.webcast"), lit("No information available")).alias("Ссылка на YouTube")
    )

    launches_filtered_df.coalesce(1).write.option("header", "true").mode("overwrite").csv(temp_csv_path)

    temp_file = next(f for f in os.listdir(temp_csv_path) if f.endswith(".csv"))
    os.rename(os.path.join(temp_csv_path, temp_file), final_csv_path)

    shutil.rmtree(temp_csv_path)
    print(f"Данные успешно сохранены в файл {final_csv_path}")

except Exception as e:
    print(f"Ошибка: {e}")
    raise

finally:
    spark.stop()
