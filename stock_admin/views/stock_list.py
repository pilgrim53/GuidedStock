from django.views.generic import ListView
from stock_admin.models import Stock


class StockListView(ListView):
    model = Stock
    template_name = 'portfolio.html'

    def get_queryset(self):
        queryset = Stock.objects.filter(
            user=self.request.user).order_by('-potential', 'stock_name')
        for stock in queryset:
            stock.update_stock()
        return queryset
