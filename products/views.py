from django.shortcuts import render, redirect, get_object_or_404
from products.forms import *
from products.models import ProductCategory, Product


def index(request):
    context = {
        'title': 'Магазин',
    }
    return render(request, 'index.html', context)


def products(request):
    context = {
        'title': 'Товары',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products.html', context)


def product_view(request,product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        if request.method == 'GET':
            form = ProductForm(instance=product)
            return render(request, 'product_view.html', {'product': product, 'form': form})
        else:
            try:
                form = ProductForm(request.POST, instance=product)
                form.save()
                return redirect('index')
            except ValueError:
                return render(request, 'product_view.html',
                              {'product': product , 'form': form, 'error': 'Неправильно введеные данные'})

