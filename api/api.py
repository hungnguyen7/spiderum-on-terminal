import requests

class SpiderumAPI:
    BASE_URL = 'https://spiderum.com/api/v1'
    FEED_URL = f'{BASE_URL}/feed/getAllPosts?type=hot&page={{page_idx}}'
    POST_URL = f'{BASE_URL}/post/'

    @classmethod
    def fetch_posts(cls, page_idx):
        url = cls.FEED_URL.format(page_idx=page_idx)
        print("Getting data from:", url)
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.json()['posts']["items"]

    @classmethod
    def fetch_post_content(cls, slug):
        url = cls.POST_URL + slug
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.json()["post"]
