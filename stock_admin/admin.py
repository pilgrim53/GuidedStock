from django.urls import reverse
from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import DefaultPortfolio, Stock
from django.utils.safestring import mark_safe

User = get_user_model()


class StockAdmin(admin.ModelAdmin):
    list_display = ('users', 'ticker', 'potential', 'current', 'buy_target', 'sell_target',
                    'proximity', 'profit', 'shares', 'purchase', 'stock_name')
    fields = ['ticker', 'purchase', 'user', 'shares', 'is_default',
              'current', 'sell_target', 'buy_target']
    list_display_links = ['ticker']
    search_fields = ['user__email', 'ticker', 'stock_name']

    def users(self, obj):
        link = reverse("admin:users_user_change", args=(obj.user.id,))
        return mark_safe('<a href="%s">%s</a>' % (link, obj.user.email))


admin.site.register(Stock, StockAdmin)


@admin.register(DefaultPortfolio)
class DefaultPortfolioAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'potential', 'current', 'buy_target', 'sell_target',
                    'proximity', 'profit', 'shares', 'purchase', 'stock_name')
    fields = ['ticker', 'potential', 'shares', 'sell_target', 'buy_target']

    def get_queryset(self, request):
        return super(DefaultPortfolioAdmin, self).get_queryset(request).filter(is_default=True, user__is_superuser=True)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined', 'last_login',
                    'total_stocks_in_portfolio')
    search_fields = ['email']

    def total_stocks_in_portfolio(self, obj):
        link = reverse("admin:stock_admin_stock_changelist") + \
            '?q=%s' % obj.email  # model name has to be lowercase
        return mark_safe('<a href="%s">%s</a>' % (link, Stock.objects.filter(user=obj).count()))
