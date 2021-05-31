from aframe import *
from services import *


@accepts('number')
class AddOneComponent(AddOneService, Component):
    """

    """

    def __init__(self):
        super().__init__()

    async def receive(self, message: Message) -> None:
        value = message.data[0]
        result = super().add_one(value)
        await self.emit(Message(message_type='number', data=[result]))


@accepts(['number', 'string'])
class PrintComponent(PrintService, Component):
    """

    """

    def __init__(self):
        super().__init__()

    async def receive(self, message: Message) -> None:
        value = message.data[0]
        print(value)
