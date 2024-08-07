from tinydb import TinyDB, Query

class Database:
    def __init__(self, db_path='database/db.json', page_index_db='database/page_index_db.json'):
        self.db = TinyDB(db_path)
        self.page_index_db = TinyDB(page_index_db)

    def insert_post(self, slug):
        if self.db.contains(Query().slug == slug):
            return
        self.db.insert({'slug': slug, 'read': False})

    def mark_post_as_read(self, slug):
        self.db.update({'read': True}, Query().slug == slug)

    def is_post_read(self, slug):
        return self.db.get(Query().slug == slug)['read']

    def upsert_page_index(self, page_index):
        # Upsert the page index into the database
        self.page_index_db.upsert({'page_index': page_index}, Query().page_index.exists())

    def get_page_index(self):
        # Retrieve the page index from the database, default to None if not found
        result = self.page_index_db.get(Query().page_index.exists())
        return result.get('page_index') if result else None