from user.dinner import Dinner_main
from .Cook_main import Cook_main
from employee.module import listToString
from django.shortcuts import redirect, render
from employee.models import OrderList


class Cook_interface:
    @staticmethod
    def emcookpage(request):   
        data = Cook_main.get_currunt_order_list()
        users = list()
        for i in data:
            for j in i[1:]:
                _ = OrderList()
                _.time = i[0]
                l = list(map(int,j[1]))
                _2 = Dinner_main.make_dinner_data(l)
                _.person = _2[0]
                _.dinner = _2[1]
                _.style = _2[2]
                l = listToString(_2[3])
                _.add = l
                if j[2]<2 :
                    _.state = Cook_main.get_state(j[2])
                    users.append(_)
        context = {'users':users}
        return render(request, 'em_cook.html', context)

    @staticmethod
    def emcookchangepage(request):  
        data = Cook_main.get_currunt_order_list()
        users = list()
        for i in data:
            for j in i[1:]:
                _ = OrderList()
                _.time = i[0]
                l = list(map(int,j[1]))
                _2 = Dinner_main.make_dinner_data(l)
                _.person = _2[0]
                _.dinner = _2[1]
                _.style = _2[2]
                l = listToString(_2[3])
                _.add = l
                _.field_id = j[0]
                if j[2]<2 :
                    _.state = Cook_main.get_state(j[2])
                    users.append(_)
        context = {'users':users} 
        return render(request, 'em_cookchange.html', context)