import requests
import json

def fetch_news(api_key, query, languague ='pt'):
    url = f''