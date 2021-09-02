from datetime import datetime


class JournalEntry(object):
    """A journal entry with a title (tag) and other associated information.

    Attributes:
        timestamp (datetime): The timestamp of when the journal entry was created
        tag (str): The title of the journal entry
        data (any): The journal entry payload associated with the specified title
    """

    @staticmethod
    def _new_timestamp() -> datetime:
        """Return the current timestamp in UTC"""
        return datetime.utcnow()

    def __init__(self, tag: str, data: any):
        """Constructs a new journal entry instance

        Args:
            tag (str): The title to give the journal entry
            data (any): The payload of the journal entry
        """
        self.timestamp = self._new_timestamp()
        self.tag = tag
        self.data = data
