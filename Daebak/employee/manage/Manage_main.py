import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


from django.shortcuts import redirect, render
from employee.datacontrol import change_data

class Manage_main:
    @staticmethod
    def emphone(request):
        if request.method =="POST":
            name = request.POST["name"]
            phone = request.POST["newphone"]
            err = change_data(1,name,phone)
            if err:
                pass
        return redirect("eecp")
    
    @staticmethod
    def emjob(request):
        if request.method =="POST":
            name = request.POST["name"]
            job = request.POST["job"]
            err = change_data(2,name,job)
            if err:
                pass
        return redirect("eecp")
