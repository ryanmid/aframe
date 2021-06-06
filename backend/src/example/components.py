from ..core.aframe import Component, DefaultComponent, Message
from services import AddOneService, PrintService


@Component.accepts('number')
class AddOneComponent(AddOneService, DefaultComponent):
    """

    """

    def __init__(self):
        super().__init__()

    async def receive(self, message: Message):
        value = message.data[0]
        result = super().add_one(value)
        await self.emit(Message(message_type='number', data=[result]))


@Component.accepts(['number', 'string'])
class PrintComponent(PrintService, DefaultComponent):
    """

    """

    def __init__(self):
        super().__init__()

    async def receive(self, message: Message):
        value = message.data[0]
        print(value)
