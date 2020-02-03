
class State:

    def __init__(self) -> None:
        self.values = {}
        self.achievements = {
            'rescued': 0
        }
        self.finished = []

    values: dict
    achievements: dict
    finished: list
