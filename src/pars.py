import requests
import json

# URL API SpaceX
url = "https://api.spacexdata.com/v4/launches"

def fetch_launch_data() -> None:
    """
    Запрашивает данные о запусках SpaceX и сохраняет их в файл.

    Функция отправляет GET-запрос к API SpaceX, получает данные о запусках в формате JSON
    и записывает их в файл all_launches.json в папке /opt/synthetic_data.

    Исключения:
    - requests.exceptions.RequestException: если произошла ошибка при запросе.
    - Exception: для отлова любых других ошибок.
    """
    try:
        # Отправляем запрос к API
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        
        # Получаем данные в формате JSON
        launches = response.json()
        
        with open("/opt/synthetic_data/all_launches.json", "w") as file:
            json.dump(launches, file, indent=4)
        
        print("Данные сохранены в файл all_launches.json")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    fetch_launch_data()
