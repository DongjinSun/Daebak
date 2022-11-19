from django.shortcuts import redirect, render
from .models import *
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
            elif err == -3:
                messages.warning(request,"휴대폰 번호를 올바르게 입력해주세요")
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
        request.session["user"]=_login._user_login_init(int(request.POST['phonenumber']),request.POST['password']) # session에 개인정보 저장.
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
    dinnerMain = Dinner_main 
    if request.session["user"]:
        name = request.session["user"][0]
    else:
        name = "Anonymous User"
    
    state_l=["주문완","조리중","배달준비","배달중","배달완료"]
    temp = OrderList.objects.filter(user=request.session["user"][1])
    #for test
    # print("above is ", temp)
    # for i in temp:
    #     print("temp[{}] is ".format(i), list(temp[i]))
    # print("user0",request.session["user"][0])
    # print("user1",request.session["user"][2])
    # print("user2",request.session["user"][3])
    #for test end

    for j in temp:
        tempOrderList = stringToList(j.ordernum)
        _ = dinnerMain.make_dinner_data(dinnerMain, tempOrderList)
        print(j.ordernum)
        j.num = _[0]
        j.food = _[1]
        j.style = _[2]
        j.add = _[3]
        j.state = state_l[j.state]
        
    # for j in temp:
    #     _ = Dinner_main.dinner_reverse(j.ordernum)
    #     j.food = _[0]
    #     j.num = _[1]
    #     j.style = _[2]
    #     j.add = _[3]
    #     j.state = state_l[j.state]
    # if len(temp)>10:
    #     request.session["user"][2] = 1
    return render(request, 'userorderlist.html', {'user_name': name,'users':temp})

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
        voice = request.POST.get('voicesubmit',False)
        print(voice)
        if voice:
            request.session["dinner_menu"]=[0,0,0,0]
            i = make_voice_dinner_data(voice,"menu")
            request.session["dinner_menu"][i] = 1
            request.session["base"] = Dinner_main.dinner_convert(request.session["dinner_menu"])
            if not i:
                request.session["dinner_style"] = [3]
                return redirect('ap')
            return redirect('dsp')
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

def ds(request):
    if request.method =="POST":
        voice = request.POST.get('voicesubmit',False)
        if voice:
            i = make_voice_dinner_data(voice,"style")
            if i==0:
                request.session["dinner_style"] = [0]
            elif i==1:
                request.session["dinner_style"] = [1]
            elif i==2:
                request.session["dinner_style"] = [2]
            return redirect('ap')
        _l = ["sim","gra","del"]
        name = request.POST["name"]
        i = _1.index(name)
        if i==0:
            request.session["dinner_style"] = [0]
        elif i==1:
            request.session["dinner_style"] = [1]
        elif i==2:
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
    #print("addorder = ",request.session["order"])
    request.session["order"] = request.session["order"]
    
    if request.POST.get('go') == '1':
            return redirect('dfp')
    elif request.POST.get('go') == '2':
            return redirect('op')
            
# 주문
def orderpage(request):
    #~~~# 
    dinnerMain = Dinner_main()
    orderMain = Order_main()
    #print(dinnerMain.additional_list)
    order = list(request.session["order"])
    money_l = []
    money = 0
    #print("order is !!!!!", order) # for test
    for o in order:
        _ = dinnerMain.cal_dinner_price(dinnerMain, o)
        money_l.append(_) # request.session["order"]: order list
        money += _
    print("total money is ", money) # 이 부분에서, 뒤로 갔다가 다시 로딩 시 가격이 2배가 되는 버그 존재. 

    request.session["orderObject"] = [["name","phonenumber","addr","card"],"13:00","additionalOrder","dinnerData"] # <=== 미리 선언하자.
    print("before make dinner") # for test
    dinnerData = dinnerMain.make_dinner_data(dinnerMain, request.session["order"])
    #[persons, selected_dinner, selected_style, customizated_str, money]
    orderData = orderMain.makeOrder(request.session["user"], dinnerData, "16:00", request.session["addition"]) ############### 여기부터. 
    print("after make dinner") # for test
    # print("디너 데이터는 다음과 같습니다: ", dinnerData)
    #들어가야 할 내용들: 유저정보 + 시간 + 추가요청사항 + 디너정보
    #request.session["name"] = request.POST["name"]
    time_l = orderMain.get_currunt_time(request)
    # time_l = "111111111111" # 테스트용

    for i, j in enumerate(request.session['user']): # request.session['user']에 저장된 값 확인용 코드
        print("user is ", request.session['user'][i])  # user[0] = 이름. user[1] = 전화번호. user[2] = 할인여부 user[3] = 주소. user[4] = 카드번호

    #~~~#
    context = {"arr":time_l, "dinner":dinnerData[1], "num":dinnerData[0], "style":dinnerData[2], "addition":dinnerData[3], 
                "name":request.session["user"][0], "phonenumber":request.session["user"][1], "sale":request.session["user"][2], 
                 "address":request.session["user"][3],  "card":request.session["user"][4], "price":dinnerData[4], "money":money} # price: 할인 전. dinnerData에서 받음.  money: 할인 후
    return render(request, 'order.html', {"context":context}) # {money = 'money'} <- context로 반환?  # 수정. order 전달하자. 
@csrf_exempt
def order(request):
    orderMain = Order_main()
    #dinner data: 고객 정보 + 배달 시간 + 배달요청사항 + 디너 정보
    #출력 형식: [3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]
    #order 리턴값: [["name", "phnum", "addr"], "13:00", "additional", dinner Data]
    err = orderMain.send_order_data(request)
    # print(test_)
    if err == -1:
        messages.warning(request,"주문이 마감되었습니다.")
        return redirect('op')
    elif err == -2:
        messages.warning(request,"시간을 선택해주세요")
        return redirect('op')
    elif err == -3:
        messages.warning(request,"휴대폰 번호를 입력해주세요")
        return redirect('op')
    return redirect('orderfin')
        
        
        
        # dinnerData = [[3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]] # for test
        # #orderMain.makeOrder()
        # #orderData = orderMain.makeOrder(["name", "phnum", "addr"], "13:00", "추가요청사항", dinnerData) # for test
        # orderData = [["name", "phnum", "addr"], "13:00", "추가요청사항", dinnerData]
        
        # return redirect('cm')
        # #return render(request, 'customermain.html', {'user_name': name})

def orderfinishpage(request):
    del request.session["order"]
    del request.session["time"]
    del request.session["order"]
    del request.session["addition"]
    del request.session["dinner_menu"]
    del request.session["dinner_style"]
    return render(request, 'orderfinish.html')


# 음성인식 페이지
def voiceaipage(request):
    return render(request, 'voiceai.html')