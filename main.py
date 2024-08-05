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

    def run(self):
        self.fetch_and_display_posts()
        while True:
            ans = input("Select a post to read (N to next page, P to previous page, L to show list, X to exit): ").strip().upper()
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
            elif ans == 'L':
                PostDisplay.show_list_posts(self.posts, self.db)
            elif ans.isdigit() and 0 <= int(ans) < len(self.posts):
                slug = self.posts[int(ans) - 1]['slug']
                self.db.mark_post_as_read(slug)
                post_content = SpiderumAPI.fetch_post_content(slug)
                PostDisplay.display_post_content(post_content)
            else:
                Printer.print_with_style("Invalid input. Please try again.", color=RED)

    def fetch_and_display_posts(self):
        self.posts = SpiderumAPI.fetch_posts(self.current_page)
        for post in self.posts:
            self.db.insert_post(post['slug'])
            
        PostDisplay.show_list_posts(self.posts, self.db)

if __name__ == '__main__':
    app = SpiderumApp()
    app.run()
