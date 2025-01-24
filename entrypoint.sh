#!/bin/bash

superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname Admin \
    --email admin@example.com \
    --password admin

superset db upgrade
superset init

# Запускаем Superset
superset run -h 0.0.0.0 -p 8088
