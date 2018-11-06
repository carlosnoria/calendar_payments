# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework import status
from schedules.serializers import *
from schedules.models import *
from .utils import CalendarpaymentsUtils

class ScheduleController():

	def schedule_put(request, schedule):
		serializer = SchedulePostSerializer(schedule, data=request.data)
		if serializer.is_valid():
			serializer.save()
			if schedule['is_active'] == False and schedule['is_paid'] == False:
				amount_to_be_deferred = schedule.fee_amount - schedule.paid_amount
				if amount_to_be_deferred == 0:
					schedule.is_paid = True
					schedule.save()
				elif amount_to_be_deferred > 0:
					active_schedules = schedule.serviceId.schedule_set.filter(is_active=True, is_paid=False, payment_date__gt=schedule.payment_date)
					if active_schedules.exists():
						next_schedule = active_schedules[0]
						next_schedule.fee_amount += amount_to_be_deferred
						next_schedule.save()
					else:
						time_to_add = CalendarpaymentsUtils.get_timedelta(schedule.service.schedule_frequency)
						next_date = schedule.payment_date + time_to_add
						next_schedule = Schedule(
							payment_date = next_date,
							fee_amount = amount_to_be_deferred,
							serviceId = schedule.service
						)
						next_schedule.save()

					schedule.fee_amount -= amount_to_be_deferred
					schedule.is_paid = True
					schedule.save()

			elif schedule['is_active'] == True and schedule['is_paid'] == True:
				schedule.is_active = False
				schedule.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

