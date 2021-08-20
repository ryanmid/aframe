from __future__ import annotations
from abc import abstractmethod

from aframe.jobs.journal import Journal
from aframe.tasks.base import BaseTask
from jobs.journal_entry import JournalEntry


class BasePhase(object):

    def __init__(self, name: str):
        self._name = name
        self._tasks = []
        self._next_phase = None

    def add_task(self, task: BaseTask):
        self._tasks.append(task)

    def set_next_phase(self, phase: BasePhase):
        self._next_phase = phase

    def get_next_phase(self):
        return self._next_phase

    @abstractmethod
    def run(self, journal: Journal):
        pass
