from che.intercept.cache import CacheInterceptor
from che.intercept.markdown import MarkdownInterceptor
from che.intercept.vote import VoteInterceptor
from che.intercept.request import Request

class InterceptorChain:
    def __init__(self):
        self.interceptors = [
            VoteInterceptor(),
            CacheInterceptor(),
            MarkdownInterceptor()
        ]

    def execute(self, request: Request):
        try:
            for interceptor in self.interceptors:
                request = interceptor.process(request)
        except RuntimeError:
            pass
