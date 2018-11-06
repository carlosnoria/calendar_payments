# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from .controllers.utils import CalendarpaymentsUtils
from .controllers.service_controller import ServiceController
from .controllers.schedule_controller import ScheduleController


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

class UserClientUpsert(APIView):

	def post(self, request, format=None):
		serializer = UserClientSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk, format=None):
		client = get_object_or_404(UserAdmin, pk=pk)
		serializer = UserClientSerializer(client, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		client = get_object_or_404(UserClient, pk=pk)
		admin.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ServiceUpsert(APIView):

	def post(self, request, format=None):
		try:
			return ServiceController.service_post(request)
		except Exception as ex:
			print(ex)
			return Response({"error: error in post operation"}, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk, format=None):
		try:
			service = get_object_or_404(Service, pk=pk)
			return ServiceController.service_put(request, service)
		except Exception as ex:
			print(ex)
			return Response({"error: error in post operation"}, status=status.HTTP_400_BAD_REQUEST)	

	def delete(self, request, pk, format=None):
		service = get_object_or_404(Service, pk=pk)
		service.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ScheduleUpsert(APIView):

	def post(self, request, format=None):
		serializer = SchedulePostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk, format=None):
		try:
			schedule = get_object_or_404(Schedule, pk=pk)
			return ScheduleController.schedule_put(rrequest, schedule)
		except Exception as ex:
			print(ex)
			return Response({"error: error in put operation"}, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		schedule = get_object_or_404(Schedule, pk=pk)
		schedule.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


