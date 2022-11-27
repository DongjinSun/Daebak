from django.shortcuts import redirect, render
from django.contrib import messages


from user.module import listToString


class Dinner_main:
    
    dinner_list = ["발렌타인 디너", "프렌치 디너", "잉글리쉬 디너", "샴페인 축제 디너"]
    add_l = ["box","pot","cup","val","pla","steak","salad","egg","bacon","bread","bag","cof","cofp","wine","wineb","champ"]
    
    
    @staticmethod
    def make_dinner_data(dinnerLists):
        #initialize for reuse#
        persons = 0
        selected_dinner = []
        selected_style = []
        customizated_str = []
       # money = 0

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
        dinnerData = []
        dinnerData.append(persons)
        dinnerData.append(selected_dinner)
        dinnerData.append(selected_style)
        dinnerData.append(customizated_str)
        #dinnerData.append(money)
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
                _l[9]+= num # 빵
                _l[8]+= num # 베이컨
                _l[7]+= num #에크스크램블
            if i == 3 and num:
                _l[5] += num # 스테이크 2개. # 수정.    
                _l[-6]+= num//2 # 바게트빵 4개. # 수정.  
                _l[-4] += num//2 # 커피 한포트
                _l[-2] += num//2 # 와인한병
                _l[-1] += num//2 # 샴페인 한병
        return _l
    
    @staticmethod
    def addorder(request):
        _l = [x+y for x,y in zip(request.session["addition"],request.session["base"])]
        request.session["stock"].append(_l)
        request.session["order"].append(request.session["dinner_menu"]+request.session["dinner_style"]+ _l)
        request.session["order"] = request.session["order"]
        
        if request.POST.get('go') == '1':
                return redirect('dfp')
        elif request.POST.get('go') == '2':
                return redirect('op')

    
    @staticmethod
    def dinner_food(request):
        _l = ["valnum","frenum","engnum","chanum"]
        if request.method == 'POST':
            voice = request.POST.get('voicesubmit',False)
            print(voice)
            if voice:
                request.session["dinner_menu"]=[0,0,0,0]
                i = Dinner_main.make_voice_dinner_data(voice,"menu")
                request.session["dinner_menu"][i] = 1
                request.session["base"] = Dinner_main.dinner_convert(request.session["dinner_menu"])
                if not i:
                    request.session["dinner_style"] = [3]
                    return redirect('ap')
                return redirect('dsp')
            
            name = request.POST["name"]
                
            i = _l.index(name)
            request.session["dinner_menu"]=[0,0,0,0]
            request.session["dinner_menu"][i] = int(request.POST[name])
            request.session["base"] = Dinner_main.dinner_convert(request.session["dinner_menu"])
            if not i:
                request.session["dinner_style"] = [3]
                return redirect('ap')
            return redirect('dsp')
        
    @staticmethod
    def make_voice_dinner_data(data,type):
        if type =="menu":
            _l = ["발렌타인 디너","프렌치 디너","잉글리쉬 디너","샴페인 축제 디너"]
        elif type=="style":
            _l = ["심플 디너","그랜드 디너","딜럭스 디너"]
        return _l.index(data)
    
    @staticmethod
    def dinner_style(request):
        if request.method =="POST":
            voice = request.POST.get('voicesubmit',False)
            if voice:
                i = Dinner_main.make_voice_dinner_data(voice,"style")
                if i==0:
                    if request.session["dinner_menu"][3]!=0:
                        return redirect('dsp')
                    request.session["dinner_style"] = [0]
                elif i==1:
                    request.session["dinner_style"] = [1]
                elif i==2:
                    request.session["dinner_style"] = [2]
                return redirect('ap')
            _l = ["sim","gra","del"]
            name = request.POST["name"]
            i = _l.index(name)
            if i==0:
                if request.session["dinner_menu"][3]!=0:
                        return redirect('dsp')
                request.session["dinner_style"] = [0]
            elif i==1:
                request.session["dinner_style"] = [1]
            elif i==2:
                request.session["dinner_style"] = [2]
            return redirect('ap')

    @staticmethod
    def add(request):
        if request.method == 'POST':
            name = request.POST["name"]
            mod = request.POST["mode"]
            if mod == "add":
                i = Dinner_main.add_l.index(name)
                if request.session["base"][i] + request.session["addition"][i] + int(request.POST[name+mod]) > 9:
                    plusError = -1 # 에러변수. 미사용시 삭제.
                    print("음식 수는 9보다 클 수 없습니다. ") #테스트용 
                    return redirect('ap')

                request.session["addition"][i] += int(request.POST[name+mod])
                request.session["addition"]=request.session["addition"]
            else:
                i = Dinner_main.add_l.index(name)
                if request.session["base"][i] + request.session["addition"][i] - int(request.POST[name+mod]) < 0:
                    # 에러 발생 ## 
                    minusError = -1 # <-- 전달해야됨
                    # print("음식 수는 0보다 작을 수 없습니다. ")
                    return redirect('ap')

                request.session["addition"][i] -= int(request.POST[name+mod])
                request.session["addition"]=request.session["addition"]
            return redirect('ap')
   