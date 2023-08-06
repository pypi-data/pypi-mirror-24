# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django_szuprefix.saas.models import Party
from django.contrib.auth.models import User


class Task(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = u"任务"
        ordering = ('-create_time',)

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="message_tasks",
                              on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="message_tasks",
                             on_delete=models.PROTECT)
    type = models.CharField(u"消息类型", max_length=32, default='sys')
    title = models.CharField(u"标题", max_length=255, blank=True)
    content = models.TextField(u"内容", blank=True, null=True)
    link = models.CharField(u"连接", max_length=255, blank=True, null=True, default='')
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    is_active = models.BooleanField(u"有效", default=True)


class Message(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = u"消息"
        ordering = ('-create_time',)

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="messages",
                              on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="messages",
                             on_delete=models.PROTECT)
    task = models.ForeignKey(Task, verbose_name=Task._meta.verbose_name, related_name="messages",
                             on_delete=models.PROTECT)
    is_read = models.BooleanField(u"是否已读", default=False)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
    read_time = models.DateTimeField(u"阅读时间", null=True, blank=True)

    def save(self, **kwargs):
        return super(Message, self).save(**kwargs)
