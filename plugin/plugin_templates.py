# coding:utf-8
def Printf(tg_handle,qq_handle,mag=""):# 这些参数是必不可少的
    print("this plugin is running.....")
def Initialization():
    return "/test", { # 第一个参数为唯一标识符
    "name":"test",
    "register_trigger":"",# 触发语句，当这个语句为空时，则所有都捕获
    "register_type":"all", #  qq , tg , all 选择触发类型，如果是all则都触发
    "register_target":{# 指定只处理某些用户或者群
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
    "truncated":False, # 是否截断，截断则不让其他插件捕获
    "callback":{ # 对于不同类型的触发函数
        "tg":printf,
        "qq":printf,
        }
    }