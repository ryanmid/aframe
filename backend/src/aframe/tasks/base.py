from abc import abstractmethod
from typing import List

from aframe.exceptions.unmet_requirement import UnmetRequirementException
from aframe.jobs.journal import Journal, JournalEntry


class BaseTask(object):

    def __init__(self, name: str, requires: List[str]):
        self.name = name
        self.requires = requires

    def _validate_requirements(self, journal: Journal):
        for requirement in self.requires:
            if not journal.is_provided(requirement):
                raise UnmetRequirementException(requirement, self.name)

    def get_requirements(self) -> List[str]:
        return self.requires

    @abstractmethod
    def run(self, journal: Journal) -> List[JournalEntry]:
        pass
