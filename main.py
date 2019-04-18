#coding:utf-8
from coolq import CoolQHttpAPI
import telegram
import sys
import json,os,importlib
from * import config
from flask import Flask, request
app = Flask(__name__)
api = CoolQHttpAPI(COOLQ_PUAH_URL, access_token=ASSESS_TOKEN)

sys.path.append('plugin')
COMMAND_MAP = {}
class PluginException(Exception):
    def __init__(self,err='插件错误'):
        print("%s\n",err)
        Exception.__init__(self,err)

def Plugin_Load():
    if not os.path.isdir("plugin/"):
        os.mkdir("plugin/")
    files = os.listdir("plugin/")
    for i in files:
        if i[i.rfind("."):] == ".py":
            register,plugins = importlib.import_module(i.replace(".py","")).Initialization()

            if type(plugins) != dict:
                raise PluginException("初始化插件失败")
            if "name" not in plugins or "register_trigger" not in plugins or "register_type" not in plugins or "callback" not in plugins:
                raise PluginException("初始化插件失败")
            COMMAND_MAP[register] = plugins
            
@app.route("/"+TG_API, methods=["POST"])
def tg_event():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message is None:
        return "Show me your TOKEN please!"
    data = update.message.to_dict()
    # 遍历插件加载消息

    return ""

@app.route(COOLQ_RECVER_URL[COOLQ_RECVER_URL.rfind("/"):], methods=["POST"])
def qq_event():
    data = json.loads(request.data.decode("utf-8"))
    # 遍历插件加载消息
    return ""

@app.route("/control")
def control():
    pass
