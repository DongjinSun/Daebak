import os
import sys

from datacontrol import change_data
from django.shortcuts import redirect

class Stock_main:
    @staticmethod
    def emstock(request):
        if request.method == 'POST':
            name = request.POST["name"]
            num = request.POST["stockadd"]
            err = change_data(0,name,num)
        return redirect('estcp')
