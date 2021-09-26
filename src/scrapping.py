# Contains the information about the post
from typing import List
from reddit_item import RedditItem
from bs4 import BeautifulSoup
import requests


itemName = "_2MkcR85HDnYngvlVW2gMMa"
# Contains the ref to the new post
itemReference = "y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE"
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

    # Always install the lxml
    soup = BeautifulSoup(response.text, "lxml")

    # Contains all the data necessary to render
    items = soup.find_all("div", class_=itemName)
    # Contains all the references
    itemsReference = soup.find_all("div", class_=itemReference)

    redditItems: List[RedditItem] = []

    for i in range(len(items)):

        redditItem = RedditItem()

        item = items[i]
        itemRef = itemsReference[i]

        # Get the title
        # Basically if is not an image don't send nothing from here
        div = item.find("div")
        if div is not None:
            title = div.get("aria-label")
            if title is not None:
                redditItem.title = title

        # Get the background Image or a news reference
        # Basically if is not an image don't send nothing from here
        a = item.find("a")
        if a is not None:
            img = a.get('href')
            if img is not None:
                if "jpg" in img or "png" in img:
                    redditItem.image = img

        # Get the ref
        # Basically if is not an image send only this reference
        aRef = itemRef.find("a")
        if aRef is not None:
            href = aRef.get('href')
            if href is not None:
                ref = get_reddit_community_url(href)
                redditItem.reference = ref

        redditItems.append(redditItem)
    
    return redditItems
    
    """
    print('List to save:')
    string = RedditItem.convert_list_to_string(redditItems)
    print(string)
    # Save the objets with a key as follow:
    print('Retriving list to show:')
    print(len(RedditItem.convert_string_to_list(string)))
    """