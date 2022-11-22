from .datacontrol import *
from .models import *
from datetime import datetime
import math

class Login_main:
    def _user_login_init(self,phone,password):
        Order_list = []
        data = get_data(0,phone)
        addrCardData = get_data(3, phone) ## datacontrol에 새로 만듦. addr, card 받음. 
        print(data)
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
    
    def _user_create_init(self,phone,password):
        pass
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




    
class Dinner_main:
    def __init__(self):
        
        self.style_list = {"simple": 0, "grand" : 5000, "deluxe" : 10000}
        # UML 상에서 food_list였지만, 그릇, 컵까지 합치면 변수 이름이 맞지 않다고 생각하여 additional_list로 수정
        self.additional_list = {"box" : 0, "pot": 3000, "cup": 2000, "val": 3000, "pla": 1000, 
                        "steak": 38000, "salad": 12000, "egg": 8000, "bacon": 8000, "bread": 4000,
                        "bag": 4000, "cof": 5000, "cofp": 18000, "wine": 7000, "wineb": 40000, "champ": 70000}
        self.dinner_list = ["valentineDinner", "frenchDinner", "englishDinner", "champagneDinner"]
        self.i = 0 # for iterration
    #dinnerData = 
    #sale = 
    def cal_dinner_price(self, dinnerLists):
        #[[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 13]] 21개. 
        #[[0, 0, 0, 1, 2, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 5, 0, 2, 3]]
        #[[0, 9, 0, 0 여기까지 디너, 2(스타일: 2), 3, 9, 0, 10, 0(여기까지 잡동사니), 29, 44, 0, 0, 0, 0, 50, 0, 9, 0, 0(음식)]]
        #[0, 1, 2, 3: dinner// 4: 스타일[0,1,2] // 5,6,7,8,9:접시, 그릇//[10~20]:음식추가
        if str(type(dinnerLists[0])) == "<class 'list'>": # 더블 리스트인 경우. list[[]]
            dinnerList = dinnerLists[0] # 추후 수정. 초기 구현은 디너 한 종류만 주문한 것으로 생각하자. 
        else:
            dinnerList = dinnerLists
        total_price = 0
        persons = 0
        # 전체 사람 수 = 디너 주문 수. 세 항목은 0, 한 항목은 사람 수만큼 값을 가지므로 총 사람 수는 아래와 같다. 
        persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3]
        # 스타일 가격 합산
        if dinnerList[4] == 1:      # grand dinner
            total_price += self.style_list["grand"] * persons
        if dinnerList[4] == 2:    # deluxe dinner
            total_price += self.style_list["deluxe"] * persons
        
        self.i = 0 # for iteration 
        #print("dinnerList is !!!", dinnerList) #문제점: 심플 디너일 때 디너리스트의 길이가 20이 됨. -> OUT OF RANGE
        for additional in self.additional_list.keys(): #
            total_price += self.additional_list[additional] * dinnerList[self.i + 5]
            self.i += 1
        else:
            self.i = 0
            print(" ### cal_dinner_price ### total price is ", total_price) 
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
            selected_dinner = "valentineDinner"
        elif dinnerList[1] != 0:
            selected_dinner = "frenchDinner"
        elif dinnerList[2] != 0:
            selected_dinner = "englishDinner"
        else:
            selected_dinner = "champangeDinner"
        
        if dinnerList[4] == 0: # 스타일 종류
            selected_style = "simple"    
        elif dinnerList[4] == 1:
            selected_style = "grand"
        else:
            selected_style = "deluxe"

        defaultDinner = Dinner_main.dinner_convert(dinnerList) # 변경 사항을 확인하기 위해 디폴트 디너 값을 구함. 0 ~ 4까지는 디너/스타일 정보이므로 제외.
        customizated = [x-y for x, y in zip(dinnerList[5:], defaultDinner)] # 변경 사항이 없으면 모두 0인 리스트로 나옴
        customizated_str = []
        for idx, count in enumerate(customizated):
            if count > 0:
                keys = list(self.additional_list.keys())
                temp = keys[idx] + " " + str(count) + "개 추가"
                customizated_str.append(temp)
            if count < 0:
                keys = list(self.additional_list.keys())
                temp = keys[idx] + " " + str(abs(count)) + "개 제외" # abs: customizated 값에서, 음식 수를 기존보다 적게 시키는 경우 음수가 됨.  
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
    def make_voice_dinner_data(data,type):
        if type =="menu":
            _l = ["발렌타인 디너","프렌치 디너","잉글리쉬 디너","샴페인 축제 디너"]
        elif type=="style":
            _l = ["simple dinner","그랜드 디너","디럭스"]
        return _l.index(data)
            
        
    

    # @staticmethod
    # def dinner_reverse(ordernum):
    #     menu_s = ordernum[:4]
    #     for i,n in enumerate(menu_s):
    #         if i == 0:
    #             menu = "Valentine dinner"
    #             break
    #         if i == 1:
    #             menu = "French dinner"
    #             break
    #         if i == 2:
    #             menu = "English dinner"
    #             break
    #         if i == 3:
    #             menu = "Champagne Feast dinner"
    #             break
    #     style = ordernum[4]
    #     add = ordernum[5:]
    #     return (menu,n[0],style,add)

    # def make_dinner_data(request, dinnerMain, dinnerList):
    #     persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3] # 사람 수 출력

    #     if dinnerList[0] != 0: # 디너 종류
    #         selected_dinner = "valentineDinner"
    #     elif dinnerList[1] != 0:
    #         selected_dinner = "frenchDinner"
    #     elif dinnerList[2] != 0:
    #         selected_dinner = "englishDinner"
    #     else:
    #         selected_dinner = "champangeDinner"
        
    #     if dinnerList[4] == 0: # 스타일 종류
    #         selected_style = "simple"    
    #     elif dinnerList[4] == 1:
    #         selected_style = "grand"
    #     else:
    #         selected_style = "deluxe"

    #     defaultDinner = dinner_convert(dinnerList) # 변경 사항을 확인하기 위해 디폴트 디너 값을 구함.
    #     customizated = [x-y for x, y in zip(dinnerList, defaultDinner)] # 변경 사항이 없으면 모두 0인 리스트로 나옴

        ## todo: customizated 완성. for loop 돌려서 0일때 pass, +일 때 / -일 때 따로 구분해서 출력하자. 
        


        # customizing 내역: views.add 보고 리스트 따로 만들자. [0, 0, 0, 2, -1, 0] 이런식으로. 
        # 합계: views.orderpage의 


        # user.name = User()~~
        # orderData = []
        # orderData = orderData.append(foolist)
       # return orderData

