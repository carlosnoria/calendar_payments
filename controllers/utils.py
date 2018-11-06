# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
class CalendarpaymentsUtils():

    def get_timedelta(frequency):
        time_to_add = timedelta(microsecond=1)
        if frequency == 'Diario':
            time_to_add = timedelta(days=1)
        elif frequency == 'Semanal':
            time_to_add = timedelta(weeks=1)
        elif frequency == 'Quincenal':
            time_to_add = timedelta(weeks=2)
        elif frequency == 'Mensual':
            time_to_add = relativedelta(months=+1)
        elif frequency == 'Bimensual':
            time_to_add = relativedelta(months=+2)
        elif frequency == 'Trimestral':
            time_to_add = relativedelta(months=+3)
        elif frequency == 'Semestral':
            time_to_add = relativedelta(months=+6)
        elif frequency == 'Anual':
            time_to_add = relativedelta(years=+1)

        return time_to_add