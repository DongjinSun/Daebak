from django.shortcuts import redirect, render
from django.contrib import messages

from user.dinner import Dinner_main
from .Order_main import Order_main

class Order_interface:
    @staticmethod
    def orderpage(request):
        order = list(request.session["order"])
        money_l = []
        dinData=[]
        money = 0
        for o in order:
            _ = Order_main.cal_dinner_price(o)
            money_l.append(_) 
            money += _
            __ = Dinner_main.make_dinner_data(o)
            dinData.append(__)
        request.session["dinData"] = dinData # views.order에 전달하기 위해. 
        # print("total money is ", money) # 이 부분에서, 뒤로 갔다가 다시 로딩 시 가격이 2배가 되는 버그 존재. 
        try:
            if request.session["user"][2]: # 할인받는 경우. 
                final_money = int(money * 0.8)
                sale_money = int(money * 0.2)
            else:
                final_money = money # 할인 안 받는 경우. 
                sale_money = 0
        except:
            final_money = money # 할인 안 받는 경우. 
            sale_money = 0

        # dinnerData = Dinner_main.make_dinner_data(request.session["order"])
        # request.session["dinnerData"] = dinnerData ######################## 디너 데이터 세션에 넣자. def order에서 사용함. 

        time_l = Order_main.get_currunt_time(request)

        try:
            context = {"arr":time_l, "name":request.session["user"][0], "phonenumber":"0"+str(request.session["user"][1]), "sale":request.session["user"][2], 
                    "address":request.session["user"][3],  "card":request.session["user"][4], "money":money,
                    "final_money":final_money, "sale_money":sale_money, "dinData":dinData}
        except:
            context = {"arr":time_l, "money":money, "final_money":final_money, "sale_money":sale_money, "dinData":dinData}
        return render(request, 'order.html', {"context":context}) # {money = 'money'} <- context로 반환?  # 수정. order 전달하자. 

    @staticmethod
    def orderfin(request):
        context = request.session["context"]
        return render(request, 'orderfinish.html', {"context":context})

