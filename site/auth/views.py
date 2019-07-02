import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_202_ACCEPTED,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from feeduser.models import ProducerProfile, ConsumerProfile
from feeduser.serializers import UserRegSerializer


class LogOut(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # print('>>>', request.data)
        # print('>>>', request.user)
        logout(request)
        response = {'logout': 'OK'}
        return Response(response, status=HTTP_202_ACCEPTED)


class Login(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response(status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        response = user.as_dict
        if not user:
            return Response(status=HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        response.update({'token': token.key})
        print(response)
        return Response(response, status=HTTP_200_OK)


class Registration(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        print('>>>data', request.POST)
        user_data = json.loads(request.data.get('user_data'))
        profile_data = json.loads(request.data.get('profile_data'))
        location_data = json.loads(request.data.het('location'))
        avatar = request.data.get('avatar')
        # print(user_data)
        user_data.update({'avatar': avatar})
        is_producer = profile_data.pop('is_producer')
        # print('>>>', is_producer)
        serializer = UserRegSerializer(data=user_data)
        if serializer.is_valid():
            # print('!'*50)
            user = serializer.save()
            if is_producer:
                producer = ProducerProfile(user=user, **profile_data)
                producer.save()
            else:
                consumer = ConsumerProfile(user=user, **profile_data)
                consumer.save()
            if user:
                response = user.as_dict
                token, _ = Token.objects.get_or_create(user=user)
                response.update({'token': token.key})
                return Response(response, status=HTTP_200_OK)
        print(serializer.errors)
        # print(serializer.error_messages)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
