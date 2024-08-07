from api.api import SpiderumAPI
from database.database import Database
from utils.post_display import PostDisplay
from utils.colors import RED, YELLOW, GREEN
from utils.printer import Printer
from utils.save_post_to_file import save_post_to_file

class SpiderumApp:
    def __init__(self):
        self.db = Database()
        self.post_display = PostDisplay()
        self.posts = []
        self.enable_tts = False
        self.show_image = False
        self.selected_post_index = None

    def run(self):
        self.fetch_and_display_posts()
        
        while True:
            ans = input("Select a post to read, or type 'H' for help, or 'X' to exit: ").upper().strip()
            if ans == 'X':
                self.exit_app()
                break
            elif ans == 'N':
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
                Printer.print_with_style("Invalid input. Please try again.", color=RED)

    def fetch_and_display_posts(self):
        if self.enable_tts:
            Printer.print_with_style("Warning: Text-to-speech is enabled.", color=YELLOW)
        if self.show_image:
            Printer.print_with_style("Warning: Image is enabled.", color=YELLOW)
            
        # * Get the current page index from the database
        page_index = self.db.get_page_index()
        
        # * If page index is not set, set it to 1
        if not page_index:
            page_index = 1
            self.db.upsert_page_index(page_index)
        
        self.posts = SpiderumAPI.fetch_posts(page_index)
        # * Insert posts into database, if not already
        for post in self.posts:
            self.db.insert_post(post['slug'])
            
        self.show_list_posts()

    def exit_app(self):
        Printer.print_with_style("Goodbye!", color=GREEN)

    def next_page(self):
        page_index = self.db.get_page_index()
        page_index += 1
        self.db.upsert_page_index(page_index)
        self.fetch_and_display_posts()

    def previous_page(self):
        if self.db.get_page_index() > 1:
            page_index = self.db.get_page_index() - 1
            self.db.upsert_page_index(page_index)
            self.fetch_and_display_posts()
        else:
            Printer.print_with_style("This is the first page", color=YELLOW)

    def first_page(self):
        page_index = 1
        self.db.upsert_page_index(page_index)
        self.fetch_and_display_posts()
        
    def show_help(self):
        self.post_display.show_help()

    def show_list_posts(self):
        posts_with_status = []
        for post in self.posts:
            post['is_read'] = self.db.is_post_read(post['slug'])
            posts_with_status.append(post)
            
        self.post_display.show_list_posts(posts_with_status)

    def toggle_tts(self):
        self.enable_tts = not self.enable_tts
        Printer.print_with_style(f"Text-to-speech is {'enabled' if self.enable_tts else 'disabled'}", color=YELLOW)

    def toggle_image(self):
        self.show_image = not self.show_image
        Printer.print_with_style(f"Image is {'enabled' if self.show_image else 'disabled'}", color=YELLOW)

    def display_post(self, index):
        self.selected_post_index = index
        
        slug = self.posts[index]['slug']
        # * Mark post as read in database
        self.db.mark_post_as_read(slug)
        
        # * Fetch and display post content
        post_content = SpiderumAPI.fetch_post_content(slug)
        self.post_display.display_post_content(post_content, self.enable_tts, self.show_image)
        
    def mark_post_as_favorite(self):
        if self.selected_post_index is None:
            Printer.print_with_style("No post selected", color=RED)
            return
        
        post = self.posts[self.selected_post_index]
        save_post_to_file(post)
        
        

if __name__ == '__main__':
    app = SpiderumApp()
    app.run()
