from django.shortcuts import render, redirect
from .forms import InputForm
from .models import Customers
from sklearn.externals import joblib
import numpy as np

# モデルの読み込みはグローバルで宣言しておく。まいかい読み込まないように。
loaded_model = joblib.load('demo_app/demo_model.pkl')

# Create your views here.
def index(request):
    return render(request, 'demo_app/index.html',{})

def menu(request):
    return render(request, 'demo_app/menu.html',{})

def input_form(request):

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save() # 入力された値を保存
            return redirect('result')
    else:
        form = InputForm()
        return render(request, 'demo_app/input_form.html',{'form':form})

def result(request):

    comment1 = 'まあまあ'
    comment2 = 'やばい'
    comment3 = 'よい'
    comment4 = 'あやしい・・・'

    # DBからデータを取得
    _data = Customers.objects.order_by('id').reverse().values_list('limit_balance', 'sex', 'education', 'marriage', 'age', 'pay_0', 'pay_2', 'pay_3', 'pay_4', 'pay_5', 'pay_6', 'bill_amt_1', 'pay_amt_1', 'pay_amt_2', 'pay_amt_3', 'pay_amt_4', 'pay_amt_5', 'pay_amt_6')
    x = np.array(_data[0])
    y = loaded_model.predict([x])
    y_proba = loaded_model.predict_proba([x])
    y_proba = y_proba *100
    # 分類結果によって分岐
    # 自信度によって分岐
    # 分類結果が0の場合
    # 自信度が0.75以上　→コメント1
    # 自信度が0.75未満 →コメント2
    # 分類結果が1の場合
    # 自信度が0.75以上　→コメント3
    # 自信度が0.75未満 →コメント4

    class_result = y[0]
    proba_result = y_proba[0][class_result]
    rounded_proba = round(proba_result, 2)
    comment=''
    if (0 == class_result):
        if rounded_proba > 75:
            comment = comment1
        else:
            comment = comment2
    else:
        if rounded_proba > 75:
            comment = comment3
        else:
            comment = comment4

    #推論結果を保存
    customer = Customers.objects.order_by('id').reverse()[0]
    customer.result = class_result
    customer.proba = rounded_proba
    customer.comment = comment
    customer.save()

    return render(request, 'demo_app/result.html', {'y':y[0],'y_proba':rounded_proba,'comment':comment})

def history(request):

    if(request.method == 'POST'):
        d_id = request.POST
        d_customer = Customers.objects.filter(id=d_id['d_id'])
        print(d_customer)
        d_customer.delete()
        customers = Customers.objects.all()
        return render(request, 'demo_app/history.html',{'customers':customers})
    else:
        customers = Customers.objects.all()
        return render(request, 'demo_app/history.html',{'customers':customers})

def caliculate(request):
    if request.method == 'POST':
        nums = request.POST
        answer = int(nums['num1']) + int(nums['num2'])
        print(answer)
        return render(request, 'demo_app/caliculate.html', {'answer':answer})
    else:
        return render(request, 'demo_app/caliculate.html', {})
