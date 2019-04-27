# -*- coding:utf-8 -*-

import re
# 呕
plugin_name = "transfer tg or qq"

def tool_function_txt(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def printf():
    print(f"plugin: {plugin_name} is running.....")


def peelphotourl(message_raw):  # return the message only and image_list
    image_list = []
    while message_raw.find("url=") != -1:
        # image_list.append(message_raw[message_raw.find("url=")+4:message_raw.find("]")])
        image_list.append(tool_function_txt("url=", "]", message_raw))
        message_raw = re.sub(r"[CQ:image.*?]", "", message_raw)
        print(message_raw)
    return message_raw, image_list


def qq_handle(tg, qq, msg=None):
    if "user_id" in msg:
        info = qq.get_group_member_info(558226805, msg["user_id"])
        name = info["card"] or info["nickname"]
        symbol = re.compile(r"<.+>")
        name = re.sub(symbol, "", name)
    else:
        name = "unknown"
    data = re.sub(r"[.*?]", "", msg["message"])
    # if "CQ:at" in msg:
    #     tg.send_message(chat_id=-256726247, text="%s: %s" % (
    #                         name, data))
    if "CQ:image" in data:
        msg2, image_list = peelphotourl(data)
        for i in image_list:
            if msg2 != "":
                tg.send_photo(chat_id=-256726247, photo=i, caption=f"{name}: {msg2}")
            else:
                tg.send_photo(chat_id=-256726247, photo=i, caption=f"{name}: Send a Photo.")
    elif data != "":
        # data = re.sub("\[.*?\]", "", msg)
        tg.send_message(chat_id=-256726247, text=f"{name}: {data}")


def tg_handle(tg, qq, msg=None):
    # if "username" not in msg["from"]:
    name = f"{msg['from']['first_name']} {msg['from']['last_name']}"
    # else:
    #     name = msg["from"]["username"]
    qq.send_group_msg(558226805, f"{name}: {msg['text']}")


def initialization():
    return "/tgqqhelp", {  # 第一个参数为唯一标识符
        "name": plugin_name,  # 插件名称
        "register_trigger": "",  # 触发语句，当这个语句为空时，则所有都捕获，合格的插件应该对包含唯一标识符的消息进行处理，例如使用帮助等，哪怕这个字段为空
        "register_type": "all",  # qq , tg , all 选择触发类型，如果是all则都触发
        "register_target": {  # 指定只处理某些用户或者群，如果没有则可以不填
            "qq": {
                "member": [],
                "groups": ["558226805", ]
            },
            "tg": {
                "member": [],
                "groups": [-256726247],
            }
        },
        "level": 0,  # 优先级，暂定，也许有用也许没用
        "truncated": False,  # 是否截断，截断则不让其他插件捕获，当然前提是 register_trigger 字段为空时这个条件才有用
        "callback": {  # 对于不同类型的触发函数，如果register_type为all时，则这两个字段必须要有内容
            "tg": tg_handle,
            "qq": qq_handle,
        }
    }
