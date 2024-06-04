from che.intercept.interceptor import Interceptor
from che.intercept.request import Request
from che.utils import get_json_files, write_to_json_file


class VoteInterceptor(Interceptor):
    def process(self, request: Request):
        prompt = request.conversation.prompt
        if prompt == "vote:good" or prompt == "vote:bad":
            conversations = get_json_files()
            conversations[-1]["rating"] = "***" if prompt == "vote:good" else "*"
            write_to_json_file(conversations)
            request.conversation.prompt = "ignore"
        return request
