from datetime import datetime

from django.shortcuts import redirect
from employee.datacontrol import get_data, change_data


class Cook_main:
    @staticmethod
    def emcook(request):
        if request.method == "POST":
            id = request.POST["name"]
            try:
                state = request.POST["state"]
                if id:
                    if state =="nowcook":
                        state = 1
                    if state =="finishcook":
                        state = 2
                    change_data(3,id,state)
            except:
                pass
        return redirect('ecocp')

    @staticmethod
    def get_currunt_order_list():
        _ = datetime.now()
        data = get_data(1,_.hour,_.minute)
        # data = get_data(1,0,0)
        return data
    
    @staticmethod
    def get_state(n):
        state = ["주문완료","조리중"]
        i = state[n]
        return i
    