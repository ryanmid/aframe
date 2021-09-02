from typing import List, Optional
from uuid import uuid4
from journal_entry import JournalEntry


class Journal(object):
    """A journal used to store parameters and values from each step of the execution of a job.

    Attributes:
        _workflowId (str): A string uniquely identifying a job
        _entries (dict): A dictionary of parameters and values related to steps performed executing a job
    """

    def __init__(self):
        """Constructs a new Journal instance."""
        self._workflowId: str = self._generate_uuid()
        self._entries: dict = {}

    @staticmethod
    def _generate_uuid() -> str:
        """ Returns a new UUID string value."""
        return str(uuid4())

    def get_workflow_id(self) -> str:
        """Returns the unique UUID of the journal."""
        return self._workflowId

    def add_entry(self, entry: JournalEntry) -> None:
        """Records an entry in the journal.

        Args:
            entry (JournalEntry): The entry to record in the journal
        """
        self._entries[entry.tag] = entry

    def has_entry(self, tag: str, value: any = None) -> bool:
        """Checks if the journal instance contains an entry with the specified tag and value.

        Args:
            tag (str): The entry name (tag) to check for in the journal instance
            value (any, optional): The value to check for in the journal entry with the specified tag

        Returns:
            True if there is a matching (tag: value) entry in the journal instance OR there is an entry with
                a matching tag and the given value argument is None
            False otherwise
        """
        if any is None:
            return tag in self._entries
        return tag in self._entries and self._entries[tag] == value

    def get_available_tags(self) -> List[str]:
        """Returns a list of the tags of all entries recorded in the journal instance."""
        return list(self._entries.keys())

    def get_entry(self, tag: str) -> Optional[JournalEntry]:
        """Returns the journal entry with the specified tag.

        Args:
            tag (str): The tag of the journal entry to return

        Returns:
            The journal entry with the specified tag, or None if no such entry exists in the journal instance
        """
        if tag in self._entries:
            return self._entries[tag]
        return None

    def get_entries(self) -> List[JournalEntry]:
        """Returns a list of all the journal entries in the journal instance"""
        return list(self._entries.values())

