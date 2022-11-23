from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse
from .module import *
from .datacontrol import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



class Order_main:
    @staticmethod
    def makeOrder(user, time, dinnerData, comment):
        orderData = [[user[0], user[1], user[2], user[3], user[4]], time, dinnerData, comment]
        # print("orderData is ", orderData) #$#
        return orderData

    @staticmethod
    def send_order_data(request):
        if request.method == 'POST':
            #print("for test, rq.session[user] = ", request.session["user"])
            cOrder = CurruntOrder()
            cOrder.name = request.POST['name']
            try:
                cOrder.phone = int(request.POST['phonenumber'])
            except:
                return -3
            cOrder.address = request.POST['address']
            #user.card = request.POST['card']  # 모델에 추가해야 함.
            l = ["time1","time2","time3","time4","time5","time6","time7","time8","time9","time10","time11","time12"]
            i=0
            deliverytime = request.POST["dtime"]
            try:
                deliverytime = int(deliverytime[0:2]+deliverytime[3:])
                request.session["time"] = deliverytime
            except:
                time = Order_main.get_currunt_time(request)
                if "1" not in time:
                    return -1
                return -2
            
            cOrder.field_id = Order_main.Field_id_set(request) ## field_id
            cos = CurruntOrderState.objects.get(time=deliverytime)
            temp = 0
            if not cos.field_1:
                temp=0
            elif not cos.field_2:
                temp=1
            elif not cos.field_3:
                temp=2
            elif not cos.field_4:
                temp=3
            elif not cos.field_5:
                temp=4
            l = [cos.field_1,cos.field_2,cos.field_3,cos.field_4,cos.field_5]
            # le = len(request.session["order"])
            order = OrderList()
            order.field_id = cOrder.field_id
            try:
                order.user = request.session["user"][1]
            except:
                order.user = request.POST["phonenumber"]
            for i in request.session["order"]:
                order.ordernum = listToString(i)
                order.price = 0 # price 넣기
                order.info = request.POST['want']
                order.state = 0
                order.save()
                cOrder.save()
                if temp==0:
                    cos.field_1 = order.field_id
                elif temp==1:
                    cos.field_2 = order.field_id
                elif temp==2:
                    cos.field_3 = order.field_id
                elif temp==3:
                    cos.field_4 = order.field_id
                elif temp==4:
                    cos.field_5 = order.field_id
                temp += 1
                cOrder.field_id += 1
                order.field_id += 1 
            cos.save()
            return 0

    @staticmethod
    def Field_id_set(request):
        _ = datetime.now()
        year = str(_.year)[2:]
        month = f"{_.month:02}"
        day = f"{_.day:02}"
        hour = f"{_.hour:02}"
        m = f"{_.minute:02}"
        sec = f"{_.second:02}"
        if isinstance(request.session["user"],str): ## 마지막 자리수로 회원 비회원 구분 가능
            type = "5"
        else:
            type = "0"
        return int(year+month+day+hour+m+sec+type)
    
    @staticmethod
    def get_currunt_time(request):
        _ = datetime.now()
        l = [1600,1630,1700,1730,1800,1830,1900,1930,2000,2030,2100,2130]
        time = int(str(_.hour+1)+str(_.minute))
        data_1 = [x>time for x in l]
        data_2 = []
        temp = 5
        cos = CurruntOrderState.objects.all()
        for i in cos:
            temp = 5
            if i.field_5:
                temp=0
            elif i.field_4:
                temp=1
            elif i.field_3:
                temp=2
            elif i.field_2:
                temp=3
            elif i.field_1:
                temp=4
            if temp >= len(request.session["order"]):
                data_2.append(1)
            else:
                data_2.append(0)
        # print(temp,request.session["order"])
        data = [x&y for x,y in zip(data_1,data_2)]
        data = listToString(data)
        return data # 되는 시간만 구현. 자리없는것도 구현해야됨.

    @staticmethod
    def send_to_stock(_l):
        l = _l.copy()
        l[11] = math.ceil(l[11]/4+l[12]) #커피합치기
        l[13] = math.ceil(l[13]/4+l[14]) #와인합치기
        del l[12]
        del l[13]
        _l = ["box","pot","cup","val","pla","steak","salad","egg",
              "bacon","bread","bag","cof","wine","champ"]
        for i in range(len(l)):
            if l[i]:
                s_data = Stock.objects.get(name=_l[i])
                s_data.quantity -= l[i]
                s_data.save()
    
    @staticmethod
    def order(request):
        if request.method=="POST":
            dinnerMain = Dinner_main()
            orderMain = Order_main()
            #dinner data: 고객 정보 + 배달 시간 + 배달요청사항 + 디너 정보
            #출력 형식: [3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]
            #order 리턴값: [["name", "phnum", "addr"], "13:00", "additional", dinner Data] 
            err = orderMain.send_order_data(request)
            # print(test_)
            if err == -1:
                return redirect('op')
            elif err == -2:
                return redirect('op')
            elif err == -3:
                return redirect('op')
            for i in request.session["stock"]:
                orderMain.send_to_stock(i)

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
            # print("order Data is ", orderData)
            request.session["context"] = {"oname":oname, "ophone":ophonenumber, "oaddr":oaddress, "ocard":ocard, "otime":otime,
            "owant":owant, "ofoodmoney":ofoodmoney, "odiscount":odiscount, "ofinalmoney":ofinalmoney, "dinData":request.session["dinData"]}

            return redirect('of')

    
