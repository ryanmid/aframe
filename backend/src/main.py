import asyncio
import json
from aframe import App, Message, DefaultConnector
from components import AddOneComponent, PrintComponent


class DemoApp(App):
    """

    """

    def __init__(self):
        super().__init__()

    def compose(self):
        with open('architecture.json', 'r') as architecture_file:
            architecture_json = architecture_file.read()

        # Load architecture instance from file
        architecture = json.loads(architecture_json)
        components = architecture['components']
        connectors = architecture['connectors']

        # Create component objects
        for component in components.values():
            component['obj'] = globals()[component['className']]()

        # Create connector objects
        for connector in connectors.values():
            connector['obj'] = globals()[connector['className']]()

        # Connect the components to connectors
        for component in components.values():
            for connection_id in component['connections']:
                component['obj'].connect(connectors[connection_id]['obj'])

        # Connect the connectors to components
        for connector in connectors.values():
            for connection_id in connector['connections']:
                connector['obj'].connect(components[connection_id]['obj'])

        self.components.update(components)
        self.connectors.update(connectors)

    def run(self):
        entry_connector = self.connectors["0"]['obj']
        asyncio.run(entry_connector.receive(Message(message_type='number', data=[12])))


if __name__ == '__main__':
    try:
        app = DemoApp()
        app.run()

    except Exception as e:
        print(e)
