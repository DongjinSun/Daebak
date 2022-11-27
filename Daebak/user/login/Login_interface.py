from django.shortcuts import redirect, render
from django.contrib import messages

from user.models import OrderList, User
from user.dinner import Dinner_main
from user.module import stringToList


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
        if request.session["user"]:
            name = request.session["user"][0]
        else:
            name = "Anonymous User"
        
        state_l=["주문완료","조리중","배달준비","배달중","배달완료"]
        temp = OrderList.objects.filter(user=request.session["user"][1])
        for j in temp:
            tempOrderList = stringToList(j.ordernum)
            _ = Dinner_main.make_dinner_data(tempOrderList)
            j.num = _[0]
            j.food = _[1]
            j.style = _[2]
            j.add = _[3]
            j.state = state_l[j.state]
        if len(temp)>10:
            request.session["user"][2] = 1
        return render(request, 'userorderlist.html', {'user_name': name,'users':temp})

