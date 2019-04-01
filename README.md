<<<<<<< HEAD
# Project Overview

Training Steps:

- Fetch Article
- Generate Sentiment
- Get Stock Movement
- Assign += 1


## Fetching Articles

``
{
  "APPL:": {
    "news_source": "WSJ"
    "id": "12391290",
    "title": "airplay flails again, good work APPL",
    "date": "2029-09-11T00:00:00.000Z"
  },
  "BRYCE:": {
    "news_source": "CNBC"
    "id": "69696969",
    "title": "Bryce buys a llama",
    "date": {}
  }
}
``
=======
# final_project

todo:
```
training system for past data
rss system # (for live data)
system to pull from a finance api # sanket wants to do this
machine learning blah blah classification
use ML data to make future predicitons
"hureistics?" # sanket also wants to do this..
a front end
```
>>>>>>> 53b5bd835630daa21852d4ebea7d6ef000685749

# Specs:

Training System


```usage: ./classifier training_data.json # or, make our own format and pipe it in.. i like json``` 


training_data.json
```
{
  "APPL:": {
    "id": "12391290",
    "title": "airplay flails again, good work APPL",
    "date": "2029-09-11T00:00:00.000Z"
  },
  "BRYCE:": {
    "id": "69696969",
    "title": "Bryce buys a llama",
    "date": {}
  }
}
```






