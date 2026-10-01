#!/usr/bin/env bash
# build.sh — run by Render/Railway/CI during the build step
set -o errexit   # exit on any error

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
