# Generated by Django 2.1.3 on 2018-11-06 15:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('fee_amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('paid_amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=True)),
                ('is_paid', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('payment_date', 'serviceId'),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('number_of_fees', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('schedule_frequency', models.CharField(choices=[('Diario', 'Diario'), ('Semanal', 'Semanal'), ('Quincenal', 'Quincenal'), ('Mensual', 'Mensual'), ('Bimensual', 'Bimensual'), ('Trimestral', 'Trimestral'), ('Semestral', 'Semestral'), ('Anual', 'Anual')], max_length=20)),
                ('start_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('observations', models.CharField(default='', max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='UserAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('document', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='UserClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('document', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=25, validators=[django.core.validators.RegexValidator(code='Invalid phone', message='Invalid phone', regex='^([+]?[0-9]+)$')])),
                ('phone2', models.CharField(default='', max_length=25, validators=[django.core.validators.RegexValidator(code='Invalid phone', message='Invalid phone', regex='^([+]?[0-9]+)$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('address', models.CharField(max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedules.UserAdmin')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='service',
            name='clientId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.UserClient'),
        ),
        migrations.AddField(
            model_name='service',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedules.UserAdmin'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='serviceId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.Service'),
        ),
    ]