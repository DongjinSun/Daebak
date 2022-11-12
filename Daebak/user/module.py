from .datacontrol import *
from .models import User

class Login_main:
    def _user_login_init(self,phone,password):
        Order_list = []
        data = get_data(0,phone)
        print(data)
        sale = 0
        if isinstance(data,int):
            return data
        if password==data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            name = data[0]
            data = get_data(1,phone)
            for i in data:
                Order_list.append(i)
            if len(Order_list)>10:
                sale = 1
            print(Order_list)
        else: ## 없으면 오류코드 -2 
            return -2
        return (name,phone,Order_list,sale)
    def _user_create_init(self,phone,password):
        pass
    def _login_check(self,phone):
        data = get_data(0,phone)
        print(data)
        if data==-1:
            return 0
        return data

def dinner_convert(dinner_l):
    _l = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i,num in enumerate(dinner_l):
        if i ==0 and num:
            _l[5] += num #스테이크
            _l[-2]+= num # 와인한병
        if i ==1 and num:
            _l[5] += num # 스테이크
            _l[6]+= num # 셀러드
            _l[-3] += num # 와인한잔
            _l[-5] += num # 커피한잔
        if i ==2 and num:
            _l[5] += num # 스테이크
            _l[8]+= num # 빵
            _l[7]+= num # 베이컨
            _l[6]+= num #에크스크램블
        if i == 3 and num:
            _l[3] += num//2 # 스테이크
            _l[-2]+= num*2 # 바게트빵
            _l[-4] += num//2 # 커피 한포트
            _l[-2] += num//2 # 와인한병
            _l[-1] += num//2 # 샴페인 한병
    return _l
    
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
            

    
        
    
    
            
        
        