class Order_interface:
    @staticmethod
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
        # print("total money is ", money) # 이 부분에서, 뒤로 갔다가 다시 로딩 시 가격이 2배가 되는 버그 존재. 
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
        # print("before make dinner") # for test
        dinnerData = dinnerMain.make_dinner_data(request.session["order"])
        request.session["dinnerData"] = dinnerData ######################## 디너 데이터 세션에 넣자. def order에서 사용함. 
        #[persons, selected_dinner, selected_style, customizated_str, money]
        # print("after make dinner") # for test
        # print("디너 데이터는 다음과 같습니다: ", dinnerData)
        #들어가야 할 내용들: 유저정보 + 시간 + 추가요청사항 + 디너정보
        #request.session["name"] = request.POST["name"]
        time_l = orderMain.get_currunt_time(request)

        print(time_l)
        try:
            context = {"arr":time_l, "dinner":dinnerData[1], "num":dinnerData[0], "style":dinnerData[2], "addition":dinnerData[3], 
                    "name":request.session["user"][0], "phonenumber":"0"+str(request.session["user"][1]), "sale":request.session["user"][2], 
                    "address":request.session["user"][3],  "card":request.session["user"][4], "price":dinnerData[4], "money":money,
                    "final_money":final_money, "sale_money":sale_money, "dinData":dinData}
        except:
            context = {"arr":time_l, "dinner":dinnerData[1], "num":dinnerData[0], "style":dinnerData[2], "addition":dinnerData[3], 
                    "price":dinnerData[4], "money":money,
                    "final_money":final_money, "sale_money":sale_money, "dinData":dinData}
        return render(request, 'order.html', {"context":context}) # {money = 'money'} <- context로 반환?  # 수정. order 전달하자. 

    @staticmethod
    def orderfin(request):
        context = request.session["context"]
        return render(request, 'orderfinish.html', {"context":context})


