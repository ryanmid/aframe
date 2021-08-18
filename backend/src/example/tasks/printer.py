from aframe.jobs.journal import Journal
from aframe.jobs.journal_entry import JournalEntry
from aframe.tasks.base import BaseTask


class Printer(BaseTask):

    def __init__(self):
        super().__init__('printer', requires=[])

    @staticmethod
    def _print_workflow_id(journal: Journal):
        print(f'Workflow ID: {journal.get_workflow_id()}')

    @staticmethod
    def _print_entry(entry: JournalEntry):
        print(f'{entry.timestamp}: [{entry.tag}] {entry.data}')

    def run(self, journal: Journal):
        self._print_workflow_id(journal)
        entries = journal.get_entries()
        for entry in entries:
            self._print_entry(entry)