from utils.printer import Printer
from utils.colors import GREEN, BLUE, LIGHT_GRAY, PURPLE, RED
import re
from utils.tts import TTS

class PostDisplay:
    def __init__(self):
        # * Initialize text to speech
        self.tts = None
        try:
            self.tts = TTS()
        except RuntimeError as e:
            print(f"Error initializing TTS: {e}")
        
    @staticmethod
    def show_list_posts(posts):
        for idx, post in enumerate(posts):
            status = 'Read' if post["is_read"] else 'New'
            Printer.print_with_style(f'{idx+1}. {post["title"]} ({status})', color = PURPLE if post["is_read"] else GREEN)

    def display_post_content(self, post, enable_tts, show_image):
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
            elif block["type"] == "image":
                if show_image:
                    Printer.print_image_from_url(block["data"]["file"]["url"])
    
    @staticmethod
    def show_help():
        keymap = {
            'N': 'Fetch the next list of articles.',
            'P': 'Fetch the previous list of articles.',
            'X': 'Quit the program.',
            'L': 'Show list of articles.',
            'V': 'Enable/disable the text-to-speech feature.',
            'I': 'Enable/disable showing images in the article.',
            'B': 'Bookmark the article (save post to file).',
            'H': 'Show the help menu.'
        }

        Printer.print_with_style('Usage:', color=GREEN)
        for key, action in keymap.items():
            Printer.print_with_style(f"  Type '{key}' to {action}")