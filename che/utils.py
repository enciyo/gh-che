import json
import os
import stat
import subprocess

from che.intercept.conversation import Conversation

__SAMPLE_MD = os.path.join(os.path.dirname(__file__), "sample.md")
__PREF_DIR = "ai/copilot"


def give_permission(file_path):
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)


def __author_name():
    path = os.path.join(get_config()["project_path"])
    return subprocess.run(
        f"cd {path} && git config user.name",
        capture_output=True,
        shell=True,
        check=True
    ).stdout.decode("utf-8").strip()


def __current_branch():
    path = os.path.join(get_config()["project_path"])
    return subprocess.run(
        f"cd {path} && git branch --show-current",
        shell=True,
        check=True,
        capture_output=True
    ).stdout.decode("utf-8").strip().replace("/", "-")


def create_or_open_file(file_path, mode):
    directory, filename = os.path.split(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        give_permission(directory)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            ext = os.path.splitext(filename)[1]
            if ext == ".json":
                f.write("[]")
            else:
                f.write("")
        give_permission(file_path)
    return open(file_path, mode)


def get_output_dir():
    return os.path.join(get_config()["project_path"], __PREF_DIR)


def create_md_block_from_sample(conversation: Conversation) -> str:
    with create_or_open_file(__SAMPLE_MD, "r") as f:
        block = f.readlines()
        block = "".join(block)
        block = block.replace("{{author_name}}", __author_name())
        block = block.replace("{{prompt}}", conversation.prompt)
        block = block.replace("{{answer}}", conversation.answer)
        block = block.replace("{{rating}}", conversation.rating)
    return block


def create_md_file(conversations: dict):
    output_file = os.path.join(get_output_dir(), __current_branch() + ".md")
    block = "# " + __current_branch() + "\n\n"
    for c in conversations:
        block += create_md_block_from_sample(Conversation.from_dict(c))
    with create_or_open_file(output_file, "w") as f:
        f.write(block)


def get_json_files():
    output_file = os.path.join(get_output_dir(), __current_branch() + ".json")
    with create_or_open_file(output_file, "r") as f:
        conversations = json.load(f)
    return conversations


def write_to_json_file(conversations: dict):
    output_file = os.path.join(get_output_dir(), __current_branch() + ".json")
    with create_or_open_file(output_file, "w") as f:
        json.dump(conversations, f, indent=2, default=str, ensure_ascii=False)


def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_path):
        save_config(
            {
                "port": 9696,
                "debug": False,
                "project_path": os.getcwd(),
                "listen_url": "https://api.githubcopilot.com/chat/completions"
            }
        )
    with open(config_path, "r") as f:
        return json.load(f)


def save_config(config):
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with create_or_open_file(config_path, "w") as f:
        json.dump(config, f, indent=2, default=str, ensure_ascii=False)


if __name__ == '__main__':
    print(__current_branch())
    print(__author_name())
