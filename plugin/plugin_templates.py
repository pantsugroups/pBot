plugin_name = "test_plguin"
# coding:utf-8
# 这个函数也是必不可少的
def Printf(tg_handle="",qq_handle="",mag=""):# 这些参数是必不可少的。两个handle用于对相应的事件做出反馈。
    print("plugin: %s this plugin is running....."% plugin_name)
def Initialization():
    return "/test", { # 第一个参数为唯一标识符
    "name":plugin_name, # 插件名称
    "register_trigger":"",# 触发语句，当这个语句为空时，则所有都捕获，合格的插件应该对包含唯一标识符的消息进行处理，例如使用帮助等，哪怕这个字段为空
    "register_type":"all", #  qq , tg , all 选择触发类型，如果是all则都触发
    "register_target":{# 指定只处理某些用户或者群，如果没有则可以不填
        "qq":{
        "member":[],
        "groups":[]
        },
        "tg":{
        "member":[],
        "groups":[],
        }
    },
    "level":0, # 优先级，暂定，也许有用也许没用
    "truncated":False, # 是否截断，截断则不让其他插件捕获，当然前提是 register_trigger 字段为空时这个条件才有用
    "callback":{ # 对于不同类型的触发函数，如果register_type为all时，则这两个字段必须要有内容
        "tg":Printf,
        "qq":Printf,
        }
    }