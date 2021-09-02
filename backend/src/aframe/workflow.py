from journal import Journal


class Workflow:
    """A workflow class that manages the phases and tasks of executing a job.

    Attributes:
        tasks (dict): A dictionary of tasks belonging to the workflow
        phases (dict): A dictionary of phases belonging to the workflow
        registry (dict): A dictionary of task and phase types belonging to the workflow
    """

    def __init__(self):
        """Creates a new workflow instance."""
        self.tasks = {}
        self.phases = {}
        self.registry = {
            'task_types': {},
            'phase_types': {}
        }

    def load_spec(self, spec: dict, registry: dict):
        """Loads a workflow specification and registry of dependencies and constructs a runnable workflow.

        Args:
            spec (dict): A specification of the ordered phases and corresponding tasks for a workflow
            registry (dict): A registry of phase and task dependencies for the spec
        """

        # Instantiate the underlying workflow intance __dict__ with the provided workflow spec
        self.__dict__ = {**self.__dict__, **spec}

        # Associate the workflow task specs with the corresponding tasks in the dependency registry
        for task_id, task in self.tasks.items():
            task_type = task['type']
            task_fn = registry[task_type]
            task['function'] = task_fn

        # Associate the workflow phase specs with the corresponding phases in the dependency registry
        for phase_id, phase in self.phases.items():
            phase_name = phase['name']
            phase_type = phase['type']
            phase_class = registry[phase_type]
            phase['instance'] = phase_class(phase_name)

            # Connect phases to the associated tasks as specified in the spec
            task_ids = phase['tasks']
            for task_id in task_ids:
                task = self.tasks[task_id]['function']
                phase['instance'].add_task(task)

        # Connect the phases according to the ordering in the spec
        for phase_id, phase in self.phases.items():
            next_phase_id = phase['next']
            next_phase = self.phases[next_phase_id]['instance'] if next_phase_id else None
            phase['instance'].set_next_phase(next_phase)

    def run(self):
        """Run the workflow instance, recording data in a journal instance at every phase."""

        journal = Journal()
        current_phase = self.phases[self.start_phase]['instance']
        while current_phase is not None:
            current_phase.run(journal)
            current_phase = current_phase.get_next_phase()
