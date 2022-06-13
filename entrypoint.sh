#!/bin/sh

cd /app/ && pip install .

cd vecsim_app/ && python load_data.py

python main.py