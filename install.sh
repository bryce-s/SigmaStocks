#!/usr/bin/bash
set -e
set -x
source env/bin/activate
pip install -r requirements.txt
npm run build
