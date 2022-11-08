from .datacontrol import *


class Login_main:
    def __init__(self):
        self.user = list([0,0,list()])
        self.sale = 0
    
    
    def _user_login_init(self,phonenum,password):
        
        data = get_data(0,phonenum)
        if len(data): ### 아이디가 있는지 확인
            return -1 ## 오류코드 -1 출력
        
        if password==get_data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            self.user[0] = get_data[0]
            self.user[1] = phonenum
            data = get_data(1,phonenum)
            for i in data:
                self.user[2].append(list(i))
            
            if len(self.user[2])>10:
                self.sale = 1
        else: ## 없으면 오류코드 -2 
            return -2
            
    def _user_create_init(self,phonenum,password):
        
        data = get_data(0,phonenum)
        if len(data): ### 아이디가 있는지 확인
            return -1 ## 오류코드 -1 출력
        
        if password==get_data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            self.user[0] = get_data[0]
            self.user[1] = phonenum
            data = get_data(1,phonenum)
            for i in data:
                self.user[2].append(list(i))
            
            if len(self.user[2])>10:
                self.sale = 1
        else: ## 없으면 오류코드 -2 
            return -2
    
            
        
        