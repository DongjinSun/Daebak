# employee로 고쳐야함.

from .datacontrol import *
from .models import Employee

class Login_main:
    def __init__(self):
        self.employee = Employee()
        self.root = 0
    
    
    def _user_login_init(self,phone,password):
        data = get_data(0,phone)
        print(data)
        if isinstance(data,int):
            return -10
        if not len(data): ### 아이디가 있는지 확인
            return -1 ## 오류코드 -1 출력 // 아이디 없음 데이터 오류
        
        if password==data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            self.employee.name = data[0]
            self.employee.phone = phone
            self.employee.type = data[2]
        else: ## 틀리면 오류코드 -2 
            return -2
        return (self.employee.name,self.employee.phone,self.employee.type)
    def _user_create_init(self,phone,password):
        pass
        
    
    
            
        
        