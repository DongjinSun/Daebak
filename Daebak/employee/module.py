# employee로 고쳐야함.

from .datacontrol import *
from .models import Employee
from datetime import datetime

class Login_main:
    def __init__(self):
        self.employee = Employee()

    def _user_login_init(self,phone,password):
        data = get_data(0,phone)
        print(data)
        if isinstance(data,int):
            return data
        if password==data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            self.employee.name = data[0]
            self.employee.phone = phone
            self.employee.type = data[2]
        else: ## 틀리면 오류코드 -2 
            return -2
        return (self.employee.name,self.employee.phone,self.employee.type)
    def _user_create_init(self,phone,password):
        pass
    
    def _login_check(self,phone):
        data = get_data(0,phone)
        print(data)
        if data==-1:
            return 0
        return data
        
def get_currunt_order_list():
    _ = datetime.now()
    data = get_data(1,_.hour,_.minute)
    return data
    