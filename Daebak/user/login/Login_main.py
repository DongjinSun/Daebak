from django.shortcuts import redirect, render
from django.contrib import messages

from user.datacontrol import get_data
from user.models import OrderList, User



class Login_main:
    
    @staticmethod
    def _user_login_init(phone,password):
        Order_list = []
        data = get_data(0,phone)
        addrCardData = get_data(3, phone) ## datacontrol에 새로 만듦. addr, card 받음. 
        # print(data)
        sale = 0
        if isinstance(data,int):
            return data
        if password==data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            name = data[0]
            address = addrCardData[0] # 수정
            card = addrCardData[1] # 수정
            if len(OrderList.objects.filter(user=phone))>10:
                sale=1
        else:
            return -2
        return (name,phone,sale, address, card) # 수정
    
    @staticmethod
    def _account_check(phone):
        try:
            int(phone)
        except:
            return -3
        data = get_data(0,phone)
        if data==-1:
            return 0
        if data==-10:
            return data
        return -1
    
    @staticmethod
    def logout(request):
        request.session.clear()
        return redirect('cm')

    @staticmethod
    def login(request):
        if request.method == 'POST': 
            try:
                phone = int(request.POST['phonenumber'])
            except:
                messages.warning(request,"휴대폰번호를 입력해주세요")
                return redirect('lp')
            
            request.session["user"]=Login_main._user_login_init(phone,request.POST['password']) # session에 개인정보 저장.
            if isinstance(request.session["user"],int): ## 오류가 난 경우 로그인 다시
                if request.session["user"] == -1:
                    messages.warning(request,"없는 계정입니다.")
                    request.session["user"] = None
                elif request.session["user"] == -2:
                    messages.warning(request,"비밀번호가 다릅니다.")
                    request.session["user"] = None
                elif request.session["user"] == -10:
                    messages.warning(request,"데이터를 가져오지 못했습니다. 다시 시도해주세요.")
                    request.session["user"] = None
                return redirect('lp')
            else:
                return redirect('uolp')

    
    @staticmethod
    def reorder(request):
        if request.method =="POST":
            data = request.POST.get("ordernum",False)
            if data:
                d = list(data)
                for i,n in enumerate(d):
                    d[i] = int(n)
                request.session["order"] = [d]
                request.session["stock"] = [d[5:]]
        return redirect('op')
    
    @staticmethod
    def signup(request):
        if request.method == 'POST':
            user = User()
            user.name = request.POST.get('name',False)
            if not user.name:
                messages.warning(request,"이름을 입력하세요")
                return redirect('sp')
                
            user.phone = request.POST.get('phonenumber',False)
            if not user.phone:
                messages.warning(request,"휴대폰번호를 입력하세요")
                return redirect('sp')

            err=Login_main._account_check(user.phone)
            if err: 
                if err == -1:
                    messages.warning(request,"이미 있는 계정입니다.")
                elif err == -10:
                    messages.warning(request,"데이터를 가져오지 못했습니다. 다시 시도해주세요.")
                elif err == -3:
                    messages.warning(request,"휴대폰 번호를 올바르게 입력해주세요")
                return redirect('sp')

            user.password = request.POST.get('password',False)
            if not user.password:
                messages.warning(request,"비밀번호를 입력하세요")
                return redirect('sp')
            user.address = request.POST.get('address',False)  
            if not user.address:
                messages.warning(request,"주소를 입력하세요")
                return redirect('sp') 
            
            user.card = request.POST.get('card',False)  
            if not user.card:
                messages.warning(request,"카드번호를 입력하세요")
                return redirect('sp')
            user.save()
        return redirect('cm')
