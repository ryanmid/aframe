import json
from aframe.phases.default import DefaultPhase
from example.tasks.adder import Adder
from example.tasks.printer import Printer
from example.tasks.runner import Runner
from workflow import Workflow


def run_example():
    workflow = Workflow()
    with open('data/example1.json', 'r') as spec_file:
        spec_str = spec_file.read()
        spec = json.loads(spec_str)
        workflow.load_spec(spec, {
            'Runner': Runner,
            'Adder': Adder,
            'Printer': Printer,
            'DefaultPhase': DefaultPhase
        })
    workflow.run()


if __name__ == '__main__':
    run_example()
