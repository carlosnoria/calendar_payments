# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class UserAdminUpsert(APIView):

	def post(self, request, format=None):
		serializer = UserAdminSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk, format=None):
		admin = get_object_or_404(UserAdmin, pk=pk)
		serializer = UserAdminSerializer(admin, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		admin = get_object_or_404(UserAdmin, pk=pk)
		admin.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

# Falta el resto
