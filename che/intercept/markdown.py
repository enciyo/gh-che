from che.intercept.interceptor import Interceptor
from che.intercept.request import Request
from che.utils import get_json_files, create_md_file


class MarkdownInterceptor(Interceptor):
    def process(self, request: Request):
        conversations = get_json_files()
        create_md_file(conversations)
        return request
