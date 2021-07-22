from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Product
from .forms import RegisterForm
from order.forms import RegisterForm as OrderForm

# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list' # template에서 사용하는 default명은 'object_list' 임

class ProductCreate(FormView):
    template_name = "register_product.html"
    form_class = RegisterForm
    success_url = '/product/'

class ProductDetail(DetailView):
    template_name = "product_detail.html"
    queryset = Product.objects.all() # all로 가져와 하나씩 꺼내씀
    context_object_name = 'product'


    # 기본적으로 장고는 object_list 변수를 만들어 그 안에 해당 객체를 넣어 보내준다.
    # 변수의 이름을 바꾸는 속성이 context_object_name이고, 
    # 다른 객체들도 context에 넣어 보내고 싶다면 get_context_data 메서드를 구현하는 것으로 해결 가능
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) # ProductDetail 객체를 먼저 생성
        context['form'] = OrderForm(self.request) # 이후에 form이라는 key에 OrderForm을 넣음
        # form class를 생성하면서 request도 함께 넣게됨
        return context # context 반환