from fcuser.models import Fcuser
from product.models import Product
from django import forms
from .models import Order
from django.db import transaction


class RegisterForm(forms.Form):

    # 생성자함수
    # requst에 전달하기 위해서 생성자 함수를 생성
    # product views의 productDetail에서 form을 생성하는 부분이 있습니다!
    # 그리고 order의 views.py에서 request를 처리한다
    def __init__(self, request, *args, **kwargs):
        # 기존에 있던 생성자를 사용할 수 있도록 super()에서 불러온다!
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required' : '수량을 입력해주세요'
        }, label='수량'
    )
    # 실제로 입력받는 값이 아니라 선택한 상품의 아이디를 받아오기 때문에 fcuser는 불필요
    product = forms.IntegerField(
        error_messages={
            'required' : '상품을 입력해주세요'
        }, label='상품', widget = forms.HiddenInput 
        # forms.HiddenInput : 실제로 사용자에게 입력 받지 않기 때문에 보여지지 않음, 
        # 유저로부터 정보를 직접 입력 받는 것이 아니라 브라우저 내에서 자동으로 입력해주기 위함<input type="hidden" ...>
    )

    def clean(self):
        cleaned_data = super().clean() # clean 함수가 유효성 검사를 한후 cleaned_data를 반환함
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')

        # print(self.request.session)
        fcuser = self.request.session.get('user') # 유저 이메일을 가지고 옴 
        
        if quantity and product and fcuser:
            with transaction.atomic(): # 트랜젝션의 원자성(all or nothing)을 구현 : 하나의 단위로 수행
                prod = Product.objects.get(pk=product)
                order = Order(
                    quantity = quantity,
                    product = Product.objects.get(pk=product),
                    fcuser = Fcuser.objects.get(email=fcuser)
                )
                order.save() # 주문 시 주문정보가 저장이 되고
                prod.stock -= quantity # 주문 시 주문한 만큼 재고에서 수량이 차감됨
                prod.save()
        else:
            # 실패했을 경우에
            # 템플릿 이름이 지정되지 않아 이대로면 오류가 난다
            # 주문하기 페이지를 따로 만들지 않기 때문에 템플릿을 만들필요는 없다!
            # Order의 views에 함수를 만들고 추가하기!(self.product = product)
            self.product = product
            self.add_error('quantity', '값이 업습니다')
            self.add_error('product', '값이 업습니다')