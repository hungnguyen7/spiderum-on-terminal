import requests
from imgcat import imgcat

BASE_URL = 'https://spiderum.com/api/v1'
FEED_URL = f'{BASE_URL}/feed/getAllPosts?type=hot&page={{page_idx}}'
POST_URL = f'{BASE_URL}/post/'


def get_posts(page_idx):
    url = FEED_URL.format(page_idx=page_idx)
    print("Getting data from:", url)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    data = response.json()
    return data['posts']["items"]


def show_list_posts(posts):
    for idx, post in enumerate(posts):
        print(f'{idx}. {post["title"]}')


def get_post_content(slug):
    url = POST_URL + slug
    response = requests.get(url, verify=False)
    response.raise_for_status()
    data = response.json()
    post = data["post"]
    print(f'\n{post["title"]}\n')
    for block in post["blockBody"]["blocks"]:
        if block["type"] == "smallerHeader":
            print(f'\n{block["data"]["text"]}\n')
            
        if block["type"] == "paragraph":
            print(block["data"]["text"])
            
        # if block["type"] == "image":
        #     url = block["data"]["file"]["url"]
        #     imgcat(requests.get(url, verify=False).content)

def main():
    current_page = 1
    posts = get_posts(current_page)
    show_list_posts(posts)
    
    while True:
        ans = input("Select a post to read (N to next page, P to previous page, L to show list, X to exit): ").strip().upper()
        
        if ans == 'X':
            break
        elif ans == 'N':
            current_page += 1
            posts = get_posts(current_page)
            show_list_posts(posts)
        elif ans == 'P':
            if current_page > 1:
                current_page -= 1
                posts = get_posts(current_page)
                show_list_posts(posts)
            else:
                print("This is the first page")
        elif ans == 'L':
            show_list_posts(posts)
        elif ans.isdigit() and 0 <= int(ans) < len(posts):
            get_post_content(posts[int(ans)]['slug'])
        else:
            print("Invalid input. Please try again.")
    

if __name__ == '__main__':
    main()
