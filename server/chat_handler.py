import json
import os


def get_chat_list():
    CHATDIR = "./chat"
    dir_list = os.listdir(CHATDIR)
    result = []
    for d in dir_list:
        chat_dir = os.path.join(CHATDIR, d, "chat.json")
        with open(chat_dir, "r") as f:
            chat_log = json.load(f)
            result.append(chat_log["metadata"])
    return result
