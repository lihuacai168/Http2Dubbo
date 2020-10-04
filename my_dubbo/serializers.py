# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: serializers.py 
# @Time : 2020-10-03 14:17:27
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

from rest_framework import serializers


class DubboServiceInfoSerializer(serializers.Serializer):
    is_detail = serializers.BooleanField(write_only=True, default=False, help_text='是否显示服务的详情')
    services = serializers.ListField(read_only=True)


class DubboInvokeSerializer(serializers.Serializer):
    service = serializers.CharField(required=True, write_only=True, help_text='接口完整路径')
    method = serializers.CharField(required=True, write_only=True, help_text='请求方法名')
    params = serializers.ListField(required=True, write_only=True, help_text='请求参数')
