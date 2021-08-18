
class UnmetRequirementException(Exception):

    def __init__(self, requirement: str, task: str):
        super().__init__(f'Attempted to run \'${task}\' task on a job with unmet \'${requirement}\' requirement')
