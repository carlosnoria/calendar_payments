# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from dateutil.relativedelta import relativedelta

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
		serializer = ServicePostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			service = get_object_or_404(Service, pk=serializer.validated_data['id'])
			fees_amount = round(float(service.service_amount)/float(service.number_of_fees), 2)
			start_date = service.start_date
			schedule_frequency = service.schedule_frequency
			time_to_add = timedelta(microsecond=1)

			if schedule_frequency == 'Diario':
				time_to_add = timedelta(days=1)
			elif schedule_frequency == 'Semanal':
				time_to_add = timedelta(weeks=1)
			elif schedule_frequency == 'Quincenal':
				time_to_add = timedelta(weeks=2)
			elif schedule_frequency == 'Mensual':
				time_to_add = relativedelta(months=+1)
			elif schedule_frequency == 'Bimensual':
				time_to_add = relativedelta(months=+2)
			elif schedule_frequency == 'Trimestral':
				time_to_add = relativedelta(months=+3)
			elif schedule_frequency == 'Semestral':
				time_to_add = relativedelta(months=+6)
			elif schedule_frequency == 'Anual':
				time_to_add = relativedelta(years=+1)

			aux_date = start_date
			for i in range(0, number_of_fees):
				schedule = Schedule(
					payment_date = aux_date,
					fees_amount = fees_amount,
					serviceId = service
				)
				schedule.save()
				aux_date = aux_date + time_to_add

			serializer = ServiceSerializer(service)
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk, format=None):
		service = get_object_or_404(Service, pk=pk)
		previous_amount = service.service_amount
		previous_number_of_fees = service.number_of_fees
		schedule_frequency = 
		serializer = ServicePostSerializer(service, data=request.data)
		if serializer.is_valid():


