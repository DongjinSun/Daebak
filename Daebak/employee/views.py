from django.shortcuts import redirect, render
from .models import User
from django.http import HttpResponse
from .module import *
from .datacontrol import *

# EMPLOYEE
# 메인
def emmainpage(request):
    return render(request, 'employeemain.html')

# 회원가입
def emsignuppage(request):
    return render(request, 'em_signup.html')


def emsignup(request):
    if request.method == 'POST':
        user = User()
        user.name = request.POST['name']
        user.phone = request.POST['phonenumber']
        user.password = request.POST['password']
        user.address = request.POST['address']   # 모델에 추가해야함.
        user.card = request.POST['card']  # 모델에 추가해야 함.
        user.save()

    return redirect('em')

# 로그인
def emloginpage(request):
    return render(request, 'login.html')

def emlogin(request):
    if request.method == 'POST':
        login = Login_main()
        
        try:
            login._user_login_init(int(request.POST['phonenumber']),request.POST['password'])
        except:
            pass

    return redirect('uolp')