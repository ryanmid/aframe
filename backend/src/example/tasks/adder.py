from typing import List
from aframe.jobs.journal import Journal, JournalEntry
from aframe.tasks.base import BaseTask


class Adder(BaseTask):

    def __init__(self):
        super().__init__('adder', requires=['x', 'y'])

    def run(self, journal: Journal) -> List[JournalEntry]:
        x = journal.get_entry('x').data
        y = journal.get_entry('y').data
        return [JournalEntry('x+y', x+y)]
