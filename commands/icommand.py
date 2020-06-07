from abc import ABC


class ICommand(ABC):
    def get_representation(self):
        raise NotImplementedError()
