#coding=utf-8
import hashlib
import random
import time
import redis

from django.shortcuts import render
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from Utils.common import success_response, failure_response, ERROR_CODE

from .serializers import UserLoginSerializer, UserRegisterSerializer, UserDetailSerializer
from .models import User, UserPermission

# 根据uid产生token并存入缓存
def generate_token_for_user(uid):
	token = hashlib.md5(str(int(time.time() * 1000) + random.randint(10000000, 99999999))).hexdigest()
	r = redis.Redis(host=settings.REDIS_HOST, db=settings.REDIS_USER_TOKEN_DB)
	r.set(uid, token)
	return token

#test
def getToken(request):
    uid = request.GET.get('uid')
    r = redis.Redis(host=settings.REDIS_HOST, db=settings.REDIS_USER_TOKEN_DB)
    token = r.get(uid)
    if token is not None:
        return HttpResponse(token)
    else:
        return HttpResponse(u'未获取到token,或token已过期')

class UserLoginAPIView(APIView):
	def post(self, request):
		serializer = UserLoginSerializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			user = auth.authenticate(username=data['username'], password=data['password'])
			if user is not None:
				token = generate_token_for_user(uid=user.id)
				return success_response({u'uid': user.id, u'token': token})
			else:
				try:
					User.objects.get(username=data['username'])
					return failure_response(ERROR_CODE.AUTH_ERROR, u'用户名或密码错误')
				except User.DoesNotExist:
					return failure_response(ERROR_CODE.AUTH_ERROR, u'用户名不存在')
		else:
			return failure_response(ERROR_CODE.SERIALIZER_ERROR, str(serializer.errors))

class UserRegisterAPIView(APIView):
	def post(self, request):
		serializer = UserRegisterSerializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data

			# 检查用户名是否可用
			try:
				User.objects.get(username=data['username'])
				return failure_response(ERROR_CODE.FAILED, u'用户名已存在,请登录')
			except User.DoesNotExist:
				pass

			# 创建新用户
			user = User.objects.create(username=data['username'])
			user.set_password(data['password'])
			user.save()
			UserPermission.objects.create(user=user)

			# 产生Token
			token = generate_token_for_user(uid=user.id)
			return success_response({u'token': token, u'user': UserDetailSerializer(user).data})
		else:
			return failure_response(ERROR_CODE.SERIALIZER_ERROR, str(serializer.errors))

class UserDetailAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterAPIView(data=request.data)