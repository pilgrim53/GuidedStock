import json

import yahoo_fin.stock_info as si
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import _get_queryset
from django.views.generic import CreateView, DeleteView, UpdateView
from stock_admin.models import Stock


class JsonNotFound(Exception):

    def __init__(self):
        Exception.__init__(self, 'Record not found')


# replacement for django.shortcuts.get_object_or_404()
# allows json to be returned with a 404 error
def get_object_or_json404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise JsonNotFound()


def render_to_json_response(context, **response_kwargs):
    # returns a JSON response, transforming 'context' to make the payload
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(convert_context_to_json(context), **response_kwargs)


def convert_context_to_json(context):
    # convert the context dictionary into a JSON object
    # note: this is *EXTREMELY* naive; in reality, you'll need
    # to do much more complex handling to ensure that arbitrary
    # objects — such as Django model instances or querysets
    # — can be serialized as JSON.
    return json.dumps(context)


# a mixin to add AJAX support to a form
# must be used with an object-based FormView (e.g. CreateView)
class AjaxFormResponseMixin(object):
    def get_object(self, queryset=None):
        return get_object_or_json404(self.model, pk=self.kwargs['pk'])

    def form_invalid(self, form):
        return render_to_json_response(form.errors, status=400)

    def form_valid(self, form):

        # save
        self.object = form.save()

        # initialize an empty context
        context = {}

        # return the context as json
        return render_to_json_response(self.get_context_data(context))


class StockCreate(AjaxFormResponseMixin, CreateView):
    model = Stock
    fields = ('ticker', 'shares', 'purchase', 'buy_target', 'sell_target')

    def get_context_data(self, context):
        context['success'] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            self.object = stock = self.model.objects.get(
                ticker=form.instance.ticker, user=self.request.user)
            if form.instance.shares and form.instance.purchase:
                stock.purchase = (stock.purchase * stock.shares) + \
                    (form.instance.shares * form.instance.purchase)
                stock.shares += form.instance.shares
                stock.purchase /= stock.shares
            if form.instance.buy_target:
                stock.buy_target = form.instance.buy_target
            if form.instance.sell_target:
                stock.sell_target = form.instance.sell_target
            stock.save()
            # initialize an empty context
            context = {}

            # return the context as json
            return render_to_json_response(self.get_context_data(context))
        except Stock.DoesNotExist:
            return super().form_valid(form)


class StockUpdate(AjaxFormResponseMixin, UpdateView):
    model = Stock
    fields = ('shares', 'purchase', 'buy_target', 'sell_target')

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return render_to_json_response(self.get_context_data())

    def get_context_data(self, *kwargs):
        obj = self.get_object()
        return serializers.serialize('json', [obj, ])


class StockDelete(AjaxFormResponseMixin, DeleteView):
    model = Stock

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return render_to_json_response(self.get_context_data())

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then return json response.
        """
        self.object = self.get_object()
        self.object.delete()
        return render_to_json_response({'success': 'true'})

    def get_context_data(self, *kwargs):
        obj = self.get_object()
        obj.update_stock()
        return serializers.serialize('json', [obj, ])


def get_fundamentals(request, ticker):
    obj = si.get_quote_table(ticker)
    return JsonResponse(json.dumps(obj, allow_nan=True), safe=False)
