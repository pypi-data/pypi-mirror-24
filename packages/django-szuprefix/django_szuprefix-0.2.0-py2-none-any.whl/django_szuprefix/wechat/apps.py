# -*- coding:utf-8 -*-
from django.apps import AppConfig
from django.conf import settings

__author__ = 'denishuang'


class Config(AppConfig):
    name = "wechat"
    label = u"微信"

    # def ready(self):
    #     from . import receivers


MP = settings.WECHAT.get("MP", {})
