from abc import ABC, abstractmethod

class JSONStorage(ABC):
    @abstractmethod
    def save(self, record) -> None: ...

    @abstractmethod
    def read(self) -> dict | list: ...

    @abstractmethod
    def write(self, records) -> None: ...

    @abstractmethod
    def delete(self, index: int) -> None: ...
