# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework import status
from schedules.serializers import *
from schedules.models import *
from .utils import CalendarpaymentsUtils
from datetime import datetime, date
class ServiceController():

    def service_post(request):
        serializer = ServicePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            service = Service.objects.get(pk=serializer.validated_data['id'])
            fees_amount = round(float(service.service_amount)/float(service.number_of_fees), 2)
            start_date = service.start_date
            time_to_add = CalendarpaymentsUtils.get_timedelta(service.schedule_frequency)
            aux_date = start_date
            for i in range(0, number_of_fees):
                schedule = Schedule(
                    payment_date = aux_date,
                    fee_amount = fees_amount,
                    serviceId = service
                )
                schedule.save()
                aux_date = aux_date + time_to_add

            serializer = ServiceSerializer(service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def service_put(request, service):
        service_was_active = service.is_active
        serializer = ServiceMinimalPostSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if service.is_active != service_was_active:
                if service.is_active:
                    aux = service.schedule_set.filter(is_paid=False, is_active=False)
                    if aux.exists():
                        aux.update(is_active=True)

                else:
                    aux = service.schedule_set.all()
                    if aux.exists():
                        aux.update(is_active=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)