import asyncio
from src.core.aframe import App, Message
from src.example.components import AddOneComponent, PrintComponent

class DemoApp(App):
    """

    """

    def __init__(self):
        super().__init__()

    def run(self):
        first_connector_id = list(self.connectors.keys())[0]
        entry_connector = self.connectors[first_connector_id]['obj']
        asyncio.run(entry_connector.receive(Message(message_type='number', data=[12])))


if __name__ == '__main__':
    try:
        app = DemoApp()
        app.register_classes([
            ('AddOneComponent', AddOneComponent),
            ('PrintComponent', PrintComponent)
        ])
        app.compose(architecture_filename='./data/demo2.json')
        app.run()

    except Exception as e:
        print(e)
