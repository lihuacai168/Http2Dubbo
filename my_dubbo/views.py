from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from my_dubbo.dubbo import Dubbo
from my_dubbo.serializers import DubboServiceInfoSerializer, DubboInvokeSerializer


class DubboView(ViewSet):
    """
    invoke:
    调用dubbo接口

    list:
    查询所有节点上所有dubbo接口

    """
    serializer_classes = {
        'list': DubboServiceInfoSerializer,
        'create': DubboInvokeSerializer
    }

    @swagger_auto_schema(
        request_body=DubboInvokeSerializer
    )
    def invoke(self, request):
        ser = DubboInvokeSerializer(data=request.data)
        if ser.is_valid():

            service: str = ser.validated_data.get('service')
            method: str = ser.validated_data.get('method')
            for dubbo_conf in settings.DUBBO_CONFIG:
                conn = Dubbo(**dubbo_conf)
                if service in conn.ls():
                    find_service = False
                    for item in conn.ll(service):
                        service_method: dict = conn.parse_method(item)
                        if service_method['method_name'] == method:
                            # 接口和方法名都相同，判定为找到可调用的服务
                            find_service = True
                            break
                    if find_service is True:
                        # 服务在当前的节点，就跳出
                        break
                else:
                    # 当前节点不包含服务，就关闭当前连接
                    conn.close()
            else:
                # 所有的节点都不包含服务
                return Response({'res': f'not exist service: {service} or method: {method}'})

            params: list = ser.validated_data.get('params')
            res = conn.invoke(service, method, *params)
            conn.close()
            return Response(res)

        else:
            return Response(ser.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @swagger_auto_schema(
        query_serializer=DubboServiceInfoSerializer
    )
    def list(self, request):
        ser = DubboServiceInfoSerializer(data=request.query_params)
        if ser.is_valid():
            is_detail: bool = ser.validated_data.get('is_detail')
            res = []
            for dubbo_conf in settings.DUBBO_CONFIG:
                host = dubbo_conf['host']
                port = dubbo_conf['port']
                conn = Dubbo(host=host, port=port)
                if is_detail is True:
                    services: list = conn.ls()
                    for service in services:
                        # 因为item是dict类型，不能hash，所以不能用set(res)来过滤
                        item = {service: conn.get_service_method(service)}
                        if item in res:
                            continue
                        else:
                            res.append(item)
                else:
                    res.extend(conn.ls())
                conn.close()

            # list包含的string，可以用set
            if is_detail is False:
                res = set(res)
            return Response(res)
        else:
            return Response(ser.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
