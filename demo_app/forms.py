from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import NumberInput
from django.contrib.auth.models import User
from .models import Customers



class RangeInput(NumberInput):
    input_type = 'range'
    input_oninput = "document.getElementById('output').value=this.value"

class InputForm(forms.ModelForm):

    limit_balance = forms.IntegerField(widget=RangeInput(),min_value=0,max_value=200000)
    bill_amt_1 = forms.IntegerField(widget=RangeInput(), min_value=-200000, max_value=100000)
    pay_amt_1 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_2 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_3 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_4 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_5 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_6 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)


    class Meta:
        model = Customers
        exclude = ['id','result','proba','registered_date']
        widgets = {
        'last_name':forms.TextInput(attrs={'placeholder':'last_name'}),
        'first_name':forms.TextInput(attrs={'placeholder':'first_name'})
        }


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='名前を入力')
    last_name = forms.CharField(max_length=30, required=True, help_text='苗字を入力')
    email = forms.EmailField(max_length=254, help_text='有効なEmailアドレス')

    class Meta:
        model = User
        fields = ('username','last_name','first_name','email', 'password1','password2')
