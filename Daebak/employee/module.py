# employee로 고쳐야함.

from employee.datacontrol import *
from employee.models import Employee
from datetime import datetime

class Dinner_main:
    style_list = {"심플 디너": 0, "그랜드 디너" : 5000, "딜럭스 디너" : 10000}
    additional_list = {"box" : 0, "pot": 3000, "cup": 2000, "val": 3000, "pla": 1000, 
                        "steak": 38000, "salad": 12000, "egg": 8000, "bacon": 8000, "bread": 4000,
                        "bag": 4000, "cof": 5000, "cofp": 18000, "wine": 7000, "wineb": 40000, "champ": 70000}
    dinner_list = ["발렌타인 디너", "프렌치 디너", "잉글리쉬 디너", "샴페인 축제 디너"]
    add_l = ["box","pot","cup","val","pla","steak","salad","egg","bacon","bread","bag","cof","cofp","wine","wineb","champ"]
    
    @staticmethod
    def cal_dinner_price(dinnerLists):
        if str(type(dinnerLists[0])) == "<class 'list'>": # 더블 리스트인 경우. list[[]]
            dinnerList = dinnerLists[0] # 추후 수정. 초기 구현은 디너 한 종류만 주문한 것으로 생각하자. 
        else:
            dinnerList = dinnerLists
        total_price = 0
        persons = 0
        # 전체 사람 수 = 디너 주문 수. 세 항목은 0, 한 항목은 사람 수만큼 값을 가지므로 총 사람 수는 아래와 같다. 
        persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3]
        # 스타일 가격 합산
        if dinnerList[4] == 1:      # 그랜드 디너 dinner
            total_price += Dinner_main.style_list["그랜드 디너"] * persons
        if dinnerList[4] == 2:    # 딜럭스 디너 dinner
            total_price += Dinner_main.style_list["딜럭스 디너"] * persons
        
        i = 0 # for iteration 
        #print("dinnerList is !!!", dinnerList) #문제점: 심플 디너일 때 디너리스트의 길이가 20이 됨. -> OUT OF RANGE
        for additional in Dinner_main.additional_list.keys(): #
            total_price += Dinner_main.additional_list[additional] * dinnerList[i + 5]
            i += 1
        else:
            i = 0
        return total_price
    
    @staticmethod
    def make_dinner_data(dinnerLists):
        #initialize for reuse#
        persons = 0
        selected_dinner = []
        selected_style = []
        customizated_str = []
        money = 0

        # if str(type(dinnerLists[1])) == "<class 'int'>":
        #     dinnerList = dinnerLists
        # else:
        #     dinnerList = dinnerLists[0]
        if str(type(dinnerLists[0])) == "<class 'list'>": # 더블 리스트인 경우. list[[]]
            dinnerList = dinnerLists[0] # 추후 수정. 초기 구현은 디너 한 종류만 주문한 것으로 생각하자. 
        else:
            dinnerList = dinnerLists
        persons = dinnerList[0] + dinnerList[1] + dinnerList[2] + dinnerList[3] # 사람 수 출력
        selected_dinner = ""
        selected_style = ""
        if dinnerList[0] != 0: # 디너 종류
            selected_dinner = Dinner_main.dinner_list[0]
        elif dinnerList[1] != 0:
            selected_dinner = Dinner_main.dinner_list[1]
        elif dinnerList[2] != 0:
            selected_dinner = Dinner_main.dinner_list[2]
        else:
            selected_dinner = Dinner_main.dinner_list[3]
        
        if dinnerList[4] == 0: # 스타일 종류
            selected_style = "심플 디너"    
        elif dinnerList[4] == 1:
            selected_style = "그랜드 디너"
        else:
            selected_style = "딜럭스 디너"

        defaultDinner = Dinner_main.dinner_convert(dinnerList) # 변경 사항을 확인하기 위해 디폴트 디너 값을 구함. 0 ~ 4까지는 디너/스타일 정보이므로 제외.
        customizated = [x-y for x, y in zip(dinnerList[5:], defaultDinner)] # 변경 사항이 없으면 모두 0인 리스트로 나옴
        customizated_str = []
        keys = ["상자 접시","도자기 접시","컵","발렌타인 접시","플라스틱 잔","스테이크","샐러드","에그스크램블","베이컨","빵","바게트빵(4조각)","커피","커피","와인","와인","샴페인"]
        for idx, count in enumerate(customizated):
            if count > 0:
                temp = keys[idx] + " " + str(count) + "개 추가 / "
                if idx==11 or idx==13:
                    temp = keys[idx] + " " + str(count) + "잔 추가 / "
                if idx==12:
                    temp = keys[idx] + " " + str(count) + "포트 추가 / "
                if idx==14 or idx==15:
                    temp = keys[idx] + " " + str(count) + "병 추가 / " 
                customizated_str.append(temp)
            if count < 0:
                temp = keys[idx] + " " + str(abs(count)) + "개 제외 / " # abs: customizated 값에서, 음식 수를 기존보다 적게 시키는 경우 음수가 됨. 
                if idx==11 or idx==13:
                    temp = keys[idx] + " " + str(count) + "잔 제외 / "
                if idx==12:
                    temp = keys[idx] + " " + str(count) + "포트 제외 / "
                if idx==14 or idx==15:
                    temp = keys[idx] + " " + str(count) + "병 제외 / "  
                customizated_str.append(temp)
        if customizated_str == []: # 커스터마이징이 없다면 "수정 사항 없음 출력. "
            customizated_str.append("추가 사항 없음")
            
        customizated_str = listToString(customizated_str)
        money = Dinner_main.cal_dinner_price(dinnerList)##
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
                _l[5] += num # 스테이크 2개. # 수정.    
                _l[-6]+= num//2 # 바게트빵 4개. # 수정.  
                _l[-4] += num//2 # 커피 한포트
                _l[-2] += num//2 # 와인한병
                _l[-1] += num//2 # 샴페인 한병
        return _l
        








def listToString(listMenu):            #[1,2,3,4] -> 1234
    str_list = list(map(str, listMenu))#int list -> str list ["1", "2", "3", "4"]
    result = ""
    for s in str_list:
        result += s
    return result


def stringToList(intMenu):           #1234 -> [1,2,3,4]
    strMenu = str(intMenu)           #int -> str
    str_list = list(strMenu)         # ["1", "2", "3", "4"]
    return list(map(int, str_list))  # [1, 2, 3, 4]
