from database.base_connection import BaseConnection

class PageTracking(BaseConnection):
    """
    PageTracking class is used to interact with the page_tracking collection in the database.
    This collection is used to store the current page index of the user.
    """

    def __init__(self):
        super().__init__(collection_name='page_tracking')

    def upsert_page_index(self, page_index):
        """
        Upsert the page index into the database.

        Args:
            page_index (int): The page index to be upserted into the database.

        Returns:
            None
        """
        # Upsert the page index into the database
        self.collection.upsert({'page_index': page_index},
                               self.query.page_index.exists())

    def get_page_index(self):
        """
        Retrieve the page index from the database.

        Returns:
            int: The page index retrieved from the database, None if not found.
        """
        # Retrieve the page index from the database, default to None if not found
        result = self.collection.get(self.query.page_index.exists())
        return result.get('page_index') if result else None
