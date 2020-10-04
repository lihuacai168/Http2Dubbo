# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: urls.py 
# @Time : 2020/7/22 23:38
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

from django.urls import path
from my_dubbo.views import DubboView

urlpatterns = [
    path('service/', DubboView.as_view({
        "get": "list",
        "post": "invoke"
    })),

]
