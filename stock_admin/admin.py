from django.contrib import admin

from .models import Stock


class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'ticker', 'shares')


admin.site.register(Stock, StockAdmin)
