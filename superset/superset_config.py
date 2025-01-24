import os
from superset.config import *

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "pass_UnreAl_comm_2026")

# Адрес подключения PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://airflow:airflow@postgres/airflow'

# Кэширование (по желанию)
CACHE_CONFIG = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
}

# Настройки аутентификации (по умолчанию, без изменений)
AUTH_TYPE = 1