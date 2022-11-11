from django.shortcuts import redirect, render
from .models import User
from django.http import HttpResponse
from .module import *
from .datacontrol import *

# EMPLOYEE
# 메인 + 로그인
def emmainpage(request):
    return render(request, 'employeemain.html')

    # 배달직원 - 배달 조회 페이지는 'edep'입니다.
    # 요리직원 - 재고조회랑 주문조회 직원관리 선택 페이지는 'ecp'입니다.
def emlogin(request):
    if request.method == 'POST':
        _login = Login_main()
        data=request.session["user"]=_login._user_login_init(int(request.POST['phonenumber']),request.POST['password']) # session에 로그인 정보 저장
        if isinstance(request.session["user"],int): ## 오류가 난 경우 로그인 다시
            return redirect('em') ## 오류코드에 따른 오류 메세지 출력하는거 구현필요
        if data[2] == 2:
            return redirect('edep') ## 배달 직원 페이지로
        else:
            return redirect('ecp')

# 회원가입
def emsignuppage(request):
    return render(request, 'em_signup.html')

def emsignup(request):
    if request.method == 'POST':
        user = Employee()
        user.name = request.POST['name']
        user.phone = request.POST['phonenumber']
        user.password = request.POST['password']
        job = request.POST['job'] #cook: 조리, delivery: 배달, manage: 관리
        if job =="manage":
            user.type = 0
        elif job =="cook":
            user.type = 1
        elif job =="delivery":
            user.type = 2
        else:
            print("Type Error")
            return redirect('eep')
        user.save()
    return redirect('eep')



# 로그인
# def emloginpage(request):
#    return render(request, 'em_login.html')


# 선택창
def emchoosepage(request):
    return render(request, 'em_choose.html')

# root 권한 확인
def root_check(request):
    if request.session["user"][2] != 0:
        return redirect('ecp') ##root 권한 없을경우 선택 불가
    return redirect('eep')

# 재고 조회
def emstockpage(request):
    return render(request, 'em_stock.html')

def emstock(request):
    users = User()
    user
    context = {'users':users}

    return render(request, 'em_stock.html', context)

# 주문 조회
def emcookpage(request):
    
    return render(request, 'em_cook.html')


def emcook(request):
    data = get_currunt_order_list()
    users = list()
    for i in data:
        _ = User()
        _.time = i[0]
        for j in i:
            pass # Dinner 변환 구현되면 입력예정
        users.append(_)
    
    
    context = {'users':users}
    # 배달 시간은 time, 디너 종류는 food, 디너 스타일은 style, 추가사항은 add입니다.
    # '' 안의 'users'는 html안 이름이니 바꾸지 말아주세요. 

    return render(request, 'em_cook.html', context)

# 직원 관리
def emempage(request):
    return render(request, 'em_employee.html')

def emem(request):
    users = User.objects.all()
    context = {'users':users}
    
    return render(request, 'em_employee.html', context)

# 배달 조회
def emdeliverypage(request):
    return render(request, 'em_delivery.html')

def emdelivery(request):
    users = User.objects.all()
    context = {'users':users}
    
    return render(request, 'em_delivery.html', context)