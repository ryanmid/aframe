class AddOneService(object):
    """

    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def add_one(value: float) -> float:
        return value + 1


class PrintService(object):
    """

    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def print(message: str):
        print(message)
