from django.shortcuts import redirect, render
from .models import User
from django.http import HttpResponse
from .module import *
from .datacontrol import *

# USER
# 메인
def cusmainpage(request):
    return render(request, 'customermain.html')

# 회원가입
def signuppage(request):
    return render(request, 'signup.html')

def signup(request):
    if request.method == 'POST':
        user = User()
        user.name = request.POST['name']
        user.phone = request.POST['phonenumber']
        user.password = request.POST['password']
        user.address = request.POST['address']   # 모델에 추가해야함.
        user.card = request.POST['card']  # 모델에 추가해야 함.
        user.save()

    return redirect('cm')

# 로그인
def loginpage(request):
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        login = Login_main()
        
        try:
            login._user_login_init(int(request.POST['phonenumber']),request.POST['password'])
        except:
            pass

    return redirect('uolp')

# 이전 주문내역 불러오기
def userorderlistpage(request):
    return render(request, 'userorderlist.html')

def index(request):
    user = User.objects.all()
    context = {'user':user}

    return render(request, 'userorderlist.html', context)

# 디너종류 고르기
def dfpage(request):
    return render(request, 'dinnerfood.html')

# 디너스타일 고르기
def dspage(request):
    return render(request, 'dinnerstyle.html')

# 추가사항 고르기
def addpage(request):
    return render(request, 'addition.html')

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

    return redirect('op')