class Order_main:

#출력 형식: [3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]
    #order 리턴값: [["name", "phnum"(주소 제거)], "13:00", "additional", dinner Data]
    @staticmethod
    def makeOrder(user, time, dinnerData, comment):
        orderData = [[user[0], user[1], user[2], user[3], user[4]], time, dinnerData, comment]
        print("orderData is ", orderData) #$#
        return orderData

    def updateOrderState():
        pass
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
            
            
            # temp = cos[0]
            # for i in range(1,6):
            #     a = globals()['temp.field_'+str(i)]
            #     print(a)
            ## currunt order state에 넣는거 구현
            
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
        print(temp,request.session["order"])
        data = [x&y for x,y in zip(data_1,data_2)]
        data = listToString(data)
        return data # 되는 시간만 구현. 자리없는것도 구현해야됨.
#{"box" : 0, "pot": 3000, "cup": 2000, "val": 3000, "pla": 1000, "steak": 38000, "salad": 12000, "egg": 8000, "bacon": 8000, "bread": 4000,
#                       "bag": 4000, "cof": 5000, "cofp": 18000, "wine": 7000, "wineb": 40000, "champ": 70000} 10 11 12 13


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
            
        
    
def listToString(listMenu):            #[1,2,3,4] -> 1234
    str_list = list(map(str, listMenu))#int list -> str list ["1", "2", "3", "4"]
    result = ""
    for s in str_list:
        result += s
    return result

def stringToList(intMenu):           #1234 -> [1,2,3,4]
    strMenu = str(intMenu)           #int -> str
    str_list = list(strMenu)         # ["1", "2", "3", "4"]
    return list(map(int, str_list))  # [1, 2, 3, 4]


