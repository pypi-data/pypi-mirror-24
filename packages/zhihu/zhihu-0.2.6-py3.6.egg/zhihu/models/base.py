# encoding: utf-8

"""

获取知乎数据对象的抽象既基类，任何对象都可以继承该类

比如 Answer, Question, Account

"""

import os
import platform
import re
import subprocess
from http import cookiejar

import requests
import requests.packages.urllib3 as urllib3
from bs4 import BeautifulSoup

from zhihu import settings
from zhihu.error import ZhihuError
from zhihu.url import URL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Model(requests.Session):
    def __init__(self):
        super(Model, self).__init__()
        self.cookies = cookiejar.LWPCookieJar(filename=settings.COOKIES_FILE)
        try:
            self.cookies.load(ignore_discard=True)
        except FileNotFoundError:
            pass
        self.verify = False
        self.headers = settings.HEADERS

    def _get_captcha(self, _type="login"):
        r = self.get(URL.captcha(_type=_type))
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)

        # 调用系统图片预览工具
        if platform.system() == 'Darwin':
            subprocess.call(['open', 'captcha.jpg'])
        elif platform.system() == 'Linux':
            subprocess.call(['xdg-open', 'captcha.jpg'])
        else:
            os.startfile('captcha.jpg')
        captcha = input("输入验证码：")
        return captcha

    def _get_xsrf(self, url=None):
        """
        获取某个URL页面下的xsrf
        :param url:
        :return: xsrf
        """
        response = self.get(url or URL.index())
        soup = BeautifulSoup(response.content, "lxml")
        xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
        return xsrf

    def _user_id(self, user_slug=None, user_url=None):
        """
        user_slug 转 user_id
        :param user_slug:
        :param user_url:
        :return:
        """
        if not user_slug:
            user_slug = self._user_slug(user_url=user_url)
        profile = self.profile(user_slug=user_slug)
        user_id = profile.get("id")
        return user_id

    def _user_slug(self, user_url):
        pattern = re.compile("https?://www.zhihu.com/people/([\w-]+)")
        match = pattern.search(user_url)
        if match:
            user_slug = match.group(1)
            return user_slug
        else:
            raise ZhihuError("invalid url")

    def _execute(self, method="post", url=None, params=None, json=None, data=None, **kwargs):
        """
        通用请求方法
        :param method: 请求方法
        :param url:     请求URL
        :param params:  请求参数
        :param data:    请求数据
        :param data_type:    提交的数据格式(可能是表单类型,也可能是json格式的字符串)
        :param kwargs:  requests支持的参数，比如可以设置代理参数
        :return: response
        """
        r = getattr(self, method)(url, json=json, data=data, params=params, **kwargs)
        return r
