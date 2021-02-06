from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, UpdateView
from stock_admin.models import Stock


class BaseStockFormView(FormView):

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.user = self.request.user
        return super().form_valid(form)


class StockCreate(CreateView, BaseStockFormView):
    model = Stock
    fields = ('ticker', 'shares', 'purchase', 'buy_target', 'sell_target')
    success_url = reverse_lazy('portfolio')
    template_name = 'stock_form.html'


class StockUpdate(UpdateView, BaseStockFormView):
    model = Stock
    fields = ('shares', 'purchase', 'buy_target', 'sell_target')
    success_url = reverse_lazy('portfolio')
    template_name = 'stock_form.html'


class StockDelete(DeleteView):
    model = Stock
    success_url = reverse_lazy('portfolio')
    template_name = 'stock_confirm_delete.html'
