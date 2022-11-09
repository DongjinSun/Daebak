# employee로 고쳐야함.

from .datacontrol import *
from .models import User

class Login_main:
    def __init__(self):
        self.user = User()
        self.sale = 0
    
    
    def _user_login_init(self,phone,password):
        data = get_data(0,phone)
        if isinstance(data,int):
            return -10
        if len(data): ### 아이디가 있는지 확인
            return -1 ## 오류코드 -1 출력 // 아이디 없음 데이터 오류
        
        if password==get_data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            self.user.name = get_data[0]
            self.user.phone = phone
            data = get_data(1,phone)
            for i in data:
                self.user[2].append(list(i))
            
            if len(self.user[2])>10:
                self.sale = 1
        else: ## 없으면 오류코드 -2 
            return -2
            
    def _user_create_init(self,phone,password):
        pass
        
    
    
            
        
        