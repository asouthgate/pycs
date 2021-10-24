from abc import ABC, abstractmethod

class ResourceABC:

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self):
        pass
