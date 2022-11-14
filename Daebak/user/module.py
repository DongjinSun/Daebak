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
        if data==-10:
            return data
        return -1




class Dinner_main:
    style_list = {"simple": 0, "grand" : 5000, "deluxe" : 10000}
    # UML 상에서 food_list였지만, 그릇, 컵까지 합치면 변수 이름이 맞지 않다고 생각하여 additional_list로 수정
    additional_list = {"box" : 0, "pot": 3000, "cup": 2000, "val": 3000, "pla": 1000, 
                       "steak": 38000, "salad": 12000, "egg": 8000, "bacon": 8000, "bread": 4000,
                       "bag": 4000, "cof": 5000, "cofp": 18000, "wine": 7000, "wineb": 40000, "champ": 70000}
    dinner_list = ["valentineDinner", "frenchDinner", "englishDinner", "champagneDinner"]
    i = 0 # for iterration
    #dinnerData = 
    #sale = 
    def cal_dinner_price(request, dinnerMain, dinnerList):
        #[[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 13]] 21개. 
        #[[0, 0, 0, 1, 2, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 5, 0, 2, 3]]
        #[[0, 9, 0, 0 여기까지 디너, 2(스타일: 2), 3, 9, 0, 10, 0(여기까지 잡동사니), 29, 44, 0, 0, 0, 0, 50, 0, 9, 0, 0(음식)]]
        #[0, 1, 2, 3: dinner// 4: 스타일[0,1,2] // 5,6,7,8,9:접시, 그릇//[10~20]:음식추가
        total_price = 0
        # 전체 사람 수 = 디너 주문 수. 세 항목은 0, 한 항목은 사람 수만큼 값을 가지므로 총 사람 수는 아래와 같다. 
        persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3]
        # 스타일 가격 합산
        if dinnerList[4] == 1:      # grand dinner
            total_price += dinnerMain.style_list["grand"] * persons
        elif dinnerList[4] == 2:    # deluxe dinner
            total_price += dinnerMain.style_list["deluxe"] * persons
        
        for additional in dinnerMain.additional_list.keys(): #
            total_price += dinnerMain.additional_list[additional] * dinnerList[dinnerMain.i + 5]
            dinnerMain.i += 1
        else:
            dinnerMain.i = 0
            #print("total price is ", total_price)
        return total_price

    def make_dinner_data(request, dinnerMain, dinnerLists):
        #initialize for reuse#
        persons = 0
        selected_dinner = []
        selected_style = []
        customizated_str = []
        money = 0

        dinnerList = dinnerLists[0] # 추후 수정. 초기 구현은 디너 한 종류만 주문한 것으로 생각하자. 
        persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3] # 사람 수 출력
        selected_dinner = ""
        selected_style = ""
        if dinnerList[0] != 0: # 디너 종류
            selected_dinner = "valentineDinner"
        elif dinnerList[1] != 0:
            selected_dinner = "frenchDinner"
        elif dinnerList[2] != 0:
            selected_dinner = "englishDinner"
        else:
            selected_dinner = "champangeDinner"
        
        if dinnerList[4] == 0: # 스타일 종류
            selected_style = "simple"    
        elif dinnerList[4] == 1:
            selected_style = "grand"
        else:
            selected_style = "deluxe"

        defaultDinner = Dinner_main.dinner_convert(dinnerList) # 변경 사항을 확인하기 위해 디폴트 디너 값을 구함. 0 ~ 4까지는 디너/스타일 정보이므로 제외.
        customizated = [x-y for x, y in zip(dinnerList[5:], defaultDinner)] # 변경 사항이 없으면 모두 0인 리스트로 나옴
        print("customizated is ", customizated) # for test 
        customizated_str = []
        for idx, count in enumerate(customizated):
            if count > 0:
                keys = list(dinnerMain.additional_list.keys())
                temp = keys[idx] + " " + str(count) + "개 추가"
                customizated_str.append(temp)
            if count < 0:
                keys = list(dinnerMain.additional_list.keys())
                temp = keys[idx] + " " + str(abs(count)) + "개 제외" # abs: customizated 값에서, 음식 수를 기존보다 적게 시키는 경우 음수가 됨.  
                customizated_str.append(temp)
            
        money = dinnerMain.cal_dinner_price(dinnerMain, dinnerList)
        #print("돈!!!!!!!!!!!!!", money) #for test 
        dinnerData = []
        dinnerData.append(persons)
        dinnerData.append(selected_dinner)
        dinnerData.append(selected_style)
        dinnerData.append(customizated_str)
        dinnerData.append(money)
        return dinnerData
    
    @staticmethod
    def dinner_convert(dinner_l):
        _l = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i,num in enumerate(dinner_l): # i: idx. num: value
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

    @staticmethod
    def dinner_reverse(ordernum):
        menu_s = ordernum[:4]
        for i,n in enumerate(menu_s):
            if i == 0:
                menu = "Valentine dinner"
                break
            if i == 1:
                menu = "French dinner"
                break
            if i == 2:
                menu = "English dinner"
                break
            if i == 3:
                menu = "Champagne Feast dinner"
                break
        style = ordernum[4]
        add = ordernum[5:]
        return (menu,n[0],style,add)

    # def make_dinner_data(request, dinnerMain, dinnerList):
    #     persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3] # 사람 수 출력

    #     if dinnerList[0] != 0: # 디너 종류
    #         selected_dinner = "valentineDinner"
    #     elif dinnerList[1] != 0:
    #         selected_dinner = "frenchDinner"
    #     elif dinnerList[2] != 0:
    #         selected_dinner = "englishDinner"
    #     else:
    #         selected_dinner = "champangeDinner"
        
    #     if dinnerList[4] == 0: # 스타일 종류
    #         selected_style = "simple"    
    #     elif dinnerList[4] == 1:
    #         selected_style = "grand"
    #     else:
    #         selected_style = "deluxe"

    #     defaultDinner = dinner_convert(dinnerList) # 변경 사항을 확인하기 위해 디폴트 디너 값을 구함.
    #     customizated = [x-y for x, y in zip(dinnerList, defaultDinner)] # 변경 사항이 없으면 모두 0인 리스트로 나옴

        ## todo: customizated 완성. for loop 돌려서 0일때 pass, +일 때 / -일 때 따로 구분해서 출력하자. 
        


        # customizing 내역: views.add 보고 리스트 따로 만들자. [0, 0, 0, 2, -1, 0] 이런식으로. 
        # 합계: views.orderpage의 


        # user.name = User()~~
        # orderData = []
        # orderData = orderData.append(foolist)
       # return orderData

class Order_main:
    current_order_state = None
    order_data = None

#출력 형식: [3, "valentine Dinner", "Deluxe Dinner", ["빵 +1", "스테이크 -3"], 72000]
    #order 리턴값: [["name", "phnum", "addr"], "13:00", "additional", dinner Data]
    def makeOrder(user, dinnerData, time, additional):
        orderData = [[user[0], user[1], user[3]], time, additional, dinnerData]
        return orderData

    def updateOrderState():
        pass
    def send_order_data():
        pass

def listToString(listMenu):            #[1,2,3,4] -> 1234
    str_list = list(map(str, listMenu))#int list -> str list ["1", "2", "3", "4"]
    result = ""
    for s in str_list:
        result += s
    
    result = int(result)               #int형으로 반환
    return result

def stringToList(intMenu):           #1234 -> [1,2,3,4]
    strMenu = str(intMenu)           #int -> str
    str_list = list(strMenu)         # ["1", "2", "3", "4"]
    return list(map(int, str_list))  # [1, 2, 3, 4]