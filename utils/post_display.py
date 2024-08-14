import re
from utils.printer import Printer
from utils.colors import GREEN, BLUE, PURPLE, RED, GRAY
from utils.tts import TTS


class PostDisplay:
    """
    Class to display posts and help menu.

    Attributes:
        tts (TTS): Text-to-speech object.
    """

    def __init__(self):
        self.tts = self.initialize_tts()

    @staticmethod
    def initialize_tts():
        """
        Initialize the text-to-speech object.

        Returns:
            TTS (TTS or None): Text-to-speech object or None if an error occurred.
        """
        try:
            return TTS()
        except RuntimeError as e:
            print(f"Error initializing TTS: {e}")
            return None

    @staticmethod
    def show_list_posts(posts):
        """
        Display the list of posts.

        Args:
            posts (list): List of posts.

        Returns:
            None
        """
        for idx, post in enumerate(posts):
            status = 'Read' if post["is_read"] else 'New'
            color = PURPLE if post["is_read"] else GREEN
            Printer.print_with_style(
                f'{idx + 1}. {post["title"]} ({status})', color=color)

    def display_post_content(self, post, enable_tts, show_image):
        """
        Display the content of a post.

        Args:
            post (dict): Post object.
            enable_tts (bool): Enable text-to-speech.
            show_image (bool): Show images in the article.

        Returns:
            None
        """
        Printer.print_with_style(f'---{post["title"]}---', color=GREEN)
        for block in post["blockBody"]["blocks"]:
            self.display_block(block, enable_tts, show_image)

    def display_block(self, block, enable_tts, show_image):
        """
        Display a block of content.

        Args:
            block (dict): Block object.
            enable_tts (bool): Enable text-to-speech.
            show_image (bool): Show images in the article.

        Returns:
            None
        """
        block_type = block["type"]
        # * Remove HTML tags and &nbsp; characters from text
        text = re.sub(r'<[^>]*>|&nbsp;', '', block["data"].get("text", ""))

        if block_type == "smallerHeader":
            self.print_and_speak(text, BLUE, enable_tts)
        elif block_type == "paragraph":
            self.print_and_speak(text, GRAY, enable_tts)
        elif block_type == "image" and show_image:
            Printer.print_image_from_url(block["data"]["file"]["url"])

    def print_and_speak(self, text, color, enable_tts):
        """
        Print text and speak it if text-to-speech is enabled.

        Args:
            text (str): Text to display.
            color (str): Color of the text.
            enable_tts (bool): Enable text-to-speech.

        Returns:
            None
        """
        Printer.print_with_style(f"\n{text}", color=color)
        if enable_tts and self.tts:
            self.tts.speak(text)
        elif enable_tts:
            Printer.print_with_style("Error initializing TTS", color=RED)

    @staticmethod
    def show_help():
        """
        Display the help menu.

        Returns:
            None
        """
        keymap = {
            'N': 'Fetch the next list of articles.',
            'P': 'Fetch the previous list of articles.',
            'F': 'Go to the first page of list of articles.',
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
