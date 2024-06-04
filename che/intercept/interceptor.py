from abc import ABC, abstractmethod

from che.intercept.request import Request


class Interceptor(ABC):
    @abstractmethod
    def process(self, request: Request) -> Request:
        pass
