from typing import List
from journal import Journal, JournalEntry
from task import task


@task(requirements=[
    lambda journal: journal.has_entry('x'),
    lambda journal: journal.has_entry('y')
])
def adder(journal: Journal) -> List[JournalEntry]:
    """A task that requires previous phases to have recorded journal entres with tags 'x' and 'y', which it will sum.

    Returns a new journal entry, titled 'x+y', containing the sum of the existing journal entries 'x' and 'y'
    """

    x = journal.get_entry('x').data
    y = journal.get_entry('y').data
    return [JournalEntry('x+y', x + y)]
