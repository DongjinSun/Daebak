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
    request.session["stock"] = []
    return render(request, 'customermain.html')

def anoorder(request):
    try:
        request.session["user"][0]
        return redirect('cm')
    except:
        return redirect('dfp')

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
        user.name = request.POST.get('name',False)
        if not user.name:
            messages.warning(request,"이름을 입력하세요")
            return redirect('sp')
            
        user.phone = request.POST.get('phonenumber',False)
        if not user.phone:
            messages.warning(request,"휴대폰번호를 입력하세요")
            return redirect('sp')

        err=_login._login_check(user.phone)
        if err: 
            if err == -1:
                messages.warning(request,"이미 있는 계정입니다.")
            elif err == -10:
                messages.warning(request,"데이터를 가져오지 못했습니다. 다시 시도해주세요.")
            elif err == -3:
                messages.warning(request,"휴대폰 번호를 올바르게 입력해주세요")
            return redirect('sp')

        user.password = request.POST.get('password',False)
        if not user.password:
            messages.warning(request,"비밀번호를 입력하세요")
            return redirect('sp')
            
        user.address = request.POST.get('address',False)  
        if not user.address:
            messages.warning(request,"주소를 입력하세요")
            return redirect('sp') 
        
        user.card = request.POST.get('card',False)  
        if not user.card:
            messages.warning(request,"카드번호를 입력하세요")
            return redirect('sp')
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
        try:
            phone = int(request.POST['phonenumber'])
        except:
            messages.warning(request,"휴대폰번호를 입력해주세요")
            return redirect('lp')
        
        request.session["user"]=_login._user_login_init(phone,request.POST['password']) # session에 개인정보 저장.
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
    dinnerMain = Dinner_main()
    if request.session["user"]:
        name = request.session["user"][0]
    else:
        name = "Anonymous User"
    
    state_l=["주문완료","조리중","배달준비","배달중","배달완료"]
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
        _ = dinnerMain.make_dinner_data(tempOrderList)
        j.num = _[0]
        j.food = _[1]
        j.style = _[2]
        j.add = _[3]
        j.state = state_l[j.state]
    if len(temp)>10:
        request.session["user"][2] = 1
    # for j in temp:
    #     _ = Dinner_main.dinner_reverse(j.ordernum)
    #     j.food = _[0]
    #     j.num = _[1]
    #     j.style = _[2]
    #     j.add = _[3]
    #     j.state = state_l[j.state]

    return render(request, 'userorderlist.html', {'user_name': name,'users':temp})

def reorder(request):
    if request.method =="POST":
        data = request.POST.get("ordernum",False)
        if data:
            d = list(data)
            for i,n in enumerate(d):
                d[i] = int(n)
            request.session["order"] = [d]
            request.session["stock"] = [d[5:]]
            print(request.session["stock"])
    return redirect('op')
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
            i = Dinner_main.make_voice_dinner_data(voice,"menu")
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
            i = Dinner_main.make_voice_dinner_data(voice,"style")
            if i==0:
                request.session["dinner_style"] = [0]
            elif i==1:
                request.session["dinner_style"] = [1]
            elif i==2:
                request.session["dinner_style"] = [2]
            return redirect('ap')
        _l = ["sim","gra","del"]
        name = request.POST["name"]
        i = _l.index(name)
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

            if request.session["base"][i] + request.session["addition"][i] - int(request.POST[name+mod]) < 0:
                # 에러 발생 ## 
                minusError = -1 # <-- 전달해야됨
                print("음식 수는 0보다 작을 수 없습니다. ")
                return redirect('ap')

            request.session["addition"][i] -= int(request.POST[name+mod])
            request.session["addition"]=request.session["addition"]
        return redirect('ap')
    
def addorder(request):
    _l = [x+y for x,y in zip(request.session["addition"],request.session["base"])]
    request.session["stock"].append(_l)
    request.session["order"].append(request.session["dinner_menu"]+request.session["dinner_style"]+ _l)
    #print("addorder = ",request.session["order"])
    request.session["order"] = request.session["order"]
    
    if request.POST.get('go') == '1':
            return redirect('dfp')
    elif request.POST.get('go') == '2':
            return redirect('op')
            
