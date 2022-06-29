from django.contrib import admin
from .models import Income, IncomeItem

# TODO add IncomeItems register
admin.site.register(Income)
admin.site.register(IncomeItem)
