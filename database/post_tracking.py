from database.base_connection import BaseConnection

class PostTracking(BaseConnection):
    def __init__(self):
        super().__init__(collection_name='post_tracking')
        
    def insert_post(self, slug):
        if not self.collection.contains(self.query.slug == slug):
            self.collection.insert({'slug': slug, 'read': False})

    def mark_post_as_read(self, slug):
        self.collection.update({'read': True}, self.query.slug == slug)

    def is_post_read(self, slug):
        post = self.collection.get(self.query.slug == slug)
        return post['read'] if post else False
