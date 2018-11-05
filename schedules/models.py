# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Count, Sum

FREQUENCY_CHOICES = (
	('Diario', 'Diario'),
	('Semanal', 'Semanal'),
	('Quincenal', 'Quincenal'),
	('Mensual', 'Mensual'),
	('Bimensual', 'Bimensual'),
	('Trimestral', 'Trimestral'),
	('Semestral', 'Semestral'),
	('Anual', 'Anual'),
	)

# Create your models here.
class UserAdmin(models.Model):
	name		= models.Charfield(max_length=200)
	document	= models.Charfield(max_length=50)
	email		= models.EmailField(unique=True)
	is_active	= models.BooleanField(deafult=True)
	created		= models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('name',)

class UserClient(models.Model):
	name		= models.Charfield(max_length=200)
	document	= models.Charfield(max_length=50)
	phone       = models.CharField(
        max_length=25,
        validators=[
            RegexValidator(
                regex=r'^([+]?[0-9]+)$',
                message='Invalid phone',
                code='Invalid phone'
            ),
        ]
    )
    phone2      = models.CharField(
        max_length=25,
        default ='',
        validators=[
            RegexValidator(
                regex=r'^([+]?[0-9]+)$',
                message='Invalid phone',
                code='Invalid phone'
            ),
        ]
    )
    email		= models.EmailField(unique=True, null=True, blank=True)
    is_active	= models.BooleanField(deafult=True)
    created		= models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeingKey(UserAdmin, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
    	ordering = ('name',)

class Service(models.Model):
	service_amount		= models.FloatField(validators=[MinValueValidator(0)], default=0)
	number_of_fees		= models.IntegerField(validators=[MinValueValidator(0)], default=0)
	schedule_frecuency	= models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
	start_date			= models.DateField()
	is_active			= models.BooleanField(default=True)
	observations		= models.CharField(max_length=500, default='')
	created 			= models.DateTimeField(auto_now_add=True)
	clientId			= models.ForeingKey(UserClient, on_delete=models.CASCADE)
	created_by			= models.ForeingKey(UserAdmin, on_delete=models.SET_NULL, null=True, blank=True)

	class Meta:
		ordering = ('id',)

class Schedule(models.Model):
	payment_date 	= model.DateField()
	fee_amount		= models.FloatField(validators=[MinValueValidator(0)], default=0)
	is_active		= models.BooleanField(default=True)
	is_payed		= models.BooleanField(default=False)
	serviceId		= models.ForeingKey(Service, on_delete=models.CASCADE)

	class Meta:
		ordering = ('payment_date', 'serviceId',)





