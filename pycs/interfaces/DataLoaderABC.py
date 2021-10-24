from abc import ABC, abstractmethod

class DataLoaderABC(ABC):
    
    @abstractmethod
    def get(self, s):
        pass
