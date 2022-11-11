from django.shortcuts import redirect, render
from .models import User
from django.http import HttpResponse
from .module import *
from .datacontrol import *
from django.contrib import messages

# USER
# 메인
def cusmainpage(request):
    try:
        request.session["user"]
    except:
        request.session["user"]=None
    return render(request, 'customermain.html')

# 로그아웃
def logout(request):
    del request.session["user"]

    return redirect('cm')

# 회원가입
def signuppage(request):
    return render(request, 'signup.html')

def signup(request):
    _login = Login_main()
    if request.method == 'POST':
        user = User()
        user.name = request.POST['name']
        user.phone = request.POST['phonenumber']
        err=_login._login_check(user.phone)
        if err:
            print("errer=",err)
            return redirect('sp')
        user.password = request.POST['password']
        user.address = request.POST['address']   # 모델에 추가해야함.
        user.card = request.POST['card']  # 모델에 추가해야 함.
        user.save()
    return redirect('cm')

# 로그인
def loginpage(request):
    if request.session["user"] != None:
        return redirect("uolp")
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST': 
        _login = Login_main()
        request.session["user"]=_login._user_login_init(int(request.POST['phonenumber']),request.POST['password']) # session에 로그인 정보 저장
        if isinstance(request.session["user"],int): ## 오류가 난 경우 로그인 다시
            if request.session["user"] == -1:
                messages.warning(request,"없는 계정입니다.")
                request.session["user"] = None
            elif request.session["user"] == -2:
                messages.warning(request,"비밀번호가 다릅니다.")
                request.session["user"] = None
            elif request.session["user"] == -10:
                messages.warning(request,"데이터를 가져오지 못했습니다. 다시 시도해주세요.")
                request.session["user"] = None
            return redirect('lp')
        else:
            return redirect('uolp')
    # else: 
    #     print("errer = ",request.session["user"])
    #     return render(request, 'login.html', {'code': request.session["user"]})
# 이전 주문내역 불러오기
def userorderlistpage(request):
    name = request.session["user"][0]
    return render(request, 'userorderlist.html', {'user_name': name})

def userorderlist(request):
    users = User.objects.all()
    context = {'users':users}

    return render(request, 'userorderlist.html', context)

# 디너종류 고르기
def dfpage(request):
    name = request.session["user"][0]
    return render(request, 'dinnerfood.html', {'user_name': name})

def df(request):
    if request.method == 'POST':
        a = request.session["user"]
        print("print",a)
    return redirect('dsp')

# 디너스타일 고르기
def dspage(request):
    name = request.session["user"][0]
    return render(request, 'dinnerstyle.html', {'user_name': name})

def ds(request):
    if request.method == 'POST':
        a = request.POST['dinnerform']

    return redirect('cp')

# 추가 주문할 건지 고르기
def cpage(request):
    return render(request, 'dinnerchoose.html')

# 수정할 추가사항 고르기
def addpage(request):
    name = request.session["user"][0]
    return render(request, 'addition.html', {'user_name': name})

def add(request):
    if request.method == 'POST':
        a = request.POST['dinnerform']
        print("a")
    return redirect('ap')

def delete(request):
    if request.method == 'POST':
        user = User()
        user.name = request.POST['name']
        user.phone = request.POST['phonenumber']
        user.password = request.POST['password']
        user.address = request.POST['address']   # 모델에 추가해야함.
        user.card = request.POST['card']  # 모델에 추가해야 함.
        user.save()

    return redirect('ap')

# 주문
def orderpage(request):
    return render(request, 'order.html')

def order(request):
    if request.method == 'POST':
        user = User()
        user.name = request.POST['name']
        user.phone = request.POST['phonenumber']
        user.password = request.POST['password']
        user.address = request.POST['address']   # 모델에 추가해야함.
        user.card = request.POST['card']  # 모델에 추가해야 함.
        user.deliverytime = request.POST['deliverytime']
        user.save()

    return redirect('cm')


