FROM apache/superset:latest

USER root

# Установка дополнительных библиотек (если нужно)
RUN pip install psycopg2-binary

# Копирование пользовательских настроек
COPY superset_config.py /app/superset_config.py

# Копирование скрипта запуска
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER superset

# Установка точки входа
ENTRYPOINT ["/app/entrypoint.sh"]

