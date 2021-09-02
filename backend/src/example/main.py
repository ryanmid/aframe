import json
import importlib
import inspect
from aframe.phases import SequentialPhase, ThreadedPhase
from aframe.workflow import Workflow
from tasks import adder, printer, runner

def run_example():
    phase_mappings = {
        'SequentialPhase': SequentialPhase,
        'ThreadedPhase': ThreadedPhase
    }

    task_mappings = {
        'adder': adder,
        'printer': printer,
        'runner': runner
    }

    all_mappings = {** phase_mappings, **task_mappings}

    workflow = Workflow()
    with open('data/example1.json', 'r') as spec_file:
        spec_str = spec_file.read()
        spec = json.loads(spec_str)
        workflow.load_spec(spec, all_mappings)
    workflow.run()


if __name__ == '__main__':
    run_example()