# 주문
def orderpage(request):
    dinnerMain = Dinner_main()
    orderMain = Order_main()
    order = list(request.session["order"])
    money_l = []
    dinData=[]
    money = 0
    for o in order:
        _ = dinnerMain.cal_dinner_price(o)
        money_l.append(_) # request.session["order"]: order list
        money += _
        __ = dinnerMain.make_dinner_data(o)
        dinData.append(__)
    request.session["dinData"] = dinData # views.order에 전달하기 위해. 
    print("total money is ", money) # 이 부분에서, 뒤로 갔다가 다시 로딩 시 가격이 2배가 되는 버그 존재. 
    try:
        if request.session["user"][2]: # 할인받는 경우. 
            final_money = money * 0.8
            sale_money = money * 0.2
        else:
            final_money = money # 할인 안 받는 경우. 
            sale_money = 0
    except:
        final_money = money # 할인 안 받는 경우. 
        sale_money = 0
    #request.session["orderObject"] = [["name","phonenumber","addr","card"],"13:00","additionalOrder","dinnerData"] # <=== 미리 선언하자.
    print("before make dinner") # for test
    dinnerData = dinnerMain.make_dinner_data(request.session["order"])
    request.session["dinnerData"] = dinnerData ######################## 디너 데이터 세션에 넣자. def order에서 사용함. 
    #[persons, selected_dinner, selected_style, customizated_str, money]
    print("after make dinner") # for test
    # print("디너 데이터는 다음과 같습니다: ", dinnerData)
    #들어가야 할 내용들: 유저정보 + 시간 + 추가요청사항 + 디너정보
    #request.session["name"] = request.POST["name"]
    time_l = orderMain.get_currunt_time(request)
    # print("time_l is ", time_l)
    # time_l = "111111111111" # 테스트용
    # for i, j in enumerate(request.session['user']): # request.session['user']에 저장된 값 확인용 코드
    #     print("user is ", request.session['user'][i])  # user[0] = 이름. user[1] = 전화번호. user[2] = 할인여부 user[3] = 주소. user[4] = 카드번호
    #~~~#
    try:
        context = {"arr":time_l, "dinner":dinnerData[1], "num":dinnerData[0], "style":dinnerData[2], "addition":dinnerData[3], 
                "name":request.session["user"][0], "phonenumber":request.session["user"][1], "sale":request.session["user"][2], 
                 "address":request.session["user"][3],  "card":request.session["user"][4], "price":dinnerData[4], "money":money,
                  "final_money":final_money, "sale_money":sale_money, "dinData":dinData}
    except:
        context = {"arr":time_l, "dinner":dinnerData[1], "num":dinnerData[0], "style":dinnerData[2], "addition":dinnerData[3], 
                  "price":dinnerData[4], "money":money,
                  "final_money":final_money, "sale_money":sale_money, "dinData":dinData}
    return render(request, 'order.html', {"context":context}) # {money = 'money'} <- context로 반환?  # 수정. order 전달하자. 
@csrf_exempt
def order(request):
    if request.method=="POST":
        dinnerMain = Dinner_main()
        orderMain = Order_main()
        #dinner data: 고객 정보 + 배달 시간 + 배달요청사항 + 디너 정보
        #출력 형식: [3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]
        #order 리턴값: [["name", "phnum", "addr"], "13:00", "additional", dinner Data] 
        for i in request.session["stock"]:
            orderMain.send_to_stock(i)
        err = orderMain.send_order_data(request)
        # print(test_)
        if err == -1:
            return redirect('op')
        elif err == -2:
            return redirect('op')
        elif err == -3:
            return redirect('op')
## 추가한 세션 변수: "dinnerData", "orderUser", "dinData"
    #if request.method == 'POST': # 주문하는 고객 정보 수정사항 받아오기. + 시간 정보 받아오기. + 추가 요청 사항 받아오기. 
        oname = request.POST["name"]
        ophonenumber = request.POST["phonenumber"]
        oaddress = request.POST["address"]
        ocard = request.POST["card"]
        otime = request.POST["dtime"]
        owant = request.POST["want"]
        ofoodmoney = request.POST["foodmoney"]
        odiscount = request.POST["discount"]
        ofinalmoney = request.POST["finalmoney"] 
        #print("oname, ophone, oaddr, otime", oname, oaddress, ocard, otime) for test
        
        try:
            request.session["orderUser"] = [oname, ophonenumber, request.session["user"][2], oaddress, ocard]
        except:
            request.session["orderUser"] = [oname, ophonenumber, 0, oaddress, ocard]
        orderData = orderMain.makeOrder(request.session["orderUser"], request.session["time"], request.session["dinnerData"], owant)#orderUser 기반으로 orderData 만듦. 
        print("order Data is ", orderData)
        request.session["context"] = {"oname":oname, "ophone":ophonenumber, "oaddr":oaddress, "ocard":ocard, "otime":otime,
        "owant":owant, "ofoodmoney":ofoodmoney, "odiscount":odiscount, "ofinalmoney":ofinalmoney, "dinData":request.session["dinData"]}

        return redirect('of')
    
def orderfin(request):
    context = request.session["context"]
    return render(request, 'orderfinish.html', {"context":context})
        
        
        
        # dinnerData = [[3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]] # for test
        # #orderMain.makeOrder()
        # #orderData = orderMain.makeOrder(["name", "phnum", "addr"], "13:00", "추가요청사항", dinnerData) # for test
        # orderData = [["name", "phnum", "addr"], "13:00", "추가요청사항", dinnerData]
        
        # return redirect('cm')
        # #return render(request, 'customermain.html', {'user_name': name})


# 음성인식 페이지
def voiceaipage(request):
    return render(request, 'voiceai.html')