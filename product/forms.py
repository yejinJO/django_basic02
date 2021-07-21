from django import forms
from .models import Product


class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required' : '상품명 입력해주세요'
        },
        max_length=64, label='상품명'
    )
    price = forms.IntegerField(
        error_messages={
            'required' : '상품가격를 입력해주세요'
        }, label='상품가격'
    )
    description = forms.CharField(
        error_messages={
            'required' : '상품설명를 입력해주세요'
        }, label='상품설명'
    )
    stock = forms.IntegerField(
        error_messages={
            'required' : '재고를 입력해주세요'
        }, label='재고'
    )

    def clean(self):
        cleaned_data = super().clean() # clean 함수가 유효성 검사를 한후 cleaned_data를 반환함
        name = cleaned_data.get("name")
        price = cleaned_data.get('price') # cleaned_data에는 form 데이터들이 dictionary 형태로 저장됨
        description = cleaned_data.get('description')
        stock = cleaned_data.get('stock')

        if name and price and description and stock:
            product = Product(
                name = name,
                price = price,
                description = description,
                stock = stock
            )
            product.save()