from typing import Protocol

class ProcessMessage(Protocol):
    def process(self, str)->None:
        """ processes incoming message """
