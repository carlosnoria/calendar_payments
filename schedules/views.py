# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from datetime import datetime, date

# UserAdmin Views
class UserAdminListView(APIView):

    def get(self, request, format=None):
        serializer = UserAdminSerializer(UserAdmin.objects.all(), many=True)
        return Response(serializer.data)

class UserAdminDetailView(APIView):

    def get(self, request, pk, format=None):
        serializer = UserAdminSerializer(get_object_or_404(UserAdmin, pk=pk))
        return Response(serializer.data)

class UserAdminActiveListView(APIView):

    def get(self, request, format=None):
        serializer = UserAdminSerializer(UserAdmin.objects.filter(is_active=True), many=True)
        return Response(serializer.data)

# UserClient Views
class UserClientListView(APIView):

    def get(self, request, format=None):
        serializer = UserClientSerializer(UserClient.objects.all(), many=True)
        return Response(serializer.data)

class UserClientDetailView(APIView):

    def get(self, request, pk, format=None):
        serializer = UserClientSerializer(get_object_or_404(UserClient, pk=pk))
        return Response(serializer.data)

class UserAdminActiveListView(APIView):

    def get(self, request, format=None):
        serializer = UserClientSerializer(UserClient.objects.filter(is_active=True), many=True)
        return Response(serializer.data)

# Service Views
class ServicesListView(APIView):

    def get(self, request, format=None):
        services = Service.objects.all()
        services = ServiceSerializer.setup_eager_loading(services)
        serializer = ServiceSerializer(Service.objects.all(), many=True)
        return Response(serializer.data)

class ServiceDetailView(APIView):

    def get(self, request, pk, format=None):
        service = get_object_or_404(Service, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

class ServicesActiveListView(APIView):

    def get(self, request, format=None):
        services = Service.objects.filter(is_active=True)
        services = ServiceSerializer.setup_eager_loading(services)
        serializer = ServiceSerializer(Service.objects.all(), many=True)
        return Response(serializer.data)

class UserServicesActiveListView(APIView):

    def get(self, request, userpk, format=None):
        services = Service.objects.filter(is_active=True, clientId__id=userpk)
        services = ServiceSerializer.setup_eager_loading(services)
        serializer = ServiceSerializer(Service.objects.all(), many=True)
        return Response(serializer.data)

# Schedules views
class UnpaidSchedulesListView(APIView):
    
    def get(self, request, format=None):
        today = date.today()
        schedules = Schedules.objects.filter(is_paid=False, is_active=True, payment_date__lte=today)
        schedules = ScheduleSerializer.setup_eager_loading(schedules)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

class SchedulesDetailView(APIView):
    
    def get(self, request, pk, format=None):
        serializer = get_object_or_404(Schedules, pk=pk)
        return Response(serializer.data)

class DiscardedUnpaidSchedulesListByServiceView(APIView):

    def get(self, request, servicepk, format=None):
        today = date.today()
        schedules = Schedules.objects.filter(serviceId__id=servicepk, is_active=False, 
            is_paid=False, payment_date__lte=today)
        schedules = ScheduleSerializer.setup_eager_loading(schedules)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

class UnpaidSchedulesListByServiceView(APIView):

    def get(self, request, servicepk, format=None):
        today = date.today()
        schedules = Schedules.objects.filter(serviceId__id=servicepk, is_paid=False, is_active=True,
        payment_date__lte=today)
        schedules = ScheduleSerializer.setup_eager_loading(schedules)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

class SchedulesToBePaidListByServiceView(APIView):
    
    def get(self, request, servicepk, format=None):
        today = date.today()
        schedules = Schedules.objects.filter(serviceId__id=servicepk, is_paid=False, is_active=True,
        payment_date__gt=today)
        schedules = ScheduleSerializer.setup_eager_loading(schedules)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

class PaidSchedulesListByService(APIView):
    
    def get(self, request, servicepk, format=None):
        schedules = Schedules.objects.filter(serviceId__id=servicepk, is_paid=True)
        schedules = ScheduleSerializer.setup_eager_loading(schedules)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

