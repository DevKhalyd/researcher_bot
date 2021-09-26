from typing import List

# Separator on each item
object_separator = "&&"


class RedditItem:
    """A response from Reddit website"""

    def __init__(self, title: str = '', image: str = '', reference: str = ''):
        self.title = title
        self.image = image
        self.reference = reference

    def convert_to_telegram_msg(self) -> str:
        """Send a message in MARKDOWN2 to telegram user"""
        title = self.title
        image = self.image
        reference = self.reference

        if title and image:
            return f'{title} \n {image}'
            
        return reference

    @staticmethod
    def convert_list_to_string(items: List) -> str:
        if items is None:
            return

        separator = "@"

        string = ""
        # Allow to split the string into a list of RedditItem objects
        for index, item in enumerate(items):
            title = item.title
            image = item.image
            reference = item.reference
            if index == len(items) - 1:
                separator = ""
            if title and image:
                string += f"{title}{object_separator}{image}{separator}"
                continue
            string += f"{reference}{separator}"
        return string

    @staticmethod
    def convert_string_to_list(items: str) -> List:

        if items is None:
            return []

        # Separator of objects
        separator = "@"
        itemsToUse: List[RedditItem] = []

        objects = items.split(separator)

        for object in objects:
            newObject = RedditItem()
            object = object.split(object_separator)
            # It's a reference
            if len(object) == 1:
                newObject.reference = object[0]
                itemsToUse.append(newObject)
                continue

            # It's a title and a image
            if len(object) == 2:
                newObject.title = object[0]
                newObject.image = object[1]
                itemsToUse.append(newObject)
                continue

        return itemsToUse

    def __str__(self):
        return f"""
        Title: {self.title}
        Image: {self.image}
        Reference: {self.reference}
        """
