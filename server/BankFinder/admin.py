from django.contrib import admin
from .models import *

admin.site.register(bank)
admin.site.register(branch)
admin.site.register(source_currency)
admin.site.register(target_currency)
admin.site.register(exchange_rate)
admin.site.register(bank_exchange_rate)

