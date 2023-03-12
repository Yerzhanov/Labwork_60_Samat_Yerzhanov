from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from products.forms import *
from products.models import ProductCategory, Product, Basket
from django.db.models.functions import Lower


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Магазин'
        return context


class ProductsListView(ListView):
     model = Product
     template_name = 'products.html'
     paginate_by = 6

     def get_queryset(self):
         queryset = super(ProductsListView, self).get_queryset().order_by(Lower('name'))
         category_id = self.kwargs.get('category_id')
         return queryset.filter(category_id=category_id) if category_id else queryset

     def get_context_data(self, *, object_list=None, **kwargs):
         context = super(ProductsListView, self).get_context_data()
         context['title'] = 'Каталог товаров'
         context['categories'] = ProductCategory.objects.all().order_by('-name')
         return context


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


def product_view(request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        return render(request, 'product_view.html', {'product': product})


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_add.html'
    extra_context = {'title': 'Добавить товар'}
    success_url = reverse_lazy('products:index')

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


