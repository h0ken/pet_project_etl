import os
from superset.config import *

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "pass_UnreAl_comm_2026")

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://airflow:airflow@postgres/airflow'

CACHE_CONFIG = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
}

AUTH_TYPE = 1