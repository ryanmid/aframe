import json
import importlib
import inspect
from aframe.phases.default import DefaultPhase
from workflow import Workflow


def run_example():
    phases_module = importlib.import_module('phases')
    phase_types = inspect.getmembers(phases_module, inspect.isclass)
    phase_type_mappings = {key: value for key, value in phase_types}

    tasks_module = importlib.import_module('tasks')
    task_types = inspect.getmembers(tasks_module, inspect.isclass)
    task_type_mappings = {key: value for key, value in task_types}

    all_type_mappings = {** phase_type_mappings, **task_type_mappings}

    workflow = Workflow()
    with open('data/example1.json', 'r') as spec_file:
        spec_str = spec_file.read()
        spec = json.loads(spec_str)
        workflow.load_spec(spec, all_type_mappings)
    workflow.run()


if __name__ == '__main__':
    run_example()
