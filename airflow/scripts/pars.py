import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://api.spacexdata.com/v4/launches"
OUTPUT_FILE = "/opt/synthetic_data/all_launches.json"

def fetch_launch_data() -> None:
    """
    Запрашивает данные о запусках SpaceX и сохраняет их в файл.

    Исключения:
    - requests.exceptions.RequestException: если произошла ошибка при запросе.
    - Exception: для отлова любых других ошибок.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()
        
        launches = response.json()
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(launches, file, indent=4, ensure_ascii=False)
        
        logging.info("Данные сохранены в: %s", OUTPUT_FILE)
    except requests.exceptions.RequestException as e:
        logging.error("Ошибка при запросе: %s", e)
    except Exception as e:
        logging.exception("Неожиданная ошибка")

if __name__ == "__main__":
    fetch_launch_data()