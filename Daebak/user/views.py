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
    request.session["order"] = []
    return render(request, 'customermain.html')

# 로그아웃
def logout(request):
    request.session.clear()
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
# 이전 주문내역 불러오기
def userorderlistpage(request):
    if request.session["user"]:
        name = request.session["user"][0]
    else:
        name = "Anonymous User"
    temp = request.session["user"][2]
    order = []
    temp2 = OrderList()
    for i in temp:
        _ = dinner_reverse(i[0])
        temp2.food = _[0]
        temp2.style = _[1]
        temp2.add = _[2]
        temp2.state = 0
        order.append(temp2)
    return render(request, 'userorderlist.html', {'user_name': name,'users':order})

# 디너종류 고르기
def dfpage(request):
    if request.session["user"]:                                                 #
        name = request.session["user"][0]
    else:
        name = "Anonymous User"
    request.session["addition"]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return render(request, 'dinnerfood.html', {'user_name': name})

def df(request):
    _l = ["valnum","frenum","engnum","chanum"]
    if request.method == 'POST':
        name = request.POST["name"]
        i = _l.index(name)
        request.session["dinner_menu"]=[0,0,0,0]
        request.session["dinner_menu"][i] = int(request.POST[name])
        request.session["base"] = dinner_convert(request.session["dinner_menu"])
        if not i:
            request.session["dinner_style"] = [3]
            return redirect('ap')
        return redirect('dsp')

# 디너스타일 고르기
def dspage(request):
    if request.session["user"]:
        name = request.session["user"][0]
    else:
        name = "Anonymous User"
    return render(request, 'dinnerstyle.html', {'user_name': name})

def simnum(request):
    request.session["dinner_style"]=[0,0,0]
    request.session["dinner_style"] = [0]
    return redirect('ap')

def granum(request):
    request.session["dinner_style"]=[0,0,0]
    request.session["dinner_style"] = [1]
    return redirect('ap')

def delnum(request):
    request.session["dinner_style"]=[0,0,0]
    request.session["dinner_style"] = [2]
    return redirect('ap')


# 수정할 추가사항 고르기
def addpage(request):
    if request.session["user"]:
        name = request.session["user"][0]
    else:
        name = "Anonymous User"
    return render(request, 'addition.html', {'user_name': name})

def add(request):
    _l = ["box","pot","cup","val","pla","steak","salad","egg","bacon","bread","bag","cof","cofp","wine","wineb","champ"]
    if request.method == 'POST':
        name = request.POST["name"]
        mod = request.POST["mode"]
        if mod == "add":
            i = _l.index(name)
            request.session["addition"][i] += int(request.POST[name+mod])
            request.session["addition"]=request.session["addition"]
        else:
            i = _l.index(name)
            request.session["addition"][i] -= int(request.POST[name+mod])
            request.session["addition"]=request.session["addition"]
        return redirect('ap')
    
def addorder(request):
    _l = [x+y for x,y in zip(request.session["addition"],request.session["base"])]
    request.session["order"].append(request.session["dinner_menu"]+request.session["dinner_style"]+ _l)
    print(request.session["order"])
    request.session["order"] = request.session["order"]
    if request.POST.get('go') == '1':
            return redirect('dfp')
    elif request.POST.get('go') == '2':
            return redirect('op')
            
# 주문
def orderpage(request):
    print(request.session["order"])
    return render(request, 'order.html')

def order(request):
    if request.method == 'POST':
        # user = User()
        # user.name = request.POST['name']
        # user.phone = request.POST['phonenumber']
        # user.password = request.POST['password']
        # user.address = request.POST['address']   # 모델에 추가해야함.
        # user.card = request.POST['card']  # 모델에 추가해야 함.
        # user.deliverytime = request.POST['deliverytime']
        # user.save()

        return redirect('cm')


