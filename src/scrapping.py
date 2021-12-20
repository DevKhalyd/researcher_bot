# Contains the information about the post
import json
from typing import List
from models.reddit_item import RedditItem,redditItemFromDic
from bs4 import BeautifulSoup,Tag
import requests


baseUrl = "https://www.reddit.com"


def get_reddit_search_url(search: str) -> str:
    """Search in Reddit about something you want to know"""
    #search = search.replace(' ', '%20')
    url = f'{baseUrl}/search/?q={search}'
    return url


def get_reddit_community_url(complement: str) -> str:
    """Completes an url given by the Reddit Website"""
    return f'{baseUrl}{complement}'


def get_results_from_reddit(lookup: str) -> List[RedditItem]:
    url = get_reddit_search_url(lookup)
    print(f'Url: {url}')
    # Help to render the data without another library.
    # More info: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    response = requests.get(url, headers={"User-Agent": custom_user_agent})

    # Start to scrapping
    # Always install the lxml
    soup = BeautifulSoup(response.text, "lxml")

    # Contains all the data necessary to render
    # items = soup.find_all("div", class_=itemName)

    tag = soup.find("script", id="data")

    if type(tag) is not Tag:
        return []
    
    text = tag.getText()

    jsonToParse = text[14: len(text)  - 1]


    d = json.loads(jsonToParse)

    allPosts = d['posts']['models']

    redditItems: List[RedditItem] = []

    for key in allPosts:
        post = allPosts[key]
        item = redditItemFromDic(post)
        if item.image is not None:
            redditItems.append(item)
    return redditItems