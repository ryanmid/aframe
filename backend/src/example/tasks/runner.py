from typing import List
from journal import Journal, JournalEntry
from task import task


@task(requirements=[])
def runner(journal: Journal) -> List[JournalEntry]:
    """A task that always runs and returns new 'x' and 'y' journal entries with values 10 and 20 respectively."""

    return [
        JournalEntry(tag='x', data=10),
        JournalEntry(tag='y', data=20)
    ]
