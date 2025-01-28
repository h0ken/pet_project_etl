#!/bin/bash

superset db upgrade
superset fab create-admin --username "${ADMIN_USERNAME}" --firstname Superset --lastname Admin --email "${ADMIN_EMAIL}" --password "${ADMIN_PASSWORD}"
superset init
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
