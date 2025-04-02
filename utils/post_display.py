import re
from utils.printer import Printer
from utils.colors import GREEN, BLUE, PURPLE, RED, GRAY, CYAN, YELLOW
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
        Display the help menu in a beautifully formatted way.

        Returns:
            None
        """
        keymap = {
            'N': '➡️  Next stop: More articles! Keep the knowledge train rolling. 🚂',
            'P': '⬅️  Reverse! Let’s revisit what we left behind. 🕰️',
            'F': '🔝  Back to square one. Feels like a fresh start, huh?',
            'X': '🏃  Abort mission! Close the app and reclaim your life. 😆',
            'L': '📜  Behold! A grand list of all the articles at your service.',
            'V': '🗣️  Make the computer talk! Or shut it up—it’s your call.',
            'I': '🖼️  Show or hide images. A picture is worth a thousand words... or is it?',
            'U': '🌐  Warp through cyberspace! Enter a post URL to teleport. 🌀',
            'B': '⭐  Save this post to your legendary collection of bookmarks.',
            'BM': '📖  Open the vault of wisdom—your saved bookmarks!',
            'EB': '📂  Export bookmarks to a file. 🔑',
            'H': '🆘  Feeling lost? Call for help.',
            'Number Keys': '🔢  Pick a post by number—like ordering from a menu. 🍽️',
            '(B||b) + Number Keys': '🔖  Summon a bookmarked post with a number.',
        }

        border = "═" * 50
        Printer.print_with_style(f"\n{border}", color=GREEN)
        Printer.print_with_style(
            "📖 COMMANDS & SHORTCUTS 📖".center(50), color=CYAN)
        Printer.print_with_style(f"{border}", color=GREEN)

        for key, action in keymap.items():
            Printer.print_with_style(
                f"  {key.ljust(10)} ➜ {action}", color=YELLOW)

        Printer.print_with_style(f"{border}\n", color=GREEN)