class Dinner_main:
    def __init__(self):
        self.style_list = {"심플 디너": 0, "그랜드 디너" : 5000, "딜럭스 디너" : 10000}
        # UML 상에서 food_list였지만, 그릇, 컵까지 합치면 변수 이름이 맞지 않다고 생각하여 additional_list로 수정
        self.additional_list = {"box" : 0, "pot": 3000, "cup": 2000, "val": 3000, "pla": 1000, 
                        "steak": 38000, "salad": 12000, "egg": 8000, "bacon": 8000, "bread": 4000,
                        "bag": 4000, "cof": 5000, "cofp": 18000, "wine": 7000, "wineb": 40000, "champ": 70000}
        self.dinner_list = ["발렌타인 디너", "프렌치 디너", "잉글리쉬 디너", "샴페인 축제 디너"]
        self.i = 0 # for iterration

    def cal_dinner_price(self, dinnerLists):
        if str(type(dinnerLists[0])) == "<class 'list'>": # 더블 리스트인 경우. list[[]]
            dinnerList = dinnerLists[0] # 추후 수정. 초기 구현은 디너 한 종류만 주문한 것으로 생각하자. 
        else:
            dinnerList = dinnerLists
        total_price = 0
        persons = 0
        # 전체 사람 수 = 디너 주문 수. 세 항목은 0, 한 항목은 사람 수만큼 값을 가지므로 총 사람 수는 아래와 같다. 
        persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3]
        # 스타일 가격 합산
        if dinnerList[4] == 1:      # 그랜드 디너 dinner
            total_price += self.style_list["그랜드 디너"] * persons
        if dinnerList[4] == 2:    # 딜럭스 디너 dinner
            total_price += self.style_list["딜럭스 디너"] * persons
        
        self.i = 0 # for iteration 
        #print("dinnerList is !!!", dinnerList) #문제점: 심플 디너일 때 디너리스트의 길이가 20이 됨. -> OUT OF RANGE
        for additional in self.additional_list.keys(): #
            total_price += self.additional_list[additional] * dinnerList[self.i + 5]
            self.i += 1
        else:
            self.i = 0
        return total_price
    def make_dinner_data(self,dinnerLists):
        #initialize for reuse#
        persons = 0
        selected_dinner = []
        selected_style = []
        customizated_str = []
        money = 0

        # if str(type(dinnerLists[1])) == "<class 'int'>":
        #     dinnerList = dinnerLists
        # else:
        #     dinnerList = dinnerLists[0]
        if str(type(dinnerLists[0])) == "<class 'list'>": # 더블 리스트인 경우. list[[]]
            dinnerList = dinnerLists[0] # 추후 수정. 초기 구현은 디너 한 종류만 주문한 것으로 생각하자. 
        else:
            dinnerList = dinnerLists
        persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3] # 사람 수 출력
        selected_dinner = ""
        selected_style = ""
        if dinnerList[0] != 0: # 디너 종류
            selected_dinner = "발렌타인 디너"
        elif dinnerList[1] != 0:
            selected_dinner = "프렌치 디너"
        elif dinnerList[2] != 0:
            selected_dinner = "잉글리쉬 디너"
        else:
            selected_dinner = "champangeDinner"
        
        if dinnerList[4] == 0: # 스타일 종류
            selected_style = "심플 디너"    
        elif dinnerList[4] == 1:
            selected_style = "그랜드 디너"
        else:
            selected_style = "딜럭스 디너"

        defaultDinner = Dinner_main.dinner_convert(dinnerList) # 변경 사항을 확인하기 위해 디폴트 디너 값을 구함. 0 ~ 4까지는 디너/스타일 정보이므로 제외.
        customizated = [x-y for x, y in zip(dinnerList[5:], defaultDinner)] # 변경 사항이 없으면 모두 0인 리스트로 나옴
        customizated_str = []
        keys = ["상자 접시","도자기 접시","컵","발렌타인 접시","플라스틱 잔","스테이크","샐러드","에그스크램블","베이컨","빵","바게트빵(4조각)","커피","커피","와인","와인","샴페인"]
        for idx, count in enumerate(customizated):
            if count > 0:
                temp = keys[idx] + " " + str(count) + "개 추가 / "
                if idx==11 or idx==13:
                    temp = keys[idx] + " " + str(count) + "잔 추가 / "
                if idx==12:
                    temp = keys[idx] + " " + str(count) + "포트 추가 / "
                if idx==14 or idx==15:
                    temp = keys[idx] + " " + str(count) + "병 추가 / " 
                customizated_str.append(temp)
            if count < 0:
                temp = keys[idx] + " " + str(abs(count)) + "개 제외 / " # abs: customizated 값에서, 음식 수를 기존보다 적게 시키는 경우 음수가 됨. 
                if idx==11 or idx==13:
                    temp = keys[idx] + " " + str(count) + "잔 제외 / "
                if idx==12:
                    temp = keys[idx] + " " + str(count) + "포트 제외 / "
                if idx==14 or idx==15:
                    temp = keys[idx] + " " + str(count) + "병 제외 / "  
                customizated_str.append(temp)
        if customizated_str == []: # 커스터마이징이 없다면 "수정 사항 없음 출력. "
            customizated_str.append("추가 사항 없음")
        money = self.cal_dinner_price(dinnerList)##
        #print("돈!!!!!!!!!!!!!", money) #for test 
        dinnerData = []
        dinnerData.append(persons)
        dinnerData.append(selected_dinner)
        dinnerData.append(selected_style)
        dinnerData.append(customizated_str)
        dinnerData.append(money)
        return dinnerData
    
    @staticmethod
    def dinner_convert(dinner_l):
        _l = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i,num in enumerate(dinner_l): # i: idx. num: value
            if i ==0 and num:
                _l[5] += num #스테이크
                _l[-2]+= num # 와인한병
            if i ==1 and num:
                _l[5] += num # 스테이크
                _l[6]+= num # 셀러드
                _l[-3] += num # 와인한잔
                _l[-5] += num # 커피한잔
            if i ==2 and num:
                _l[5] += num # 스테이크
                _l[8]+= num # 빵
                _l[7]+= num # 베이컨
                _l[6]+= num #에크스크램블
            if i == 3 and num:
                _l[5] += num # 스테이크 2개. # 수정.    
                _l[-6]+= num//2 # 바게트빵 4개. # 수정.  
                _l[-4] += num//2 # 커피 한포트
                _l[-2] += num//2 # 와인한병
                _l[-1] += num//2 # 샴페인 한병
        return _l
    
    @staticmethod
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

    
    @staticmethod
    def dinner_food(request):
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

    
    @staticmethod
    def dinner_style(request):
        if request.method =="POST":
            voice = request.POST.get('voicesubmit',False)
            if voice:
                i = Dinner_main.make_voice_dinner_data(voice,"style")
                if i==0:
                    if request.session["dinner_menu"][3]!=0:
                        return redirect('dsp')
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
                if request.session["dinner_menu"][3]!=0:
                        return redirect('dsp')
                request.session["dinner_style"] = [0]
            elif i==1:
                request.session["dinner_style"] = [1]
            elif i==2:
                request.session["dinner_style"] = [2]
            return redirect('ap')

    @staticmethod
    def add(request):
        _l = ["box","pot","cup","val","pla","steak","salad","egg","bacon","bread","bag","cof","cofp","wine","wineb","champ"]
        if request.method == 'POST':
            name = request.POST["name"]
            mod = request.POST["mode"]
            if mod == "add":
                i = _l.index(name)
                if request.session["base"][i] + request.session["addition"][i] + int(request.POST[name+mod]) > 9:
                    plusError = -1 # 에러변수. 미사용시 삭제.
                    print("음식 수는 9보다 클 수 없습니다. ") #테스트용 
                    return redirect('ap')

                request.session["addition"][i] += int(request.POST[name+mod])
                request.session["addition"]=request.session["addition"]
            else:
                i = _l.index(name)
                if request.session["base"][i] + request.session["addition"][i] - int(request.POST[name+mod]) < 0:
                    # 에러 발생 ## 
                    minusError = -1 # <-- 전달해야됨
                    # print("음식 수는 0보다 작을 수 없습니다. ")
                    return redirect('ap')

                request.session["addition"][i] -= int(request.POST[name+mod])
                request.session["addition"]=request.session["addition"]
            return redirect('ap')
   
