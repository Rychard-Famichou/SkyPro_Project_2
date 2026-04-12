from abc import ABC, abstractmethod


class BaseApi(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass
