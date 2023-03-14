from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from products.forms import *
from products.models import ProductCategory, Product, Basket
from django.db.models.functions import Lower
from common.views import TitleMixin

class IndexView(TitleMixin, TemplateView):
    template_name = 'index.html'
    title = 'Магазин'


class ProductsListView(TitleMixin, ListView):
     model = Product
     template_name = 'products.html'
     paginate_by = 6
     paginate_orphans = 1
     title = 'Каталог товаров'
     ordering = ['name']

     def get(self, request, *args, **kwargs):
         self.form = self.get_search_form()
         self.search_value = self.get_search_value()
         return super().get(request, *args, **kwargs)

     def get_queryset(self):
         queryset = super(ProductsListView, self).get_queryset().order_by(Lower('name'))
         category_id = self.kwargs.get('category_id')
         if self.search_value:
             query = Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value)
             queryset = queryset.filter(query)
         return queryset.filter(category_id=category_id) if category_id else queryset

     def get_context_data(self, *, object_list=None, **kwargs):
         context = super(ProductsListView, self).get_context_data(object_list=object_list, **kwargs)
         context['form'] = self.form
         context['categories'] = ProductCategory.objects.all().order_by('-name')
         if self.search_value:
             context['query'] = urlencode({'search': self.search_value})
         return context

     def get_search_form(self):
         return SimpleSearchForm(self.request.GET)

     def get_search_value(self):
         if self.form.is_valid():
             return self.form.cleaned_data['search']
         return None


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_update.html'

    def get_success_url(self):
        return reverse_lazy('product_view', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        context['title'] = 'Магазин - Просмотр товара'
        return context

class ProductDetailView(DetailView):
    template_name = 'product_view.html'
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_add.html'
    extra_context = {'title': 'Добавить товар'}
    success_url = reverse_lazy('products:index')

class ProductDeleteView(DeleteView):
    template_name = 'product_confirm_delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('index')

class CategoryCreateView(CreateView):
    model = ProductCategory
    form_class = CategoryForm
    template_name = 'category_add_view.html'
    extra_context = {'title': 'Добавить категорию'}
    success_url = reverse_lazy('products:index')


# class BasketCreateView(CreateView):  #Ломается логика при попытке перевода на классовое представление
#     model = Basket
#
#     def post(self, request, *args, **kwargs):
#         product = Product.objects.get(id=self.kwargs.get('product_id'))
#         baskets = Basket.objects.filter(user=request.user, product=product)
#
#         if not baskets.exists():
#             pass

@login_required()
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required()
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


