import csv
from stock import Stock_Obj
import datetime

reader = csv.DictReader(open('../data/news_reuters.csv'))
writer = csv.writer(open('../data/cleaned.csv', 'w'))
writer.writerow(
    ['ticker', 'company', 'date', 'movement', 'headline']
)
for row in reader:
    s = Stock_Obj(row['ticker'])
    rawdate = row['date']
    date = datetime.datetime(int(rawdate[0:4]), int(
        rawdate[4:6]), int(rawdate[6:]))
    print(row['ticker'], rawdate, ' ')
    try:
        price = s.get_delta_calculation(date)
        writer.writerow([row['ticker'], row['company'],
                     row['date'], price, row['headline']])
    except:
        pass

writer.close()