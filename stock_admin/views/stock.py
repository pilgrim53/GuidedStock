from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, UpdateView
from stock_admin.models import Stock


class BaseStockFormView(FormView):

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.user = self.request.user
        return super().form_valid(form)


class BaseStockView:
    success_message = ""

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return super().get_success_url()


class StockCreate(CreateView, BaseStockFormView, BaseStockView):
    model = Stock
    fields = ('ticker', 'shares', 'purchase', 'buy_target', 'sell_target')
    success_url = reverse_lazy('portfolio')
    template_name = 'stock_form.html'
    success_message = "Stock have been created."

    def form_valid(self, form):
        try:
            self.object = stock = Stock.objects.get(
                ticker=form.instance.ticker, user=self.request.user)
            stock.purchase = (stock.purchase * stock.shares) + \
                (form.instance.shares * form.instance.purchase)
            stock.shares += form.instance.shares
            stock.purchase /= stock.shares
            stock.buy_target = form.instance.buy_target
            stock.sell_target = form.instance.sell_target
            stock.save()
            return HttpResponseRedirect(self.get_success_url())
        except Stock.DoesNotExist:
            return super().form_valid(form)


class StockUpdate(UpdateView, BaseStockFormView, BaseStockView):
    model = Stock
    fields = ('shares', 'purchase', 'buy_target', 'sell_target')
    success_url = reverse_lazy('portfolio')
    template_name = 'stock_form.html'
    success_message = "Stock have been updated."


class StockDelete(DeleteView, BaseStockView):
    model = Stock
    success_url = reverse_lazy('portfolio')
    template_name = 'stock_confirm_delete.html'
    success_message = "Stock have been deleted."