class Dinner_interface:
    @staticmethod
    def dfpage(request):
        if request.session["user"]:                                                 #
            name = request.session["user"][0]
        else:
            name = "Anonymous User"
        request.session["addition"]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        return render(request, 'dinnerfood.html', {'user_name': name})

    
    @staticmethod
    def dspage(request):
        if request.session["user"]:
            name = request.session["user"][0]
        else:
            name = "Anonymous User"
        chamno = request.session["dinner_menu"][3]
        return render(request, 'dinnerstyle.html', {'user_name': name, 'chamno':chamno})

    
    @staticmethod
    def addpage(request):
        if request.session["user"]:
            name = request.session["user"][0]
        else:
            name = "Anonymous User"
        return render(request, 'addition.html', {'user_name': name})


class Login_main:
    def _user_login_init(self,phone,password):
        Order_list = []
        data = get_data(0,phone)
        addrCardData = get_data(3, phone) ## datacontrol에 새로 만듦. addr, card 받음. 
        # print(data)
        sale = 0
        if isinstance(data,int):
            return data
        if password==data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            name = data[0]
            address = addrCardData[0] # 수정
            card = addrCardData[1] # 수정
            if len(OrderList.objects.filter(user=phone))>10:
                sale=1
        else:
            return -2
        return (name,phone,sale, address, card) # 수정
    
    @staticmethod
    def _login_check(phone):
        try:
            int(phone)
        except:
            return -3
        data = get_data(0,phone)
        if data==-1:
            return 0
        if data==-10:
            return data
        return -1
    
    @staticmethod
    def logout(request):
        request.session.clear()
        return redirect('cm')

    @staticmethod
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

    
    @staticmethod
    def reorder(request):
        if request.method =="POST":
            data = request.POST.get("ordernum",False)
            if data:
                d = list(data)
                for i,n in enumerate(d):
                    d[i] = int(n)
                request.session["order"] = [d]
                request.session["stock"] = [d[5:]]
                # print(request.session["stock"])
        return redirect('op')
    
    @staticmethod
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

class Login_interface:
    @staticmethod
    def cusmainpage(request):
        try:
            request.session["user"]
        except:
            request.session["user"]=None
        request.session["order"] = []
        request.session["stock"] = []
        return render(request, 'customermain.html')

    @staticmethod
    def anoorder(request):
        try:
            request.session["user"][0]
            return redirect('cm')
        except:
            return redirect('dfp')

    @staticmethod
    def signuppage(request):
        return render(request, 'signup.html')

    @staticmethod
    def loginpage(request):
        if request.session["user"] != None:
            return redirect("uolp")
        return render(request, 'login.html')

    @staticmethod
    def userorderlistpage(request):
        dinnerMain = Dinner_main()
        if request.session["user"]:
            name = request.session["user"][0]
        else:
            name = "Anonymous User"
        
        state_l=["주문완료","조리중","배달준비","배달중","배달완료"]
        temp = OrderList.objects.filter(user=request.session["user"][1])
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
        return render(request, 'userorderlist.html', {'user_name': name,'users':temp})

    
    
# USER
# 메인


# 로그아웃

# 회원가입


# 로그인

# 이전 주문내역 불러오기




 
    
# 주문
