#!/bin/bash

killall python3
rm webapp/database.db
. env.ini
. venv/bin/activate
python3 -mflask init-db
./utils/fill_db_with_fake_data.py

