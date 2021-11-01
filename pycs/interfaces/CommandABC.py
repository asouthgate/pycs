from abc import ABC, abstractmethod

class CommandABC(ABC):
    """ Interface for executed UI commands. 
    
    Command objects should be created with all the
    data they need to execute their functionality. 

    """

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass
