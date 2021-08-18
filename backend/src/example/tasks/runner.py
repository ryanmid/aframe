from aframe.jobs.journal import Journal
from aframe.tasks.base import BaseTask


class Runner(BaseTask):

    def __init__(self):
        super().__init__('runner', requires=[])

    def run(self, journal: Journal):
        journal.add_entry('x', 10)
        journal.add_entry('y', 20)