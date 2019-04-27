#!/usr/bin/env python
# -*- coding:utf-8 -*-

import importlib
import json
import os
import glob
from pathlib import Path

import telegram
from flask import Flask, request

from config import *
from coolq import CoolQHttpAPI

app = Flask(__name__)
api = CoolQHttpAPI(COOLQ_PUAH_URL, access_token=ASSESS_TOKEN)
bot = telegram.Bot(token=TG_TOKEN)
plugin_center = {}


class PluginException(Exception):
    def __init__(self, err='插件错误'):
        print(f"{err}\n")
        # log操作
        Exception.__init__(self, err)


def plugin_load():
    global initialization
    os.makedirs("plugin", exist_ok=True)

    for i in glob.glob("plugin/*.py"):
        obj = importlib.import_module(f"plugin.{Path(i).stem}")
        register, plugins = obj.initialization()

        if type(plugins) != dict:
            raise PluginException("初始化插件失败")
        required = ["name", "register_trigger", "register_type", "callback"]
        if not set(required) < set(plugins.keys()):
            raise PluginException("初始化插件失败")

        plugin_center[register] = plugins
        obj.printf(qq=api,tg=bot)

    initialization = True


@app.route("/" + TG_TOKEN, methods=["POST"])
def tg_event():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message is None:
        return "Show me your TOKEN please!"
    if initialization:
        data = update.message.to_dict()
        for i in plugin_center:
            if plugin_center[i]["register_trigger"] == "" and plugin_center[i]["register_type"] == "all" or \
                    plugin_center[i]["register_type"] == "tg":
                plugin_center[i]["callback"]["tg"](qq=api, tg=bot, msg=data)
        command = data["text"].split(" ")[0]
        if "text" in data and command in plugin_center:
            if plugin_center["register_type"] == "tg" and plugin_center[command]["register_trigger"] != "":
                if data["chat"]["type"] == "group":
                    if data["chat"]["id"] in plugin_center[command]["register_target"]["tg"]["groups"] or \
                            plugin_center[command]["register_target"]["tg"]["groups"] == "all":
                        plugin_center[command]["callback"]["tg"](qq=api, tg=bot, msg=data)
                else:
                    # 处理成员消息
                    pass

    return ""


@app.route(COOLQ_RECVER_URL[COOLQ_RECVER_URL.rfind("/"):], methods=["POST"])
def qq_event():
    if initialization:
        data = json.loads(request.data.decode("utf-8"))
        # 遍历插件加载消息
        for i in plugin_center:
            if plugin_center[i]["register_trigger"] == "" and plugin_center[i]["register_type"] == "all" or \
                    plugin_center[i]["register_type"] == "qq":
                plugin_center[i]["callback"]["qq"](qq=api, tg=bot, msg=data)

        command = data["message"].split(" ")[0]
        if command in plugin_center:
            if plugin_center[command]["register_type"] == "qq" and plugin_center[command]["register_trigger"] != "":
                if data["message_type"] == "group":
                    if plugin_center[command]["register_target"]["qq"]["group"] == "all" or data["group_id"] in \
                            plugin_center[command]["register_target"]["qq"]["group"]:
                        plugin_center[command]["callback"]["qq"](qq=api, tg=bot, msg=data)

                else:
                    # if data["qq_id"] in COMMAND["register_target"]["qq"]["member"]:
                    # 我没看过成员字段是啥，先放着
                    pass
    return ""


@app.route("/control")
def control():
    # initialization = False
    if request.args.get("status") == "start":
        bot.set_webhook(TG_WEBHOOK)
        plugin_load()
        if initialization:
            return "start"
        else:
            return "error"
    elif request.args.get("status") == "stop":
        #global initialization
        initialization = False
        # 停止bot
        if not initialization:
            return "stop"
        else:
            return "error"
    elif request.args.get("status") == "uninstall":
        if request.args.get("plugins") != "" and request.args.get("plugins") in plugin_center:
            plugin_center.pop(request.args.get("plugins"))
            return "uninstall:ok"
        else:
            return "uninstall:plugin not found."

    # 返回状态
    return "Running......"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8088)
