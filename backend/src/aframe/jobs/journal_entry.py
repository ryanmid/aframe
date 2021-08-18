from datetime import datetime


class JournalEntry(object):
    """

    """

    @staticmethod
    def _get_timestamp() -> datetime:
        return datetime.utcnow()

    def __init__(self, tag: str, data: any):
        self.timestamp = self._get_timestamp()
        self.tag = tag
        self.data = data
