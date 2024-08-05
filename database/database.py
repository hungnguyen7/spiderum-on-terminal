from tinydb import TinyDB, Query

class Database:
    def __init__(self, db_path='database/db.json'):
        self.db = TinyDB(db_path)

    def insert_post(self, slug):
        if self.db.contains(Query().slug == slug):
            return
        self.db.insert({'slug': slug, 'read': False})

    def mark_post_as_read(self, slug):
        self.db.update({'read': True}, Query().slug == slug)

    def is_post_read(self, slug):
        return self.db.get(Query().slug == slug)['read']
