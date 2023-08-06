# encoding: utf-8

import logging
import re

from zhihu import settings
from zhihu.models.base import Model
from zhihu.error import ZhihuError
from zhihu.models import RequestDataType
from zhihu.url import URL


class Account(Model):
    def login(self, account, password):
        """
        账户登录
        :param account: email或者手机号码
        :param password:
        :param kwargs:
        :param kwargs:
        :return:
        """
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        phone_regex = r"\+?\d{10,15}$"
        email_pattern = re.compile(email_regex)
        phone_pattern = re.compile(phone_regex)

        if email_pattern.match(account):
            return self._login_email(account, password)
        elif phone_pattern.match(account):
            return self._login_phone(account, password)
        else:
            raise ZhihuError("无效的用户名")

    def _login_phone(self, phone, password):
        data = {
            '_xsrf': self._get_xsrf(),
            'password': password,
            'phone_num': phone,
            "captcha": self._get_captcha(),
            "remeber_me": "true",
        }
        return self._login_execute(url=URL.phone_login(), data=data)

    def _login_email(self, email, password, **kwargs):
        data = {'email': email,
                'password': password,
                '_xsrf': self._get_xsrf(),
                "captcha": self._get_captcha(),
                'remember_me': 'true'}
        return self._login_execute(url=URL.email_login(), data=data, **kwargs)

    def _login_execute(self, url=None, data=None):

        r = self._execute(method="post", url=url, data=data)
        if r.ok:
            result = r.json()
            if result.get("r") == 0:
                self.cookies.save(ignore_discard=True)  # 保存登录信息cookies
                self.cookies.load(filename=settings.COOKIES_FILE, ignore_discard=True)
            return result

        else:
            return {'r': 1, "msg": "登录失败"}

    def _register_validate(self, data):
        """
        注册前的验证,是否已经注册
        :return:
        """
        r = super(Account, self)._execute(method="post",
                                          url=URL.register_validate(),
                                          data=data,
                                          data_type=RequestDataType.FORM_DATA)
        if r.ok and r.json().get("r") == 0:
            return True
        else:
            if r.ok and r.json().get("r") == 1:
                self.log(r.text)
            return False

    def register(self, name=None, phone_num=None, password=None):
        data = {
            "fullname": name,
            "phone_num": phone_num,
            "password": password,
            "_xsrf": super(Account, self)._get_xsrf(),
            "captcha": super(Account, self)._get_captcha(_type="register"),
            "captcha_source": "register",
        }
        valid = self._register_validate(data)
        if valid:
            self.log("账号验证成功,发送短信验证码")
            params = {"phone_num": phone_num, "captcha_source": "register"}
            # 发送验证码
            r = self._execute(method="get", url=URL.register_sms_code(), params=params)
            self.log(r.json().get("msg"))
            code = input("输入短信验证码:")
            data['verification_code'] = code
            data.pop("captcha")
            r = self._execute(method="post", url=URL.register(), data=data, data_type=RequestDataType.FORM_DATA)
            if r.ok and r.json().get("r") == 0:
                self.log("注册成功")
                return r.json()
            else:
                if r.ok and r.json().get("r") != 0:
                    self.log(r.json().get("msg"), level=logging.ERROR)
                if not r.ok:
                    self.log("请求失败", level=logging.ERROR)
                return r.json()
        else:
            raise ZhihuError("验证失败,请查看日志")
