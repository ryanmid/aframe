from exceptions.unmet_requirement import UnmetRequirementException
from concurrent.futures import ThreadPoolExecutor
from aframe.jobs.journal import Journal
from aframe.phases.base import BasePhase


class ThreadedPhase(BasePhase):

    def __init__(self, name: str, max_threads=0):
        super().__init__(name)
        self.max_threads = max_threads

    def run(self, journal: Journal):
        try:
            provided_entries = journal.get_available_tags()
            matching_tasks = list(filter(
                lambda task: all(requirement in provided_entries for requirement in task.get_requirements()),
                self._tasks
            ))

            num_threads = self.max_threads or len(matching_tasks)
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(task.run, journal) for task in matching_tasks]
                new_entries = [future.result() for future in futures]

            for entries in new_entries:
                for entry in entries:
                    journal.add_entry(entry)

        except UnmetRequirementException:
            import traceback
