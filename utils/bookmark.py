import os
import json


def add_post_to_bookmarks(post):
    """Save a post to the bookmark list in the database folder."""
    try:
        file_path = os.path.join('database', 'bookmark.json')
        # * Ensure the directory exists
        os.makedirs('database', exist_ok=True)

        # * Load existing bookmarks
        bookmarks = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                bookmarks = json.load(file)

        # * Check if the post is already bookmarked
        for bookmark in bookmarks:
            if bookmark['slug'] == post['slug']:
                print("Post already bookmarked.")
                return
        # * Add the post to the bookmarks
        bookmarks.append({
            'title': post['title'],
            'url': f"https://spiderum.com/bai-dang/{post['slug']}",
            "slug": post["slug"],
        })
        # * Save the bookmarks
        with open(file_path, 'w') as file:
            json.dump(bookmarks, file, indent=4)
        print(f"Post saved to {file_path}")
    except Exception as e:
        print(
            f"Error: {e}. In the darkest depths of the codebase... an error was born. 🌑")


def list_bookmarks():
    """List all bookmarks in the database folder."""
    try:
        file_path = os.path.join('database', 'bookmark.json')
        if not os.path.exists(file_path):
            print("No bookmarks found.")
            return
        with open(file_path, 'r') as file:
            bookmarks = json.load(file)
            return bookmarks
    except Exception as e:
        print(
            f"Error: {e}. In the darkest depths of the codebase... an error was born. 🌑")
