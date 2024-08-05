from utils.printer import Printer
from utils.colors import GREEN, BLUE, LIGHT_GRAY, PURPLE, RED
import re
from utils.tts import TTS

class PostDisplay:
    def __init__(self):
        # Initialize text to speech
        self.tts = None
        try:
            self.tts = TTS()
        except RuntimeError as e:
            print(f"Error initializing TTS: {e}")
        
    @staticmethod
    def show_list_posts(posts, db):
        for idx, post in enumerate(posts):
            is_read = db.is_post_read(post['slug'])
            status = 'Read' if is_read else 'New'
            Printer.print_with_style(f'{idx+1}. {post["title"]} ({status})', color = PURPLE if is_read else GREEN)

    def display_post_content(self, post, enable_tts):
        Printer.print_with_style(f'---{post["title"]}---', color=GREEN)
        for block in post["blockBody"]["blocks"]:
            if block["type"] == "smallerHeader":
                text = re.sub(r'<[^>]*>', '', block["data"]["text"])
                Printer.print_with_style(text, color=BLUE)
                if enable_tts:
                    if self.tts is not None:
                        self.tts.speak(text)
                    else:
                        Printer.print_with_style("Error initializing TTS", color=RED)
            elif block["type"] == "paragraph":
                text = re.sub(r'<[^>]*>', '', block["data"]["text"])
                Printer.print_with_style(text, color=LIGHT_GRAY)
                if enable_tts:
                    if self.tts is not None:
                        self.tts.speak(text)
                    else:
                        Printer.print_with_style("Error initializing TTS", color=RED)
    
    @staticmethod
    def show_help():
        Printer.print_with_style('Usage:', color=GREEN)
        Printer.print_with_style("  Type 'N' to fetch next page")
        Printer.print_with_style("  Type 'P' to fetch previous page")
        Printer.print_with_style("  Type 'V' to enable text to speech, re-type to disable")