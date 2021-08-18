from aframe.jobs.journal import Journal


class Workflow:
    def __init__(self):
        self.tasks = {}
        self.phases = {}
        self.registry = {
            'task_types': {},
            'phase_types': {}
        }

    def load_spec(self, spec: dict, registry: dict):
        self.__dict__ = {**self.__dict__, **spec}

        # Create tasks
        for task_id, task in self.tasks.items():
            task_type = task['type']
            task_class = registry[task_type]
            task['instance'] = task_class()

        # Create phases
        for phase_id, phase in self.phases.items():
            phase_name = phase['name']
            phase_type = phase['type']
            phase_class = registry[phase_type]
            phase['instance'] = phase_class(phase_name)

            # Connect phase to tasks in the phase
            task_ids = phase['tasks']
            for task_id in task_ids:
                task = self.tasks[task_id]['instance']
                phase['instance'].add_task(task)

        # Sequence phases
        for phase_id, phase in self.phases.items():
            next_phase_id = phase['next']
            next_phase = self.phases[next_phase_id]['instance'] if next_phase_id else None
            phase['instance'].set_next_phase(next_phase)

    def run(self):
        journal = Journal()
        current_phase = self.phases[self.start_phase]['instance']
        while current_phase is not None:
            current_phase.run(journal)
            current_phase = current_phase.get_next_phase()
