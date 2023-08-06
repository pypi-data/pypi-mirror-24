# -*- coding:utf-8 -*-
from django_szuprefix.saas.models import Party
from django_szuprefix.utils import lbsutils

__author__ = 'denishuang'

from django.contrib.auth.models import User
from django.db import models


class Signin(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = u"签到"
        ordering = ('-create_time',)

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="signins",
                              on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="signins",
                             on_delete=models.PROTECT)
    longitude = models.FloatField(u"经度", null=True, blank=True)
    latitude = models.FloatField(u"纬度", null=True, blank=True)
    city = models.CharField(u"城市", max_length=128, null=True, blank=True, db_index=True)
    address = models.CharField(u"地址", max_length=256, null=True, blank=True)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True, db_index=True)

    def __unicode__(self):
        return u"%s %s sigin @%s" % (self.create_time.isoformat(), self.user, self.place)

    def save(self, **kwargs):
        self.party = self.user.as_saas_worker.party
        self.city = " ".join(lbsutils.get_place_province_and_city(self.address))
        return super(Signin, self).save(**kwargs)
