from django.contrib import admin

from .models import Stock


class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'stock_name', 'shares',
                    'purchase', 'current')
    fields = ['ticker', 'purchase', 'user', 'shares', 'is_default',
              'current', 'sell_target', 'buy_target']


admin.site.register(Stock, StockAdmin)
