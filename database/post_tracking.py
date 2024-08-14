from database.base_connection import BaseConnection

class PostTracking(BaseConnection):
    """
    This class is responsible for managing the post_tracking collection.
    It provides methods to insert, mark as read and check if a post is read.
    
    Attributes:
        collection_name (str): the name of the collection
    """
    def __init__(self):
        super().__init__(collection_name='post_tracking')
        
    def insert_post(self, slug):
        """
        Insert a post in the post_tracking collection.
        
        Args:
            slug (str): the slug of the post
            
        Returns:
            None
        """
        if not self.collection.contains(self.query.slug == slug):
            self.collection.insert({'slug': slug, 'read': False})

    def mark_post_as_read(self, slug):
        """
        Mark a post as read in the post_tracking collection.
        
        Args:
            slug (str): the slug of the post
            
        Returns:
            None
        """
        self.collection.update({'read': True}, self.query.slug == slug)

    def is_post_read(self, slug):
        """
        Check if a post is read in the post_tracking collection.
        
        Args:
            slug (str): the slug of the post
        
        Returns:
            bool: True if the post is read, False otherwise
        """
        post = self.collection.get(self.query.slug == slug)
        return post['read'] if post else False
