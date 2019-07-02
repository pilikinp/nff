from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from orders.serializers import ListOrderSerializer, CreateOrderSerializer
from orders.models import OrderItem


class OrdersList(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = OrderItem.objects.all()
    serializer_class = ListOrderSerializer

    # create order item
    def create(self, request, *args, **kwargs):
        print(request.data)

        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        print(serializer.errors)
        return Response(status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = OrderItem.objects.get(pk=pk)
        if instance:
            serializer = ListOrderSerializer(instance)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if 'ids' in request.GET:
            ids = list(map(lambda x: int(x), request.GET['ids'].split(',')))
            queryset = OrderItem.objects.filter(pk__in=ids, is_active=True)
        elif 'user_id' in request.GET:
            queryset = OrderItem.objects.filter(consumer__pk=int(request.GET['user_id']), is_active=True)
        elif 'chef_id' in request.GET:
            queryset = OrderItem.objects.filter(chef__id=int(request.GET['chef_id']), is_active=True)
        else:
            queryset = OrderItem.objects.all().filter(is_active=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListOrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ListOrderSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        print('update:', request.data)
        pk = request.data.get('id')
        instance = OrderItem.objects.get(pk=pk)
        print(instance.id, instance)
        serializer = CreateOrderSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        print(serializer.errors)
        return Response(status=HTTP_400_BAD_REQUEST)
