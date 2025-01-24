#!/bin/bash

# Инициализация базы данных Superset
superset db upgrade

# Создание учетной записи администратора
superset fab create-admin --username "${ADMIN_USERNAME}" --firstname Superset --lastname Admin --email "${ADMIN_EMAIL}" --password "${ADMIN_PASSWORD}"

# Загрузка примерных данных (если необходимо)
# superset load_examples

# Настройка Superset
superset init

# Запускаем Superset
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
