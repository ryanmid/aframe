from random import random
from typing import List
from aframe.jobs.journal import Journal, JournalEntry
from aframe.tasks.base import BaseTask
import time

class Printer(BaseTask):

    def __init__(self):
        super().__init__('printer', requires=[])

    @staticmethod
    def _print_entry(entry: JournalEntry):
        print(f'{entry.timestamp}: [{entry.tag}] {entry.data}')

    def run(self, journal: Journal) -> List[JournalEntry]:
        print(f'Workflow ID: {journal.get_workflow_id()}')

        entries = journal.get_entries()
        output = [f'{entry.timestamp}: [{entry.tag}] {entry.data}' for entry in entries]
        print('\n'.join(output))

        return []
