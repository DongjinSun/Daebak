from django.shortcuts import redirect, render
from .models import User
from django.http import HttpResponse
from .module import *
from .datacontrol import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

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
            if err == -1:
                messages.warning(request,"이미 있는 계정입니다.")
            elif err == -10:
                messages.warning(request,"데이터를 가져오지 못했습니다. 다시 시도해주세요.")
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
    state_l=["주문완","조리중","배달준비","배달중","배달완료"]
    if request.session["user"]:
        name = request.session["user"][0]
    else:
        name = "Anonymous User"
    temp = request.session["user"][2]
    temp2 = OrderList.objects.filter(user=request.session["user"][1])
    #for test
    print("request.session[user][2] is ", temp)
    print("above is ", temp2)
    #for test end
    for i,j in zip(temp,temp2):
        _ = Dinner_main.dinner_reverse(i[0])
        j.food = _[0]
        j.num = [1]
        j.style = _[2]
        j.add = _[3]
        j.state = state_l[j.state]
    return render(request, 'userorderlist.html', {'user_name': name,'users':temp2})

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
        request.session["base"] = Dinner_main.dinner_convert(request.session["dinner_menu"])
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
    del request.session["dinner_menu"]
    del request.session["dinner_style"]
    del request.session["addition"]
    del request.session["base"]
    
    if request.POST.get('go') == '1':
            return redirect('dfp')
    elif request.POST.get('go') == '2':
            return redirect('op')
            
# 주문
def orderpage(request):
    #~~~# 
    dinnerMain = Dinner_main()
    print(dinnerMain.additional_list)
    order = list(request.session["order"])
    money = 0
    for length in range (len(order)):
        money += dinnerMain.cal_dinner_price(dinnerMain, order[length]) # request.session["order"]: order list
    print("total money is ", money)
    #~~~#
    
    print(request.session["order"])
    print(request.session["user"][0],
          request.session["user"][1],
          request.session["user"][3] )
    request.session["orderObject"] = [["name","phonenumber","addr","card"],"13:00","additionalOrder","dinnerData"] # <=== 미리 선언하자.
    dinnerData = dinnerMain.make_dinner_data(dinnerMain, request.session["order"])
    print("디너 데이터는 다음과 같습니다: ", dinnerData)
    #들어가야 할 내용들: 유저정보 + 시간 + 추가요청사항 + 디너정보
    #밥먹고하자...  
    #~~~#
    #request.session["name"] = request.POST["name"]
    


    #~~~#
    return render(request, 'order.html') # {money = 'money'} <- context로 반환? 

@csrf_exempt
def order(request):
    orderMain = Order_main
    #dinner data: 고객 정보 + 배달 시간 + 배달요청사항 + 디너 정보
    #출력 형식: [3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]
    #order 리턴값: [["name", "phnum", "addr"], "13:00", "additional", dinner Data]
    ## 세부 구현은 나중에.. 
    if request.method == 'POST':
        #print("for test, rq.session[user] = ", request.session["user"])
        user = CurruntOrder()
        user.name = request.POST['name']
        user.phone = int(request.POST['phonenumber'])
        user.address = request.POST['address']
        #user.card = request.POST['card']  # 모델에 추가해야 함.
        deliverytime = request.POST['deliverytime']
        user.field_id = 7 ## field_id 
        user.save()
        order = OrderList()
        order.name = request.session["user"][1]
        for i in request.session["order"]:
            order.ordernum = listToString(i)
            order.price = 0 # price 넣기
            order.info = request.POST['want']
            order.state = 0
            
        ## currunt order state에 넣는거 구현
    return
        
        
        
        dinnerData = [[3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]] # for test
        #orderMain.makeOrder()
        #orderData = orderMain.makeOrder(["name", "phnum", "addr"], "13:00", "추가요청사항", dinnerData) # for test
        orderData = [["name", "phnum", "addr"], "13:00", "추가요청사항", dinnerData]
        
        return redirect('cm')
        #return render(request, 'customermain.html', {'user_name': name})


