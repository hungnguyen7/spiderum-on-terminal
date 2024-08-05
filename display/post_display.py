from utils.printer import Printer
from utils.colors import GREEN, YELLOW, BLUE, LIGHT_GRAY, PURPLE
import re

class PostDisplay:
        
    @staticmethod
    def show_list_posts(posts, db):
        for idx, post in enumerate(posts):
            is_read = db.is_post_read(post['slug'])
            status = 'Read' if is_read else 'New'
            Printer.print_with_style(f'{idx+1}. {post["title"]} ({status})', color = PURPLE if is_read else GREEN)

    @staticmethod
    def display_post_content(post):
        Printer.print_with_style(f'---{post["title"]}---', color=GREEN)
        for block in post["blockBody"]["blocks"]:
            if block["type"] == "smallerHeader":
                text = re.sub(r'<[^>]*>', '', block["data"]["text"])
                Printer.print_with_style(text, color=BLUE)
            elif block["type"] == "paragraph":
                text = re.sub(r'<[^>]*>', '', block["data"]["text"])
                Printer.print_with_style(text, color=LIGHT_GRAY)
            # elif block["type"] == "image":
            #     url = block["data"]["file"]["url"]
            #     imgcat(requests.get(url, verify=False).content)