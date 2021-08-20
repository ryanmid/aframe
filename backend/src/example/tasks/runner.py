from typing import List
from aframe.jobs.journal import Journal, JournalEntry
from aframe.tasks.base import BaseTask


class Runner(BaseTask):

    def __init__(self):
        super().__init__('runner', requires=[])

    def run(self, journal: Journal) -> List[JournalEntry]:
        return [
            JournalEntry(tag='x', data=10),
            JournalEntry(tag='y', data=20)
        ]
