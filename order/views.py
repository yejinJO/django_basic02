from django.db.models.query import QuerySet
from product.views import ProductCreate
from .forms import RegisterForm
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .models import Order

# Create your views here.

class OrderCreate(FormView):
   # 화면은 따로 구연할 필요 없기 때문에 template_name = 은 생략
    form_class = RegisterForm
    success_url = '/product/'

    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))

    def get_form_kwargs(self, **kwargs):
        # form을 생성할 때 어떤 인자값을 전달해서 만들건지를 결정하는 함수
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            # 기존에 있던 인자 값에다가 request를 포함하겠다
            'request' : self.request
        })
        return kw

class OrderList(ListView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order_list' # template에서 사용하는 default명은 'object_list' 임

    # order에 views.py에 model을 지정을 해줘서 타인의 주문 정보도 확인할 수 있게 됨
    # 현재 로그인한 사용자의 주문 정보 data만 가져올 수 있도록 queryset 사용하여 보안 높이기
    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(fcuser__email = self.request.session.get('user'))
        return queryset