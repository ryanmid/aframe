from __future__ import annotations
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List

from journal import Journal
from journal_entry import JournalEntry


class BasePhase(object):
    """The base class encapsulating the common logic of a workflow Phase.

    Attributes:
        _name (str): A name or title for the phase instance
        _tasks (List): A list of unrelated tasks to perform during the execution of the phase instance
        _next_phase (BasePhase): The next phase to execute once all of the tasks in the phase instance have completed
    """

    def __init__(self, name: str):
        """Constructs a new BasePhase instance.

        Args:
            name (str): The name or title to give to the phase instance
        """
        self._name = name
        self._tasks = []
        self._next_phase = None

    def add_task(self, task: Callable[[Journal], List[JournalEntry]]):
        """Adds a task (function) to the phase."""
        self._tasks.append(task)

    def set_next_phase(self, phase: BasePhase):
        """Sets the next phase to execute after all of the tasks in the phase instance have completed."""
        self._next_phase = phase

    def get_next_phase(self):
        """Returns the phase that will be executed after all of the tasks in the phase instance have completed."""
        return self._next_phase

    @abstractmethod
    def run(self, journal: Journal):
        """Method that each specific phase type must implement for running each task in the phase instance.

        Args:
            journal (Journal): The journal instance to give to each task and into which to record the task results
        """
        pass


class SequentialPhase(BasePhase):
    """A type of phase that will execute each contained task one-after-another."""

    def __init__(self, name: str):
        """Constructs a new SequentialPhase instance.

        Args:
            name (str): The name or title to give to the phase instance
        """
        super().__init__(name)

    def run(self, journal: Journal):
        """Runs each task in the phase instance one-after-another.

        Args:
            journal (Journal): The journal instance to give to each task and into which to record the task results
        """
        for task in self._tasks:
            entries = task(journal)
            for entry in entries:
                journal.add_entry(entry)


class ThreadedPhase(BasePhase):
    """A type of phase that will execute the contained tasks concurrently in a threadpool.

    Args:
        name (str): The
    """

    def __init__(self, name: str, max_threads=0):
        """Constructs a new ThreadedPhase instance.

        Args:
            name (str): The name or title to give to the phase instance
            max_threads (int): The maximum number of threads in the threadpool, 0 will create a pool the size of the
                total number of tasks in the phase instance
        """
        super().__init__(name)
        self.max_threads = max_threads

    def run(self, journal: Journal):
        """Runs the tasks in the phase instance concurrently with a threadpool.

        Args:
            journal (Journal): The journal instance to give to each task and into which to record the task results
        """
        num_threads = self.max_threads or len(self._tasks)
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(task, journal) for task in self._tasks]
            new_entries = [future.result() for future in futures]

        for entries in new_entries:
            for entry in entries:
                journal.add_entry(entry)
