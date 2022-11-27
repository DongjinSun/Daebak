import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from django.shortcuts import redirect, render
from employee.models import CurruntOrder
from employee.datacontrol import change_data


class Delivery_main:
    state_l = ["readydelivery","nowdelivery","finishdelivery"]
    
    @staticmethod
    def emdelivery(request):
        if request.method =="POST":
            id=request.POST["name"]
            state = request.POST.get("state",False)
            if not state:
                return redirect('edecp')
            i = int(Delivery_main.state_l.index(state))+2
            change_data(3,id,i)
            id=int(id)
            s = CurruntOrder.objects.get(field_id = id)
            if i==4:
                s.delete()
        return redirect('edecp')
    