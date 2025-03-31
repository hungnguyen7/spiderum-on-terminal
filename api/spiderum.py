import requests
import time


class SpiderumAPI:
    """
    A simple API client for Spiderum

    Attributes:
        BASE_URL: The base URL of the Spiderum API
        FEED_URL: The URL to get all posts
        POST_URL: The URL to get a post by slug
    """
    BASE_URL = 'https://spiderum.com/api/v1'
    FEED_URL = f'{BASE_URL}/feed/getAllPosts?type=hot&page={{page_idx}}'
    POST_URL = f'{BASE_URL}/post/'

    @classmethod
    def fetch_posts(cls, page_idx):
        """
        Fetch all posts from Spiderum

        Args:
            page_idx (int): The page index to get posts from

        Returns:
            list: A list of posts
        """
        try:
            url = cls.FEED_URL.format(page_idx=page_idx)
            print("Getting data from:", url)
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status()
            return response.json()['posts']["items"]
        except requests.exceptions.ConnectionError:
            print("ConnectionError: retrying in 5 seconds")
            time.sleep(5)
            return cls.fetch_posts(page_idx)

    @classmethod
    def fetch_post_content(cls, slug):
        """
        Fetch a post by slug

        Args:
            slug (str): The slug of the post

        Returns:
            dict: The post content
        """
        try:
            url = cls.POST_URL + slug
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status()
            return response.json()["post"]
        except requests.exceptions.ConnectionError:
            print("ConnectionError: retrying in 5 seconds")
            time.sleep(5)
            return cls.fetch_post_content(slug)

    @staticmethod
    def fetch_post_by_url(url):
        """
        Fetch a post by URL

        Args:
            url (str): The URL of the post

        Returns:
            dict: The post content
        """
        slug = url.split('/')[-1]
        return SpiderumAPI.fetch_post_content(slug)
