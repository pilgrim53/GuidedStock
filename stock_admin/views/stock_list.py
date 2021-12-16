from django.db import models
from django.db.models import F, Sum
from django.views.generic import ListView
from stock_admin.models import Stock


class StockListView(ListView):
    model = Stock
    template_name = 'portfolio.html'

    def get_queryset(self):
        queryset = Stock.objects.filter(
            user=self.request.user).order_by('-proximity', 'stock_name')
        if not self.request.is_ajax():
            return queryset
        else:
            for stock in queryset:
                stock.update_stock()
                stock.save()
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["investment"] = context['object_list'].aggregate(investment=Sum(F("purchase") * F("shares"),
                                                                                output_field=models.FloatField()
                                                                                ))['investment']
        context["profit"] = context['object_list'].aggregate(Sum('profit'))
        return context
