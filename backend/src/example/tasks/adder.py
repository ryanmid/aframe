from aframe.jobs.journal import Journal
from aframe.tasks.base import BaseTask


class Adder(BaseTask):

    def __init__(self):
        super().__init__('adder', requires=['x', 'y'])

    def run(self, journal: Journal):
        x = journal.get_entry('x').data
        y = journal.get_entry('y').data
        journal.add_entry('z', x + y)