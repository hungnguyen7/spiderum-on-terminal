from api.api import SpiderumAPI
from database.page_tracking import PageTracking
from database.post_tracking import PostTracking
from utils.post_display import PostDisplay
from utils.colors import RED, YELLOW, GREEN
from utils.printer import Printer
from utils.save_post_to_file import save_post_to_file


class SpiderumApp:
    """
    Main class for the Spiderum app.

    Attributes:
        page_tracking(PageTracking): An instance of PageTracking class.
        post_tracking(PostTracking): An instance of PostTracking class.
        post_display(PostDisplay): An instance of PostDisplay class.
        posts(list): A list of posts.
        enable_tts(bool): A boolean value to enable or disable text-to-speech.
        show_image(bool): A boolean value to show or hide image.
        selected_post_index(int): The index of the selected post.

    """

    def __init__(self):
        self.page_tracking = PageTracking()
        self.post_tracking = PostTracking()
        self.post_display = PostDisplay()
        self.posts = []
        self.enable_tts = False
        self.show_image = False
        self.selected_post_index = None

    def run(self):
        """Run the Spiderum app."""
        self.fetch_and_display_posts()

        while True:
            ans = input(
                "Select a post to read, or type 'H' for help, or 'X' to exit: ").upper().strip()
            if ans == 'X':
                self.exit_app()
                break

            if ans == 'N':
                self.next_page()
            elif ans == 'P':
                self.previous_page()
            elif ans == 'F':
                self.first_page()
            elif ans == 'H':
                self.show_help()
            elif ans == 'L':
                self.show_list_posts()
            elif ans == 'V':
                self.toggle_tts()
            elif ans == 'I':
                self.toggle_image()
            elif ans == 'B':
                self.mark_post_as_favorite()
            elif ans.isdigit() and 0 < int(ans) <= len(self.posts):
                self.display_post(int(ans) - 1)
            else:
                Printer.print_with_style(
                    "Invalid input. Please try again.", color=RED)

    def fetch_and_display_posts(self):
        """Fetch and display posts from the Spiderum API."""
        if self.enable_tts:
            Printer.print_with_style(
                "Warning: Text-to-speech is enabled.", color=YELLOW)
        if self.show_image:
            Printer.print_with_style(
                "Warning: Image is enabled.", color=YELLOW)

        # * Get the current page index from the database
        page_index = self.page_tracking.get_page_index()

        # * If page index is not set, set it to 1
        if not page_index:
            page_index = 1
            self.page_tracking.upsert_page_index(page_index)

        self.posts = SpiderumAPI.fetch_posts(page_index)
        # * Insert posts into database, if not already
        for post in self.posts:
            self.post_tracking.insert_post(post['slug'])

        self.show_list_posts()

    def exit_app(self):
        """Exit the Spiderum app."""
        Printer.print_with_style("Goodbye!", color=GREEN)

    def next_page(self):
        """Go to the next page."""
        page_index = self.page_tracking.get_page_index()
        page_index += 1
        self.page_tracking.upsert_page_index(page_index)
        self.fetch_and_display_posts()

    def previous_page(self):
        """Go to the previous page."""
        if self.page_tracking.get_page_index() > 1:
            page_index = self.page_tracking.get_page_index() - 1
            self.page_tracking.upsert_page_index(page_index)
            self.fetch_and_display_posts()
        else:
            Printer.print_with_style("This is the first page", color=YELLOW)

    def first_page(self):
        """Go to the first page."""
        page_index = 1
        self.page_tracking.upsert_page_index(page_index)
        self.fetch_and_display_posts()

    def show_help(self):
        """Show help."""
        self.post_display.show_help()

    def show_list_posts(self):
        """Show a list of posts."""
        posts_with_status = []
        for post in self.posts:
            post['is_read'] = self.post_tracking.is_post_read(post['slug'])
            posts_with_status.append(post)

        self.post_display.show_list_posts(posts_with_status)

    def toggle_tts(self):
        """Toggle text-to-speech."""
        self.enable_tts = not self.enable_tts
        Printer.print_with_style(
            f"Text-to-speech is {'enabled' if self.enable_tts else 'disabled'}", color=YELLOW)

    def toggle_image(self):
        """Toggle show image."""
        self.show_image = not self.show_image
        Printer.print_with_style(
            f"Image is {'enabled' if self.show_image else 'disabled'}", color=YELLOW)

    def display_post(self, index):
        """Display a post."""
        self.selected_post_index = index

        slug = self.posts[index]['slug']
        # * Mark post as read in database
        self.post_tracking.mark_post_as_read(slug)

        # * Fetch and display post content
        post_content = SpiderumAPI.fetch_post_content(slug)
        self.post_display.display_post_content(
            post_content, self.enable_tts, self.show_image)

    def mark_post_as_favorite(self):
        """Mark a post as favorite."""
        if self.selected_post_index is None:
            Printer.print_with_style("No post selected", color=RED)
            return

        post = self.posts[self.selected_post_index]
        save_post_to_file(post)


if __name__ == '__main__':
    app = SpiderumApp()
    app.run()
