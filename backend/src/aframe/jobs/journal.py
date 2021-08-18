from typing import List
from uuid import uuid4
from aframe.jobs.journal_entry import JournalEntry


class Journal(object):
    """

    """

    def __init__(self):
        self._workflowId = self._get_uuid()
        self._entries = {}

    @staticmethod
    def _get_uuid() -> str:
        return str(uuid4())

    def get_workflow_id(self) -> int:
        return self._workflowId

    def add_entry(self, tag: str, data: any) -> None:
        self._entries[tag] = JournalEntry(tag, data)

    def is_provided(self, tag: str) -> bool:
        return tag in self._entries

    def get_available_tags(self) -> List[str]:
        return list(self._entries.keys())

    def get_entry(self, tag) -> JournalEntry:
        return self._entries[tag]

    def get_entries(self) -> List[JournalEntry]:
        return list(self._entries.values())

