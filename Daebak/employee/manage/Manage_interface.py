import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from employee.models import Employee
from django.shortcuts import redirect, render

class Manage_interface:
    @staticmethod
    def emempage(request):
        users = Employee.objects.all()
        for i in users:
            if i.type==0:
                i.type ="관리자"
            elif i.type==1:
                i.type = "조리"
            elif i.type==2:
                i.type = "배달"
            i.phone = "0"+str(i.phone)
        context = {'users':users[1:]}
        return render(request, 'em_employee.html', context)

    @staticmethod
    def ememchangepage(request):
        users = Employee.objects.all()
        for i in users:
            if i.type==0:
                i.type ="관리자"
            elif i.type==1:
                i.type = "조리"
            elif i.type==2:
                i.type = "배달"
            i.phone = "0"+str(i.phone)
        context = {'users':users[1:]}
        return render(request, 'em_employeechange.html', context)
