from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Product
from .forms import RegisterForm

# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list' # template에서 사용하는 default명은 'object_list' 임

class ProductCreate(FormView):
    template_name = "register_product.html"
    form_class = RegisterForm
    success_url = '/product/'

class ProductDeatil(DetailView):
    template_name = "product_detail.html"
    queryset = Product.objects.all() # all로 가져와 하나씩 꺼내씀
    context_object_name = 'product'