from .datacontrol import *
from .models import User

class Login_main:
    def __init__(self):
        self.user = User()
        self.sale = 0

    def _user_login_init(self,phone,password):
        data = get_data(0,phone)
        print(data)
        if isinstance(data,int):
            return data
        if password==data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            self.user.name = data[0]
            self.user.phone = phone
            data = get_data(1,phone)
            for i in data:
                self.user.Order_list.append(i)
            if len(self.user.Order_list)>10:
                self.sale = 1
        else: ## 없으면 오류코드 -2 
            return -2
        return (self.user.name,self.user.phone,self.user.Order_list,self.sale)
    def _user_create_init(self,phone,password):
        pass
    
    def _login_check(self,phone):
        data = get_data(0,phone)
        print(data)
        if data==-1:
            return 0
        return data
        
        
        
    
        
    
    
            
        
        