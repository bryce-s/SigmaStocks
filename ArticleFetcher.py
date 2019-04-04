import os
import sys
import feedparser
import json

class ArticleFetcher:
    """public facing module manages various fetchers"""
    def __init__(self, json_news_sources: dict):
        """default constructor"""
        pass
        


    def fetch_articles(self, **kwargs):
        """fetch articles by **kwargs[method]"""
        if kwargs['method'] == "RSS":
            pass
        elif kwargs['method'] == "Kaggle":
            pass
        else:
            print("Please provide either 'Kaggle' or 'RSS' as method= arg.")
            # do we want to throw something...?
            # not now.im 
        # methods include active RRS, Kaggle
        pass


