from __future__ import annotations

import asyncio
import json
from abc import abstractmethod
from typing import List, Any, Union, Dict, Tuple


class Message(object):
    """

    """

    def __init__(self, message_type: str, params: List[Any] = None, data: List[Any] = None):
        self.message_type = message_type
        self.params = params
        self.data = data


class Component(object):
    """

    """

    def __init__(self):
        self.components = []

    def connect(self, connector: Connector):
        self.components.append(connector)

    @staticmethod
    def accepts(message_types: Union[str, List[str]]):
        """

        :param message_types:
        :return:
        """

        message_types = message_types if type(message_types) == list else [message_types]

        def decorator(component_class: Component):
            class WrapperComponent(component_class):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                async def receive(self, message: Message):
                    if message.message_type in message_types:
                        await super().receive(message)

            return WrapperComponent
        return decorator

    @abstractmethod
    async def emit(self, message: Message):
        pass

    @abstractmethod
    async def receive(self, message: Message):
        pass


class Connector(Component):
    """

    """

    def __init__(self):
        super().__init__()
        self.bridges = []
        self.messages = []

    def connect(self, component: Component):
        self.components.append(component)

    def bridge(self, connector: Connector):
        self.bridges.append(connector)

    @abstractmethod
    async def emit(self, message: Message):
        pass

    @abstractmethod
    async def receive(self, message: Message):
        pass


class DefaultComponent(Component):

    async def emit(self, message: Message):
        await asyncio.gather(*(component.receive(message) for component in self.components))

    @abstractmethod
    async def receive(self, message: Message):
        pass


class DefaultConnector(Connector):
    """

    """

    def __init__(self):
        super().__init__()

    async def emit(self, message: Message):
        await asyncio.gather(*(component.receive(message) for component in self.components + self.bridges))

    async def receive(self, message: Message):
        await self.emit(message)


class App(object):
    """

    """

    def __init__(self):
        self.connectors = {}
        self.components = {}
        self.classes = {}

        self.register_class('DefaultConnector', DefaultConnector)

    @staticmethod
    def _load_json_file(filename: str) -> str:
        with open(filename, 'r') as json_file:
            json_data = json_file.read()
        return json_data

    def _convert_json(self, json_data: str) -> str:
        components = {}
        connectors = {}
        converted = {}

        arch = json.loads(json_data)

        for node in arch['nodes']:
            converted_id = str(node['id'])
            converted_type = node['type']
            converted_node = {
                'name': node['title'],
                'className': node['title'],
                'connections': []
            }
            if converted_type == 'arch/connector':
                converted_node['bridges'] = []

            if converted_type == 'arch/connector':
                connectors[converted_id] = converted_node
            else:
                components[converted_id] = converted_node

        for link in arch['links']:
            link_id, src_id, src_port, dst_id, dst_port, src_type = link
            src_id = str(src_id)
            dst_id = str(dst_id)
            dst_type = 'component' if dst_id in components else 'connector'

            if src_type == 'component':
                components[src_id]['connections'].append(dst_id)
            else:
                if dst_type == 'connector':
                    connectors[src_id]['bridges'].append(dst_id)
                else:
                    connectors[src_id]['connections'].append(dst_id)

        converted = {
            'connectors': connectors,
            'components': components
        }

        return json.dumps(converted)

    def register_classes(self, classes: List[Tuple[str, type]]):
        for entry in classes:
            name, cls = entry
            self.register_class(name, cls)

    def register_class(self, name: str, cls: type):
        self.classes[name] = cls

    def compose(self, architecture_filename: str = None, architecture_json: str = None):

        if architecture_filename:
            architecture_json = self._load_json_file(architecture_filename)
            architecture_json = self._convert_json(architecture_json)

        elif not architecture_json:
            architecture_json = '{}'

        # Load architecture instance from file
        architecture = json.loads(architecture_json)
        components = architecture['components']
        connectors = architecture['connectors']

        # Create component objects
        for component in components.values():
            name = component['className']
            if name in self.classes:
                component['obj'] = self.classes[name]()
            else:
                raise TypeError('Unknown class name: {}'.format(name))

        # Create connector objects
        for connector in connectors.values():
            name = connector['className']
            if name in self.classes:
                connector['obj'] = self.classes[name]()
            else:
                raise TypeError('Unknown class name: {}'.format(name))

        # Connect the components to connectors
        for component in components.values():
            for connection_id in component['connections']:
                component['obj'].connect(connectors[connection_id]['obj'])

        # Connect the connectors to components
        for connector in connectors.values():
            for connection_id in connector['connections']:
                connector['obj'].connect(components[connection_id]['obj'])

        # Connect (bridge) the connectors to connectors
        for connector in connectors.values():
            for connection_id in connector['bridges']:
                connector['obj'].bridge(connectors[connection_id]['obj'])

        self.components.update(components)
        self.connectors.update(connectors)

    @abstractmethod
    def run(self):
        pass
