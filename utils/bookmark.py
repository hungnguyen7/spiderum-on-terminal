import os


def save_post_to_file(post):
    """Save a post to a text file in the 'favorite_posts' directory."""
    # Ensure the directory exists
    os.makedirs('favorite_posts', exist_ok=True)
    # # Define the content to save
    content = f"""
Title: {post["title"]}
Description: {post["description"]}
Link: https://spiderum.com/bai-dang/{post["slug"]}
    """

    # Create a safe filename by replacing any potentially problematic characters in the slug
    safe_slug = post["slug"].replace('/', '_').replace('\\', '_')

    # Save to file
    file_path = os.path.join('favorite_posts', f'{safe_slug}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Post saved to {file_path}")
