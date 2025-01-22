import requests
import json

# URL API SpaceX
url = "https://api.spacexdata.com/v4/launches"

def fetch_launch_data():
    try:
        # Отправляем запрос к API
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        
        # Получаем данные в формате JSON
        launches = response.json()
        
        with open("/opt/airflow/synthetic_data/all_launches.json", "w") as file:
            json.dump(launches, file, indent=4)
        
        print("Данные успешно загружены и сохранены в файл all_launches.json!")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    fetch_launch_data()
