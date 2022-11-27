from django.shortcuts import redirect, render
from django.contrib import messages

from user.models import CurruntOrderState , OrderList, CurruntOrder, Stock
from datetime import datetime
from user.module import listToString

import math


class Order_main:
    time_l = [1600,1630,1700,1730,1800,1830,1900,1930,2000,2030,2100,2130]
    stock_l = ["box","pot","cup","val","pla","steak","salad","egg",
              "bacon","bread","bag","cof","wine","champ"]
    style_list = {"심플 디너": 0, "그랜드 디너" : 5000, "딜럭스 디너" : 10000}
    additional_list = {"box" : 0, "pot": 3000, "cup": 2000, "val": 3000, "pla": 1000, 
                        "steak": 38000, "salad": 12000, "egg": 8000, "bacon": 8000, "bread": 4000,
                        "bag": 4000, "cof": 5000, "cofp": 18000, "wine": 7000, "wineb": 40000, "champ": 70000}
    @staticmethod
    def cal_dinner_price(dinnerLists):
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
            total_price += Order_main.style_list["그랜드 디너"] * persons
        if dinnerList[4] == 2:    # 딜럭스 디너 dinner
            total_price += Order_main.style_list["딜럭스 디너"] * persons
        
        i = 0 # for iteration 
        for additional in Order_main.additional_list.keys(): #
            total_price += Order_main.additional_list[additional] * dinnerList[i + 5]
            i += 1
        else:
            i = 0
        return total_price
    # @staticmethod
    # def makeOrder(user, time, dinnerData, comment):
    #     orderData = [[user[0], user[1], user[2], user[3], user[4]], time, dinnerData, comment]
    #     return orderData

    @staticmethod
    def send_order_data(request):
        if request.method == 'POST':

            cOrder = CurruntOrder()
            cOrder.name = request.POST['name']
            try:
                cOrder.phone = int(request.POST['phonenumber'])
            except:
                return -3
            cOrder.address = request.POST['address']
            
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

            order = OrderList()
            order.field_id = cOrder.field_id
            try:
                order.user = request.session["user"][1]
            except:
                order.user = request.POST["phonenumber"]
            for i in request.session["order"]:
                order.ordernum = listToString(i)
                order.price = request.POST["finalmoney"] 
                order.info = request.POST['want']
                order.state = 0
                order.time = deliverytime
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
        
        time = int(str(_.hour+1)+str(_.minute))
        data_1 = [x>time for x in Order_main.time_l]
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
        for i in range(len(l)):
            if l[i]:
                s_data = Stock.objects.get(name=Order_main.stock_l[i])
                s_data.quantity -= l[i]
                s_data.save()
    
    
    @staticmethod
    def order(request):
        if request.method=="POST":
            
            err = Order_main.send_order_data(request)

            if err == -1:
                return redirect('op')
            elif err == -2:
                return redirect('op')
            elif err == -3:
                return redirect('op')
            for i in request.session["stock"]:
                Order_main.send_to_stock(i)

            oname = request.POST["name"]
            ophonenumber = request.POST["phonenumber"]
            oaddress = request.POST["address"]
            ocard = request.POST["card"]
            otime = request.POST["dtime"]
            owant = request.POST["want"]
            ofoodmoney = request.POST["foodmoney"]
            odiscount = request.POST["discount"]
            ofinalmoney = request.POST["finalmoney"] 
            
            # try:
            #     request.session["orderUser"] = [oname, ophonenumber, request.session["user"][2], oaddress, ocard]
            # except:
            #     request.session["orderUser"] = [oname, ophonenumber, 0, oaddress, ocard]
            # orderData = Order_main.makeOrder(request.session["orderUser"], request.session["time"], request.session["dinnerData"], owant)#orderUser 기반으로 orderData 만듦. 
  
            request.session["context"] = {"oname":oname, "ophone":ophonenumber, "oaddr":oaddress, "ocard":ocard, "otime":otime,
            "owant":owant, "ofoodmoney":ofoodmoney, "odiscount":odiscount, "ofinalmoney":ofinalmoney, "dinData":request.session["dinData"]}

            return redirect('of')
