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


class Dinner_main:
    style_list = {"simple": 0, "grand" : 5000, "deluxe" : 10000}
    # UML 상에서 food_list였지만, 그릇, 컵까지 합치면 변수 이름이 맞지 않다고 생각하여 additional_list로 수정하였습니다. 
    additional_list = {"box" : 0, "pot": 3000, "cup": 2000, "val": 3000, "pla": 1000, 
                       "steak": 38000, "salad": 12000, "egg": 8000, "bacon": 8000, "bread": 4000,
                       "bag": 4000, "cof": 5000, "cofp": 18000, "wine": 7000, "wineb": 40000, "champ": 70000}
    dinner_list = ["valentineDinner", "frenchDinner", "englishDinner", "champagneDinner"]
    #dinnerData = 
    #sale = 
    def make_dinner_data():
        pass
    def cal_dinner_price(dinnerList):
        #[[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 13]] 21개. 
        #[[0, 0, 0, 1, 2, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 5, 0, 2, 3]]
        #[[0, 9, 0, 0 여기까지 디너, 2(스타일: 2), 3, 9, 0, 10, 0(여기까지 잡동사니), 29, 44, 0, 0, 0, 0, 50, 0, 9, 0, 0(음식)]]
        #[0, 1, 2, 3: dinner// 4: 스타일[0,1,2] // 5,6,7,8,9:접시, 그릇//[10~20]:음식추가
        total_price = 0
        # 전체 사람 수 = 디너 주문 수. 세 항목은 0, 한 항목은 사람 수만큼 값을 가지므로 총 사람 수는 아래와 같다. 
        persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3]
        # 스타일 가격 합산
        if dinnerList[4] == 1:      # grand dinner
            total_price += style_list[grand] * persons
        elif dinnerList[4] == 2:    # deluxe dinner
            total_price += style_list[deluxe] * persons
        
            i = 0
        for additional in additional_list.keys(): #
            total_price += additional_list[additional] * dinnerList[i + 5]
            i += 1
        else:
            i = 0
            print("total price is ", total_price)
            
