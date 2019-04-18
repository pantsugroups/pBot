# coding:utf-8
def Printf(tg_handle,qq_handle,mag=""):# 这些参数是必不可少的
    print("this plugin is running.....")
def Initialization():
    return "/test", {
    "name":"test",
    "register_trigger":"/test",# 触发语句
    "register_type":"all", #  qq , tg , all 选择触发类型，如果是all则都触发
    "level":0 # 优先级，暂定，也许有用也许没用
    "callback":{ # 对于不同类型的触发函数
        "tg":printf,
        "qq":printf,
        }
    }