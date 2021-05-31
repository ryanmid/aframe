from __future__ import annotations

import asyncio
from abc import abstractmethod
from typing import List, Any, Union


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

    async def emit(self, message: Message):
        await asyncio.gather(*(component.receive(message) for component in self.components))


    @abstractmethod
    async def receive(self, message: Message):
        pass


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


class Connector(Component):
    """

    """

    def __init__(self):
        super().__init__()
        self.messages = []

    @abstractmethod
    def connect(self, component: Component):
        pass

    @abstractmethod
    async def receive(self, message: Message):
        pass


class DefaultConnector(Connector):
    """

    """

    def __init__(self):
        super().__init__()

    def connect(self, component: Component):
        self.components.append(component)

    async def receive(self, message: Message):
        await self.emit(message)


class App(object):
    """

    """

    def __init__(self):
        self.connectors = {}
        self.components = {}
        self.compose()

    @abstractmethod
    def compose(self):
        pass

    @abstractmethod
    def run(self):
        pass
