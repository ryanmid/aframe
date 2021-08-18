from exceptions.unmet_requirement import UnmetRequirementException
from aframe.jobs.journal import Journal
from aframe.phases.base import BasePhase


class DefaultPhase(BasePhase):

    def __init__(self, name: str):
        super().__init__(name)

    def run(self, journal: Journal):
        try:

            for task in self._tasks:
                requirements = task.get_requirements()
                provided = journal.get_available_tags()
                if all(requirement in provided for requirement in requirements):
                    task.run(journal)

        except UnmetRequirementException:
            import traceback
