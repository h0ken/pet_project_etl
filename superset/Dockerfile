FROM apache/superset:latest

USER root

RUN pip install psycopg2-binary

COPY superset_config.py /app/superset_config.py

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

USER superset

ENTRYPOINT ["/app/entrypoint.sh"]

