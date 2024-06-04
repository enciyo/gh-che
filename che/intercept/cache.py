from che.intercept.interceptor import Interceptor
from che.intercept.request import Request
from che.utils import get_json_files, write_to_json_file


class CacheInterceptor(Interceptor):
    def process(self, request: Request):
        conversations = get_json_files()
        if request.conversation.prompt != "ignore":
            conversations.append(request.conversation.to_dict())
            print("Cache updated")

        write_to_json_file(conversations)

        return request
