import json
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.authentication import TokenAuthentication
from feeduser.models import FeedUser, ProducerProfile, ConsumerProfile
from feeduser.serializers import UserSerializer, ProducerSerializer, \
    ConsumerSerializer, UpdateProducerSerializer, UpdateConsumerSerializer

from pprint import pprint


class UsersList(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = FeedUser.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        pprint(request.data)
        user_data = json.loads(request.data.get('user_data'))
        profile_data = json.loads(request.data.get('profile_data'))
        avatar = request.data.get('avatar')
        is_producer = profile_data.pop('is_producer')
        # print('user data>>>', user_data)
        # print('profile data>>>', profile_data)
        # print('avatar>>>', avatar)
        user_instance = FeedUser.objects.get(pk=user_data.get('id'))
        user_data.update({'avatar': avatar})
        user_serializer = UserSerializer(data=user_data, instance=user_instance)
        if user_serializer.is_valid():
            user_serializer.save()
            if is_producer:
                # print('IS PRODUCER')
                profile_instance = ProducerProfile.objects.get(pk=profile_data.get('id'))
                profile_serializer = UpdateProducerSerializer(data=profile_data, instance=profile_instance)
            else:
                # print('NOT PRODUCER')
                profile_instance = ConsumerProfile.objects.get(pk=profile_data.get('id'))
                profile_serializer = UpdateConsumerSerializer(data=profile_data, instance=profile_instance)
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                print('errs>>>', profile_serializer.errors)

            return Response(status=HTTP_200_OK)
        print('errors>>>', user_serializer.errors)
        print('errors>>>', user_serializer.error_messages)
        return Response(status=HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = ProducerProfile.objects.filter(user__id=pk) or ConsumerProfile.objects.filter(user__id=pk)
        response = {'is_producer': False}
        if instance:
            instance = instance[0]
            # print('>>>', instance.user.username)
            if isinstance(instance, ProducerProfile):
                serializer = ProducerSerializer(instance)
                response['is_producer'] = True
            else:
                serializer = ConsumerSerializer(instance)
            response.update(serializer.data)
            return Response(response, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ProducersList(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = ProducerProfile.objects.all()
    serializer_class = ProducerSerializer

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = ProducerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProducerSerializer(self.queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = ProducerProfile.objects.get(pk=pk)
        if instance:
            serializer = ProducerSerializer(instance)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pprint(request.data)
        user = request.data.pop('user')
        profile = request.data
        print(user)

        instance_user = FeedUser.objects.get(pk=user.get('id'))
        serializer_user = UserSerializer(data=user, instance=instance_user)

        instance_profile = ProducerProfile.objects.get(id=profile.get('id'))
        serializer_profile = UpdateProducerSerializer(data=profile, instance=instance_profile)
        if serializer_user.is_valid() and serializer_profile.is_valid():
            serializer_user.save()
            serializer_profile.save()
            return Response(status=HTTP_200_OK)
        else:
            print(serializer_user.errors, serializer_profile.errors)
            return Response(status=HTTP_400_BAD_REQUEST)


class ConsumersList(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = ConsumerProfile.objects.all()
    serializer_class = ConsumerSerializer

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = ConsumerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ConsumerSerializer(self.queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = ConsumerProfile.objects.get(pk=pk)
        if instance:
            serializer = ConsumerSerializer(instance)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
