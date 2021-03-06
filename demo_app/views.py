from django.shortcuts import render, redirect
from .forms import InputForm, SignUpForm
from .models import Customers
from sklearn.externals import joblib
import numpy as np
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import json
import pandas as pd

# モデルの読み込みはグローバルで宣言しておく。まいかい読み込まないように。
anywhere = '/home/koshiba/koshiba.pythonanywhere.com/'
loaded_model = joblib.load(anywhere + 'demo_app/demo_model.pkl')

# Create your views here.
@login_required
def index(request):
    return render(request, 'demo_app/index.html',{})

@login_required
def menu(request):
    return render(request, 'demo_app/menu.html',{})

@login_required
def input_form(request):

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save() # 入力された値を保存
            return redirect('result')
    else:
        form = InputForm()
        return render(request, 'demo_app/input_form.html',{'form':form})

@login_required
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

@login_required
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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
             #入力されたデータを扱いやすい形にしてくれる
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
        return render(request, 'demo_app/signup.html',{'form':form})

@login_required
def info(request):
    # DBからデータの読み込み
    customers = Customers.objects.values_list(\
    'sex', 'education', 'marriage', 'age', 'result', 'proba')

    # データをDataFarame型に変換
    lis, cols = [], ['sex', 'education', 'marriage', 'age', 'result', 'proba']
    for customer in customers:
        lis.append(customer)
    df = pd.DataFrame(lis, columns=cols)

    # データの整形
    df['sex'].replace({1:"男性", 2:"女性"}, inplace=True)
    df['education'].replace({1:'graduate_school', 2:'university', 3:'high school', 4:'other'}, inplace=True)
    df['marriage'].replace({1:'married', 2:'single', 3:'others'}, inplace=True)
    df['result'].replace({0:'審査落ち', 1:'審査通過', 2:'その他'}, inplace=True)
    df['age'] = pd.cut(df['age'], [0,10,20,30,40,50,60,100], labels=['10代', '20代','30代','40代','50代','60代','60代以上'])
    df['proba'] = pd.cut(df['proba'], [0,75,100], labels=['要審査', '信頼度高'])

    # データのユニークな値とその数の取得
    dic_val, dic_index = {}, {}
    for col in cols:
        _val = df[col].value_counts().tolist()
        _index = df[col].value_counts().index.tolist()
        dic_val[col] = _val
        dic_index[col] = _index

    # データをJson形式に変換
    val, index = json.dumps(dic_val), json.dumps(dic_index)

    return render(request, 'demo_app/info.html',{'index':index,'val':val})

@login_required
def caliculate(request):
    if request.method == 'POST':
        nums = request.POST
        answer = int(nums['num1']) + int(nums['num2'])
        print(answer)
        return render(request, 'demo_app/caliculate.html', {'answer':answer})
    else:
        return render(request, 'demo_app/caliculate.html', {})
