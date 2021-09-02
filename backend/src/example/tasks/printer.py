from typing import List
from journal import Journal, JournalEntry
from task import task


def _print_entry(entry: JournalEntry):
    print(f'{entry.timestamp}: [{entry.tag}] {entry.data}')


@task(requirements=[])
def printer(journal: Journal) -> List[JournalEntry]:
    """A task that prints all of the journal entries in the workflow journal."""

    print(f'Workflow ID: {journal.get_workflow_id()}')

    entries = journal.get_entries()
    output = [f'{entry.timestamp}: [{entry.tag}] {entry.data}' for entry in entries]
    print('\n'.join(output))

    return []
