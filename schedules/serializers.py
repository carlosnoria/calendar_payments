# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import *
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta, date

class UserAdminSerializer(serializers.ModelSerializer):
	id		= serializers.IntegerField(read_only=True)

	class Meta:
		model = UserAdmin
		fields = ('id', 'document', 'email', 'is_active', 'created',)

class UserClientSerializer(serializers.ModelSerializer):
	id		= serializers.IntegerField(read_only=True)

	class Meta:
		model = userClient
		fields = ('id', 'name', 'document', 'phone', 'phone2', 'email', 'is_active', 'created',)

class ServiceSerializer(serializers.ModelSerializer):
	id 								= serializers.IntegerField(require=False, read_only=True)
	clientId						= UserClientSerializer(require=False, read_only=True, source='clientId')
	service_fees_summary			= serializers.SerializerMethodField()
	
	"""paid_fees_amount				= serializers.IntegerField(require=False, read_only=True, source='get_paid_fees_amount')
				unpaid_fees_amount 				= serializers.IntegerField(require=False, read_only=True, source='get_unpaid_fees_amount')
				fees_to_pay_amount				= serializers.IntegerField(require=False, read_only=True, source='get_fees_to_pay_amount')
				discarded_fees_unpayed_amount	= serializers.IntegerField(require=False, read_only=True, source='get_discarded_fees_unpayed_amount')"""

	@static_method
	def setup_eager_loading(qs):
		qs = qs.select_related('clientId').prefetch_related('schedule_set')
		return qs

	def get service_fees_summary(self, obj):
		today = datetime.today().date()
		schedules = obj.schedule_set.all()
		amount_dic ={}
		paid_fees = schedules.filter(is_payed=True)
		amount_dic['paid_fees_amount'] = paid_fees.aggregate(amount=Sum('fee_amount'))['amount']
		unpaid_fees= schedules.filter(is_payed=False, payment_date__lte=today)
		amount_dic['unpaid_fees_amount'] = unpaid_fees.aggregate(amount=Sum('fee_amount'))['amount']
		fees_to_be_paid = schedules.filter(is_payed=False, payment_date__gt=today)
		amount_dic['fees_to_be_paid_amount'] = fees_to_be_paid.aggregate(amount=Sum('fee_amount'))['amount']
		discarded_unpaid_fees = schedules.filter(is_active=False, is_payed=False)
		amount_dic['discarded_unpaid_fees_amount'] = discarded_unpaid_fees.aggregate(amount=Sum('fee_amount'))['amount']

		return amount_dic

	class Meta:
		model = Service
		service_fees_summary
		fields = ('id', 'number_of_fees', 'schedule_frequency', 'start_date', 'is_active', 'observations',
		 'created', 'clientId', 'service_fees_summary',)
		"""fields = ('id', 'number_of_fees', 'schedule_frequency', 'start_date', 'is_active', 'observations',
								 'created', 'clientId', 'paid_fees_amount', 'unpaid_fees_amount', 'fees_to_pay_amount',
								 'discarded_fees_unpayed_amount',)"""

class ServicePostSerializer(serializers.ModelSerializer):
	id 		= serializers.IntegerField(require=False, read_only=True)

	class Meta:
		model = Service
		fields = ('id', 'number_of_fees', 'schedule_frequency', 'start_date', 'is_active', 'observations',
		 'created', 'clientId', 'created_by',)

class ScheduleSerializer(serializers.ModelSerializer):
	id 			= serializers.IntegerField(require=False, read_only=True)
	clientId	= UserClientSerializer(read_only=True, required=False, source='serviceId.clientId')

	@static_method
	def setup_eager_loading(qs):
		qs = qs.select_related('serviceId__clientId')
		return qs

	class Meta:
		model = Schedule
		fields = ('id', 'payment_date', 'fee_amount', 'is_active', 'is_payed', 'clientId', 'serviceId',)

class SchedulePostSerializer(serializers.ModelSerializer):
	id 			= serializers.IntegerField(require=False, read_only=True)

	class Meta:
		model = Schedule
		fields = ('id', 'payment_date', 'fee_amount', 'is_active', 'is_payed', 'serviceId',)
