import json
import os
import subprocess

from che.intercept.conversation import Conversation


class SharedValues:
    WORKSPACE = ""

    @staticmethod
    def change_workspace(src: str):
        SharedValues.WORKSPACE = src


__AUTHOR_NAME = subprocess.run(["git", "config", "user.name"], capture_output=True).stdout.decode("utf-8").strip()
__SAMPLE_MD = os.path.join(os.path.dirname(__file__), "sample.md")
__CURRENT_BRANCH = subprocess.run(["git", "branch", "--show-current"], capture_output=True).stdout.decode(
    "utf-8").strip().replace("/", "-")
__PREF_DIR = "ai/copilot"


def create_or_open_file(file_path, mode):
    directory, filename = os.path.split(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            ext = os.path.splitext(filename)[1]
            if ext == ".json":
                f.write("[]")
            else:
                f.write("")
    return open(file_path, mode)


def get_output_dir():
    return os.path.join(SharedValues.WORKSPACE, __PREF_DIR)


def create_md_block_from_sample(conversation: Conversation) -> str:
    with create_or_open_file(__SAMPLE_MD, "r") as f:
        block = f.readlines()
        block = "".join(block)
        block = block.replace("{{author_name}}", __AUTHOR_NAME)
        block = block.replace("{{prompt}}", conversation.prompt)
        block = block.replace("{{answer}}", conversation.answer)
        block = block.replace("{{rating}}", conversation.rating)
    return block


def create_md_file(conversations: dict):
    output_file = os.path.join(get_output_dir(), __CURRENT_BRANCH + ".md")
    block = "# " + __CURRENT_BRANCH + "\n\n"
    for c in conversations:
        block += create_md_block_from_sample(Conversation.from_dict(c))
    with create_or_open_file(output_file, "w") as f:
        f.write(block)


def get_json_files():
    output_file = os.path.join(get_output_dir(), __CURRENT_BRANCH + ".json")
    with create_or_open_file(output_file, "r") as f:
        conversations = json.load(f)
    return conversations


def write_to_json_file(conversations: dict):
    output_file = os.path.join(get_output_dir(), __CURRENT_BRANCH + ".json")
    with create_or_open_file(output_file, "w") as f:
        json.dump(conversations, f, indent=2, default=str, ensure_ascii=False)
