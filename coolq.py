# -*- coding: utf-8 -*-
import json

import requests

RETCODE = {
    100: AttributeError("100: 参数缺失或参数无效"),
    102: ValueError("102: 酷Q函数返回的数据无效"),
    103: PermissionError("103: 权限不足或文件系统异常，不符合预期"),
    104: RuntimeError("104: 酷Q凭证失效"),
    201: EnvironmentError("201: 工作线程池未正确初始化")
}


class CoolQHttpAPI:
    
    def __init__(self, addr, access_token=None):
        if addr[-1] == "/":
            self.addr = addr[:-1]
        else:
            self.addr = addr
        self.access_token = access_token
        if not self.get_status()["good"]:
            raise ConnectionError("连接到酷Q失败")
    
    def _POST(self, api, **kargs):
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = "Token %s" % self.access_token
        try:
            resp = requests.post(
                url=self.addr + "/" + api,
                headers=headers,
                data=json.dumps(kargs),
                timeout=5)
        except requests.exceptions.ConnectionError:
            raise ConnectionError("无法连接到酷Q")
        except requests.exceptions.Timeout:
            raise TimeoutError("与酷Q通讯时发生超时")
        if resp.status_code == 404:
            raise NameError("API %s 不存在" % api)
        tmp = resp.json()
        if tmp["status"] == "async":
            return None
        if tmp["status"] == "failed":
            if tmp["retcode"] in RETCODE:
                raise RETCODE[tmp["retcode"]]
            else:
                raise NotImplementedError("%s 未知错误" % tmp["retcode"])
        return tmp["data"]
    
    def send_private_msg(self, user_id, message, auto_escape=False):
        return self._POST(
            "send_private_msg",
            user_id=user_id,
            message=message,
            auto_escape=auto_escape
        )
    
    def send_group_msg(self, group_id, message, auto_escape=False):
        return self._POST(
            "send_group_msg",
            group_id=group_id,
            message=message,
            auto_escape=auto_escape
        )
    
    def send_discuss_msg(self, discuss_id, message, auto_escape=False):
        return self._POST(
            "send_discuss_msg",
            group_id=discuss_id,
            message=message,
            auto_escape=auto_escape
        )
    
    def delete_msg(self, message_id):
        return self._POST(
            "delete_msg",
            message_id=message_id)
    
    def send_like(self, user_id, times=1):
        return self._POST(
            "send_like",
            times=times
        )
    
    def set_group_kick(self, group_id, user_id, reject_add_request=False):
        return self._POST(
            "set_group_kick",
            group_id=group_id,
            user_id=user_id,
            reject_add_request=reject_add_request
        )

    def set_group_ban(self, group_id, user_id, duration=60):
        return self._POST(
            "set_group_ban",
            group_id=group_id,
            user_id=user_id,
            duration=duration
        )

    def set_group_anonymous_ban(self, group_id, anonymous=None, 
                                anonymous_flag=None, duration=30):
        if anonymous:
            return self._POST(
                "set_group_anonymous_ban",
                group_id=group_id,
                anonymous=anonymous,
                duration=duration
            )
        elif anonymous_flag:
            return self._POST(
                "set_group_anonymous_ban",
                group_id=group_id,
                anonymous_flag=anonymous_flag,
                duration=duration
            )
        else:
            raise AttributeError("anonymous与anonymous_flag二选一必填")

    def set_group_whole_ban(self, group_id, enable=True):
        return self._POST(
            "set_group_whole_ban",
            group_id=group_id,
            enable=enable
        )

    def set_group_admin(self, group_id, user_id, enable=True):
        return self._POST(
            "set_group_admin",
            group_id=group_id,
            user_id=user_id,
            enable=enable
        )
    
    def set_group_anonymous(self, group_id, enable=True):
        return self._POST(
            "set_group_anonymous",
            group_id=group_id,
            enable=enable
        )
    
    def set_group_card(self, group_id, user_id, card=""):
        return self._POST(
            "set_group_card",
            group_id=group_id,
            user_id=user_id,
            card=card
        )
    
    def set_group_leave(self, group_id, is_dismiss=False):
        return self._POST(
            "set_group_leave",
            group_id=group_id,
            is_dismiss=is_dismiss
        )
    
    def set_group_special_title(self, group_id, user_id, special_title="", duration=-1):
        return self._POST(
            "set_group_special_title",
            group_id=group_id,
            user_id=user_id,
            special_title=special_title,
            duration=duration
        )
    
    def set_discuss_leave(self, discuss_id):
        return self._POST(
            "set_discuss_leave",
            discuss_id=discuss_id
        )
    
    def set_friend_add_request(self, flag, approve=True, remark=""):
        return self._POST(
            "set_friend_add_request",
            flag=flag,
            approve=approve,
            remark=remark
        )
    
    def set_group_add_request(self, flag, sub_type, approve=True, reason=""):
        return self._POST(
            "set_group_add_request",
            flag=flag,
            sub_type=sub_type,
            approve=approve,
            reason=reason
        )
    
    def get_login_info(self):
        return self._POST("get_login_info")
    
    def get_stranger_info(self, user_id, no_cache=False):
        return self._POST(
            "get_stranger_info",
            user_id=user_id,
            no_cache=no_cache
        )
    
    def get_group_list(self):
        return self._POST("get_group_list")
    
    def get_group_member_info(self, group_id, user_id, no_cache=False):
        return self._POST(
            "get_group_member_info",
            group_id=group_id,
            user_id=user_id,
            no_cache=no_cache
        )

    def get_group_member_list(self, group_id):
        return self._POST(
            "get_group_member_list",
            group_id=group_id
        )
    
    def get_cookies(self):
        return self._POST("get_cookies")

    def get_csrf_token(self):
        return self._POST("get_csrf_token")
    
    def get_credentials(self):
        return self._POST("get_credentials")
    
    def get_record(self, file, out_format):
        return self._POST(
            "get_record",
            file=file,
            out_format=out_format
        )
    
    def get_status(self):
        return self._POST("get_status")
    
    def get_version_info(self):
        return self._POST("get_version_info")
    
    def set_restart(self, clean_log=False, clean_cache=False, clean_event=False):
        return self._POST(
            "set_restart",
            clean_log=clean_log,
            clean_cache=clean_cache,
            clean_event=clean_event
        )
    
    def set_restart_plugin(self, delay=0):
        return self._POST(
            "set_restart_plugin",
            delay=delay
        )
    
    def clean_data_dir(self, data_dir):
        return self._POST(
            "clean_data_dir",
            data_dir=data_dir
        )
    
    def clean_plugin_log(self):
        return self._POST("clean_plugin_log")


if __name__ == "__main__":
    api = CoolQHttpAPI("http://127.0.0.1:5700")
    api.send_private_msg(524543577, "Hello")