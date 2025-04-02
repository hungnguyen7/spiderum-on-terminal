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
            print(
                f"Error initializing TTS: {e}. Looks like our AI lost its voice. Time for some tea and honey! 🍯☕")
            return None

    @staticmethod
    def render_post_list(posts):
        """
        Display the list of posts.

        Args:
            posts (list): List of posts.

        Returns:
            None
        """
        Printer.wipe_screen()
        for idx, post in enumerate(posts):
            status = 'Read' if post["is_read"] else 'New'
            color = PURPLE if post["is_read"] else GREEN
            Printer.print_with_style(
                f'{idx + 1}. {post["title"]} ({status})', color=color)

    def render_post_content(self, post, enable_tts, show_image):
        """
        Display the content of a post.

        Args:
            post (dict): Post object.
            enable_tts (bool): Enable text-to-speech.
            show_image (bool): Show images in the article.

        Returns:
            None
        """
        Printer.wipe_screen()
        Printer.print_with_style(f'---{post["title"]}---', color=GREEN)
        for block in post["blockBody"]["blocks"]:
            self.render_content_block(block, enable_tts, show_image)

    def render_content_block(self, block, enable_tts, show_image):
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
        text = ""
        if isinstance(block, dict) and "data" in block:
            text = re.sub(r'<[^>]*>|&nbsp;', '', block["data"].get("text", ""))

        if block_type == "smallerHeader":
            self.render_text_with_speech(text, BLUE, enable_tts)
        elif block_type == "paragraph":
            self.render_text_with_speech(text, GRAY, enable_tts)
        elif block_type == "image" and show_image:
            Printer.print_image_from_url(block["data"]["file"]["url"])

    def render_text_with_speech(self, text, color, enable_tts):
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

    def render_bookmark_list(self, bookmarks):
        """
        Display the list of bookmarks.

        Args:
            bookmarks (list): List of bookmarks.

        Returns:
            None
        """
        Printer.wipe_screen()
        if not bookmarks:
            Printer.print_with_style("No bookmarks found.", color=RED)
            return

        Printer.print_with_style("Bookmarks:", color=GREEN)
        for idx, bookmark in enumerate(bookmarks):
            Printer.print_with_style(
                f'{idx + 1}. {bookmark["title"]}', color=PURPLE)

    @staticmethod
    def render_help_instructions():
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
            'U': 'Show post via URL.',
            'B': 'Bookmark the article (save post to file).',
            'BM': 'Show list of bookmarks.',
            'H': 'Show the help menu.',
            'Number Keys': 'Read the article with the corresponding number.',
            '(B||b) + Number Keys': 'Read the bookmark with the corresponding number.',
        }

        Printer.print_with_style('Usage:', color=GREEN)
        for key, action in keymap.items():
            Printer.print_with_style(f"  Type '{key}' to {action}")
