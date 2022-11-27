import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from employee.models import OrderList, CurruntOrder, User
from django.shortcuts import render
from django.db.models import Q


class Delivery_interface:
    state_l = ["배달준비","배달중","배달완료"]
    time_l = [1600,1630,1700,1730,1800,1830,1900,1930,2000,2030,2100,2130]
    @staticmethod
    def emdeliverypage(request):
        users = []
        for i in Delivery_interface.time_l:
            order = OrderList.objects.filter(Q(state=2)|Q(state=3)) & OrderList.objects.filter(Q(time=i))
            for i in order:
                try:
                    cos = CurruntOrder.objects.get(field_id = i.field_id)
                except:
                    continue
                try:
                    user = User.objects.get(phone=i.user)
                except:
                    user = User()
                user.name=cos.name
                user.state=Delivery_interface.state_l[i.state-2]
                user.phone="0"+str(cos.phone)
                user.address = cos.address
                user.time = i.time
                user.info = i.info
                users.append(user)
            try:
                context = {'users':users}
            except:
                context = {'users':None}
        return render(request, 'em_delivery.html', context)

    @staticmethod
    def emdeliverychangepage(request):
        users = []
        for i in Delivery_interface.time_l:
            order = OrderList.objects.filter(Q(state=2)|Q(state=3)) & OrderList.objects.filter(Q(time=i))
            for i in order:
                try:
                    cos = CurruntOrder.objects.get(field_id = i.field_id)
                except:
                    continue
                try:
                    user = User.objects.get(phone=i.user)
                except:
                    user = User()
                user.name=cos.name
                user.phone="0"+str(cos.phone)
                user.address = cos.address
                user.time = i.time
                user.field_id=i.field_id
                users.append(user)
        try:
            context = {'users':users}
        except:
            context = {'users':None}
        return render(request, 'em_deliverychange.html', context)
