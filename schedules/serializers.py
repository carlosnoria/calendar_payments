# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import *
from django.core.validators import MinValueValidator

class UserAdminSerializer(serializers.ModelSerializer):
    id      = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserAdmin
        fields = ('id', 'document', 'email', 'is_active', 'created',)

class UserClientSerializer(serializers.ModelSerializer):
    id      = serializers.IntegerField(read_only=True)

    class Meta:
        model = userClient
        fields = ('id', 'name', 'document', 'phone', 'phone2', 'email', 'address', 'is_active', 'created',)

class ServiceSerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(require=False, read_only=True)
    clientId                        = UserClientSerializer(require=False, read_only=True, source='clientId')
    service_fees_summary            = serializers.SerializerMethodField()
    
    @static_method
    def setup_eager_loading(qs):
        qs = qs.select_related('clientId').prefetch_related('schedule_set')
        return qs

    def get service_fees_summary(self, obj):
        today = date.today()
        schedules = obj.schedule_set.all()
        amount_dic ={}
        paid_fees = schedules.filter(is_paid=True)
        amount_dic['paid_fees_amount'] = paid_fees.aggregate(amount=Sum('fee_amount'))['amount']
        unpaid_fees= schedules.filter(is_paid=False, payment_date__lte=today)
        amount_dic['unpaid_fees_amount'] = unpaid_fees.aggregate(amount=Sum('fee_amount'))['amount']
        fees_to_be_paid = schedules.filter(is_paid=False, payment_date__gt=today)
        amount_dic['fees_to_be_paid_amount'] = fees_to_be_paid.aggregate(amount=Sum('fee_amount'))['amount']
        discarded_unpaid_fees = schedules.filter(is_active=False, is_paid=False)
        amount_dic['discarded_unpaid_fees_amount'] = discarded_unpaid_fees.aggregate(amount=Sum('fee_amount'))['amount']

        return amount_dic

    class Meta:
        model = Service
        service_fees_summary
        fields = ('id', 'number_of_fees', 'schedule_frequency', 'start_date', 'is_active', 'observations',
         'created', 'clientId', 'service_fees_summary',)

class ServicePostSerializer(serializers.ModelSerializer):
    id      = serializers.IntegerField(require=False, read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'number_of_fees', 'schedule_frequency', 'start_date', 'is_active', 'observations',
         'created', 'clientId', 'created_by',)

class ServiceMinimalPostSerializer(serializers.ModelSerializer):
    id      = serializers.IntegerField(require=False, read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'is_active', 'observations',)

class ScheduleSerializer(serializers.ModelSerializer):
    id          = serializers.IntegerField(require=False, read_only=True)
    clientId    = UserClientSerializer(read_only=True, required=False, source='serviceId.clientId')

    @static_method
    def setup_eager_loading(qs):
        qs = qs.select_related('serviceId__clientId')
        return qs

    class Meta:
        model = Schedule
        fields = ('id', 'payment_date', 'fee_amount', 'paid_amount', 'is_active', 'is_paid', 'clientId', 'serviceId',)

class SchedulePostSerializer(serializers.ModelSerializer):
    id          = serializers.IntegerField(require=False, read_only=True)

    class Meta:
        model = Schedule
        fields = ('id', 'payment_date', 'paid_amount', 'is_active', 'is_paid',)
