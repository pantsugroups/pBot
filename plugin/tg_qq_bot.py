# coding:utf-8
import re
# 呕
def peelphotourl(message_raw):  # return the message only and image_list
    image_list = []
    while message_raw.find("url=") != -1:
        # image_list.append(message_raw[message_raw.find("url=")+4:message_raw.find("]")])
        image_list.append(tool_function_txt("url=", "]", message_raw))
        message_raw = re.sub("\[CQ:image.*?\]", "", message_raw)
        print(message_raw)
    return message_raw, image_list
def qq_handle(tg_handle,qq_handle,msg=""):
    
    info = api.get_group_member_info(
                            558226805, msg["user_id"])
    name = info["card"] or info["nickname"]
    data = re.sub("\[.*?\]", "", msg["message"])
    # if "CQ:at" in msg:
    #     tg_handle.send_message(chat_id=-256726247, text="%s: %s" % (
    #                         name, data))
    if "CQ:image" in data["message"]:
        msg2, image_list = peelphotourl(data["messages"])
        for i in image_list:
            if msg2 != "":
                tg_handle.send_photo(chat_id=-256726247, photo=i, caption="%s: %s" % (name, msg2))
            else:
                tg_handle..send_photo(chat_id=-256726247, photo=i, caption="%s: Send a Photo." % (name))
    elif "message" in data:
        data = re.sub("\[.*?\]", "", msg)
                        bot.send_message(chat_id=-256726247, text="!%s: %s" % (
                            name, data))

def tg_handle(tg_handle,qq_handle,msg=""):
    if "username" not in data["from"]:
        name = "%s %s"(data["from"]["first_name"] , data["from"]["last_name"])
    else:
        name = data["from"]["username"]
    api.send_group_msg(558226805, "%s: %s" % (name, data["text"]))
def Initialization():
    return "/tgqqhelp", { # 第一个参数为唯一标识符
    "name":"transfer tg or qq", # 插件名称
    "register_trigger":"",# 触发语句，当这个语句为空时，则所有都捕获，合格的插件应该对包含唯一标识符的消息进行处理，例如使用帮助等，哪怕这个字段为空
    "register_type":"all", #  qq , tg , all 选择触发类型，如果是all则都触发
    "register_target":{# 指定只处理某些用户或者群，如果没有则可以不填
        "qq":{
        "member":[],
        "groups":["558226805",]
        },
        "tg":{
        "member":[],
        "groups":[-256726247],
        }
    },
    "level":0, # 优先级，暂定，也许有用也许没用
    "truncated":False, # 是否截断，截断则不让其他插件捕获，当然前提是 register_trigger 字段为空时这个条件才有用
    "callback":{ # 对于不同类型的触发函数，如果register_type为all时，则这两个字段必须要有内容
        "tg":tg_handle,
        "qq":qq_handle,
        }
    }