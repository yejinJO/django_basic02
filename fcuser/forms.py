from django import forms
from .models import Fcuser
from django.contrib.auth.hashers import check_password,make_password

class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required' : '이메일을 입력해주세요'
        },
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )
    re_password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label='비밀번호 확인'
    )

    def clean(self):
        cleaned_data = super().clean() # clean 함수가 유효성 검사를 한후 cleaned_data를 반환함
        email = cleaned_data.get("email")
        password = cleaned_data.get('password') # cleaned_data에는 form 데이터들이 dictionary 형태로 저장됨
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('password','비밀번호가 서로 다릅니다')
                self.add_error('re_password','비밀번호가 서로 다릅니다')
            else:
                fcuser = Fcuser(
                    email = email,
                    password = make_password(password)
                )
                fcuser.save()

class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required' : '이메일을 입력해주세요'
        },
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                fcuser = Fcuser.objects.get(email=email)
            except Fcuser.DoesNotExist:
                self.add_error('email', '이메일이 없습니다')
                return

            if not check_password(password, fcuser.password):
                self.add_error('password', '비밀번호가 틀렸습니다')
            else:
                self.email = fcuser.email