#!/usr/bin/bash
set -e
set -x

source env/bin/activate
pip freeze > requirements.txt