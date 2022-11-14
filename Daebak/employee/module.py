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
        if data==-10:
            return data
        return -1
        
def get_currunt_order_list():
    _ = datetime.now()
    data = get_data(1,_.hour,_.minute)
    return data
    
def dinner_reverse(ordernum):
    menu_s = ordernum[:4]
    for i,n in enumerate(menu_s):
        if i == 0:
            menu = "Valentine dinner "+str(n)+"개"
        if i == 1:
            menu = "French dinner "+str(n)+"개"
        if i == 2:
            menu = "English dinner "+str(n)+"개"
        if i == 0:
            menu = "Champagne Feast dinner "+str(n)+"개"
    style = ordernum[4]
    add = ordernum[5:]
    return (menu,style,add)