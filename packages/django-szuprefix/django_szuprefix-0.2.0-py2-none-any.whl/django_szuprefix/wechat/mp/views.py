# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

__author__ = 'denishuang'
from . import helper


@csrf_exempt
def ports(request):
    echostr = request.GET.get("echostr")
    api = helper.api
    flag = api.check_tencent_signature(request)
    if flag:
        um = api.deal_post(request.body)
        if um:
            response = HttpResponse(api.response_user(um), "text/xml; charset=utf-8")
            response._charset = "utf-8"
            return response
    return HttpResponse(echostr)


@csrf_exempt
def notice(request):
    return HttpResponse(helper.api.pay_result_notify(request.body))
