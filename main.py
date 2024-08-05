from api.api import SpiderumAPI
from database.database import Database
from display.post_display import PostDisplay
from utils.colors import RED, YELLOW, GREEN
from utils.printer import Printer
class SpiderumApp:
    def __init__(self):
        self.db = Database()
        self.current_page = 1
        self.posts = []
        self.enable_tts = False
        self.post_display = PostDisplay()

    def run(self):
        self.fetch_and_display_posts()
        while True:
            ans = input("Select a post to read, or type 'H' for help, or 'X' to exit: ").upper().strip()
            if ans == 'X':
                Printer.print_with_style("Goodbye!", color=GREEN)
                break
            elif ans == 'N':
                self.current_page += 1
                self.fetch_and_display_posts()
            elif ans == 'P':
                if self.current_page > 1:
                    self.current_page -= 1
                    self.fetch_and_display_posts()
                else:
                    Printer.print_with_style("This is the first page", color=YELLOW)
            elif ans == 'H':
                PostDisplay.show_help()
            elif ans == 'L':
                PostDisplay.show_list_posts(self.posts, self.db)
            elif ans == 'V':
                self.enable_tts = not self.enable_tts
                Printer.print_with_style(f"Text-to-speech is {'enabled' if self.enable_tts else 'disabled'}", color=YELLOW)
            elif ans.isdigit() and 0 <= int(ans) < len(self.posts):
                slug = self.posts[int(ans) - 1]['slug']
                self.db.mark_post_as_read(slug)
                post_content = SpiderumAPI.fetch_post_content(slug)
                self.post_display.display_post_content(post_content, self.enable_tts)
            else:
                Printer.print_with_style("Invalid input. Please try again.", color=RED)

    def fetch_and_display_posts(self):
        # * Warning in case text-to-speech is enabled
        if self.enable_tts:
            Printer.print_with_style("Warning: Text-to-speech is enabled.", color=YELLOW)
        self.posts = SpiderumAPI.fetch_posts(self.current_page)
        for post in self.posts:
            self.db.insert_post(post['slug'])
            
        PostDisplay.show_list_posts(self.posts, self.db)

if __name__ == '__main__':
    app = SpiderumApp()
    app.run()
