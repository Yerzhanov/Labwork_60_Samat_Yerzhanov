from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from common.views import TitleMixin
from django.views.generic.list import ListView

from orders.models import Order


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

class OrderDetailView(DetailView):
    template_name = 'order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f"Магазин - Заказ №{self.object.id}"
        return context



class OrderListView(TitleMixin, ListView):
    template_name = 'orders.html'
    title = 'Заказы'
    queryset = Order.objects.all()
    ordering = ('-id')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)
