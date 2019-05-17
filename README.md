# Project Overview

Installation & Running:

For historical analysis:
```
cd content
python server/backtracing.py
python server/sentiment_stock.py
python server/mse.py
```




For the live verison:
```
git clone https://github.com/bryce-s/final_project.git
cd final_project/content
python3 -m venv env
sh bin/install.sh

cp server/*.py .
cp ./datavide_key.txt ..

sqlite3 server/portfolio.db
>> .read ./server/initialize.sql
>> ctrl d


python
>> import server.analyzer
>> server.analyzer.initalize_portfolio()
>> exit() 

python server/app.py > server_log 2>&1 & # run server in background
curl http://127.0.0.1:5000/ # make a dummy request to start the background process starts
# ignore the output of curl.

```
