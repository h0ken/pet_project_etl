import telebot
import pandas as pd
from consts import API_TOKEN

# Инициализация бота с токеном
bot = telebot.TeleBot(API_TOKEN)

# Загружаем данные из CSV файла
data = pd.read_csv("/opt/synthetic_data/launches_filtered.csv")

# Словарь для хранения данных о пользователях
user_data = {}

def send_instruction(message):
    """
    Отправляет пользователю инструкцию по использованию бота.

    Параметры:
    - message (telebot.types.Message): сообщение пользователя.
    """
    instruction = (
        "Привет! Я бот, который помогает найти видео запусков ракет SpaceX.\n\n"
        "Используйте команду /start, чтобы начать работу.\n\n"
        "Я помогу вам выбрать запуск по году и месяцу. После этого предоставлю вам все доступные записи."
    )
    bot.send_message(message.chat.id, instruction)

@bot.message_handler(commands=['start'])
def start(message):
    """
    Обрабатывает команду /start. Просит пользователя ввести год запуска.

    Параметры:
    - message (telebot.types.Message): сообщение пользователя.
    """
    bot.send_message(
        message.chat.id,
        "Для того, чтобы получить видео запусков SpaceX, нужно узнать какая дата запуска ракеты вам интересна.\n\n"
        "Пожалуйста, укажите год, который вас интересует (2006-2022):"
    )
    bot.register_next_step_handler(message, process_year)

def process_year(message):
    """
    Обрабатывает ввод пользователя с годом запуска.

    Параметры:
    - message (telebot.types.Message): сообщение пользователя.
    """
    year = message.text.strip()

    if not year.isdigit() or int(year) < 2006 or int(year) > 2022:
        bot.send_message(message.chat.id, "Пожалуйста, введите год между 2006 и 2022. Попробуйте снова:")
        bot.register_next_step_handler(message, process_year)
        return

    filtered_data_year = data[data['flight_date'].str.contains(f'{year}-')]
    if filtered_data_year.empty:
        bot.send_message(message.chat.id, f"Извините, в {year} не было запусков. Пожалуйста, выберите другой год.")
        bot.register_next_step_handler(message, process_year)
    else:
        user_data[message.chat.id] = {'year': year}
        bot.send_message(message.chat.id, f"Вы выбрали {year}. Теперь укажите месяц (1-12):")
        bot.register_next_step_handler(message, process_month)

def process_month(message):
    """
    Обрабатывает ввод пользователя с месяцем запуска.

    Параметры:
    - message (telebot.types.Message): сообщение пользователя.
    """
    month = message.text.strip()

    if not month.isdigit() or int(month) < 1 or int(month) > 12:
        bot.send_message(message.chat.id, "Неправильный месяц. Пожалуйста, введите месяц от 1 до 12.")
        bot.register_next_step_handler(message, process_month)
        return

    year = user_data.get(message.chat.id, {}).get('year')

    if not year:
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, начните заново, используя команду /start.")
        return

    filtered_data = data[data['flight_date'].str.contains(f'{year}-{month.zfill(2)}')]

    if filtered_data.empty:
        bot.send_message(message.chat.id, f"Извините, в {year}-{month} запусков не было. Пожалуйста, попробуйте другой месяц.")
        bot.register_next_step_handler(message, process_month)
    else:
        for _, row in filtered_data.iterrows():
            response = (
                f"Дата: {row['flight_date']}\n"
                f"Корабль: {row['ship_name']}\n"
                f"Успешность: {row['flight_success_rate']}\n"
                f"Ссылка на YouTube: {row['link_to_youtube']}\n"
            )
            bot.send_message(message.chat.id, response)
        bot.send_message(message.chat.id, "Вот все найденные запуски! Если хотите узнать еще, используйте /start.")

@bot.message_handler(func=lambda message: True)
def send_instruction_on_any_message(message):
    """
    Обрабатывает любое сообщение, кроме команд, отправляя инструкцию.

    Параметры:
    - message (telebot.types.Message): сообщение пользователя.
    """
    send_instruction(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
