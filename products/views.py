from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.forms import *
from products.models import ProductCategory, Product, Basket
from users.models import User


def index(request):
    context = {
        'title': 'Магазин',
    }
    return render(request, 'index.html', context)


def products(request):
    context = {
        'title': 'Товары',
        'products': Product.objects.all().order_by('name'),
        'categories': ProductCategory.objects.all().order_by('name'),
    }
    return render(request, 'products.html', context)


def product_view(request, product_pk):
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
                              {'product': product , 'form': form, 'error': 'Неправильно введенные данные'})

def product_add(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product_add.html', {'form': form})
    else:
        form = ProductForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'product_add.html', context={'form': form})
        else:
            product = Product.objects.create(**form.cleaned_data)
            return redirect('products:index', pk=product.pk)



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


