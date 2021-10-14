from abc import ABC, abstractmethod


class Handler(ABC):
    """A Abstract handler interface"""

    @abstractmethod
    def to_base64_str(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError
