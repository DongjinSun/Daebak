from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse
from .module import *
from .datacontrol import *
from django.db.models import Q
from django.contrib import messages
from django.views import View

class Login_interface:
    @staticmethod
    def emmainpage(request):
        return render(request, 'employeemain.html')
    
    @staticmethod
    def emsignuppage(request):
        return render(request, 'em_signup.html')
    
    @staticmethod
    def emchoosepage(request):
        return render(request, 'em_choose.html')

class Cook_interface:
    @staticmethod
    def emcookpage(request):   
        data = Cook_main.get_currunt_order_list()
        users = list()
        for i in data:
            for j in i[1:]:
                _ = OrderList()
                _.time = i[0]
                l = list(map(int,j[1]))
                _2 = Dinner_main.make_dinner_data(l)
                _.person = _2[0]
                _.dinner = _2[1]
                _.style = _2[2]
                l = listToString(_2[3])
                _.add = l
                if j[2]<2 :
                    _.state = Cook_main.get_state(j[2])
                    users.append(_)
        context = {'users':users}
        return render(request, 'em_cook.html', context)

    @staticmethod
    def emcookchangepage(request):  
        data = Cook_main.get_currunt_order_list()
        users = list()
        for i in data:
            for j in i[1:]:
                _ = OrderList()
                _.time = i[0]
                l = list(map(int,j[1]))
                _2 = Dinner_main.make_dinner_data(l)
                _.person = _2[0]
                _.dinner = _2[1]
                _.style = _2[2]
                l = listToString(_2[3])
                _.add = l
                _.field_id = j[0]
                if j[2]<2 :
                    _.state = Cook_main.get_state(j[2])
                    users.append(_)
        context = {'users':users} 
        return render(request, 'em_cookchange.html', context)

class Manage_interface:
    @staticmethod
    def emempage(request):
        users = Employee.objects.all()
        for i in users:
            if i.type==0:
                i.type ="관리자"
            elif i.type==1:
                i.type = "조리"
            elif i.type==2:
                i.type = "배달"
            i.phone = "0"+str(i.phone)
        context = {'users':users[1:]}
        return render(request, 'em_employee.html', context)

    @staticmethod
    def ememchangepage(request):
        users = Employee.objects.all()
        for i in users:
            if i.type==0:
                i.type ="관리자"
            elif i.type==1:
                i.type = "조리"
            elif i.type==2:
                i.type = "배달"
            i.phone = "0"+str(i.phone)
        context = {'users':users[1:]}
        return render(request, 'em_employeechange.html', context)

class Stock_interface:
    stock_list = ["상자 접시","도자기 접시","컵","발렌타인 접시","플라스틱 잔","스테이크","샐러드","계란","베이컨","빵","바게트빵","커피","와인","샴페인"]
    
    @staticmethod
    def emstockpage(request):
        stock = Stock.objects.all()
        for i in zip(stock,Stock_interface.stock_list):
            i[0].name = i[1]
        context = {'users':stock}
        return render(request, 'em_stock.html', context)

    @staticmethod  
    def emstockchangepage(request):
        stock = Stock.objects.all()
        for i in zip(stock,Stock_interface.stock_list):
            i[0].name = i[1]
        context = {'users':stock}
        return render(request, 'em_stockchange.html', context)

class Login_main:
    @staticmethod
    def emlogin(request):
        if request.method == 'POST':
            try : 
                phone = int(request.POST['phonenumber'])
            except:
                messages.warning(request,"휴대폰 번호를 입력해주세요")
                return redirect('em')
            data=request.session["employee"]=Login_main._user_login_init(int(request.POST['phonenumber']),request.POST['password']) # session에 로그인 정보 저장
            if isinstance(request.session["employee"],int):
                if request.session["employee"] == -1:
                    messages.warning(request,"없는 계정입니다.")
                elif request.session["employee"] == -2:
                    messages.warning(request,"비밀번호가 다릅니다.")
                elif request.session["employee"] == -10:
                    messages.warning(request,"데이터를 가져오지 못했습니다. 다시 시도해주세요.")
                request.session["employee"] = None
                return redirect('em') ## 오류코드에 따른 오류 메세지 출력하는거 구현필요
            if data[2] == 2:
                return redirect('edep') ## 배달 직원 페이지로
            else:
                return redirect('ecp')

    @staticmethod
    def emsignup(request):
        if request.method == 'POST':
            user = Employee()
            user.name = request.POST.get('name',False)
            if not user.name:
                messages.warning(request,"이름을 입력하세요")
                return redirect('esp')
            user.phone = request.POST.get('phonenumber',False)
            if not user.phone:
                messages.warning(request,"휴대폰번호를 입력하세요")
                return redirect('esp')
            
            err=Login_main._account_check(user.phone)
            if err: 
                if err == -1:
                    messages.warning(request,"이미 있는 계정입니다.")
                elif err == -3:
                    messages.warning(request,"휴대폰 번호를 올바르게 입력해주세요")
                elif err == -10:
                    messages.warning(request,"데이터를 가져오지 못했습니다. 다시 시도해주세요.")
                return redirect('esp')
            
            user.password = request.POST.get('password',False)
            if not user.password:
                messages.warning(request,"비밀번호를 입력하세요")
                return redirect('esp')
            job = request.POST.get('job',False) #cook: 조리, delivery: 배달, manage: 관리
            if not job:
                messages.warning(request,"직원 타입을 선택하세요")
                return redirect('esp')
            
            if job =="manage":
                user.type = 0
            elif job =="cook":
                user.type = 1
            elif job =="delivery":
                user.type = 2
            user.save()
            messages.warning(request,"회원가입이 완료되었습니다.")
        return redirect('em')

    @staticmethod
    def root_check(request):
        if request.session["employee"][2] != 0:
            return redirect('ecp') ##root 권한 없을경우 선택 불가
        return redirect('eep')

    
    @staticmethod
    def _user_login_init(phone,password):
        data = get_data(0,phone)
        if isinstance(data,int):
            return data
        employee = Employee()
        if password==data[1]: ## 비밀번호 확인하고 맞으면 데이터 가져오기
            employee.name = data[0]
            employee.phone = phone
            employee.type = data[2]
        else: ## 틀리면 오류코드 -2 
            return -2
        return (employee.name,employee.phone,employee.type)

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

class Stock_main:
    @staticmethod
    def emstock(request):
        if request.method == 'POST':
            name = request.POST["name"]
            num = request.POST["stockadd"]
            err = change_data(0,name,num)
        return redirect('estcp')

class Cook_main:
    @staticmethod
    def emcook(request):
        if request.method == "POST":
            id = request.POST["name"]
            print("id=",id)
            try:
                state = request.POST["state"]
                if id:
                    if state =="nowcook":
                        state = 1
                    if state =="finishcook":
                        state = 2
                    change_data(3,id,state)
            except:
                pass
        return redirect('ecocp')

    @staticmethod
    def get_currunt_order_list():
        _ = datetime.now()
        data = get_data(1,_.hour,_.minute)
        # data = get_data(1,0,0)
        return data
    
    @staticmethod
    def get_state(n):
        state = ["주문완료","조리중"]
        i = state[n]
        return i
    
class Manage_main:
    @staticmethod
    def emphone(request):
        if request.method =="POST":
            name = request.POST["name"]
            phone = request.POST["newphone"]
            err = change_data(1,name,phone)
            if err:
                pass
        return redirect("eecp")
    
    @staticmethod
    def emjob(request):
        if request.method =="POST":
            name = request.POST["name"]
            job = request.POST["job"]
            err = change_data(2,name,job)
            if err:
                pass
        return redirect("eecp")

class Delivery_interface:
    state_l = ["배달준비","배달중","배달완료"]
    time_l = [1600,1630,1700,1730,1800,1830,1900,1930,2000,2030,2100,2130]
    @staticmethod
    def emdeliverypage(request):
        users = []
        for i in Delivery_interface.time_l:
            order = OrderList.objects.filter(Q(state=2)|Q(state=3)) & OrderList.objects.filter(Q(time=i))
            for i in order:
                try:
                    cos = CurruntOrder.objects.get(field_id = i.field_id)
                except:
                    continue
                try:
                    user = User.objects.get(phone=i.user)
                except:
                    user = User()
                user.name=cos.name
                user.state=Delivery_interface.state_l[i.state-2]
                user.phone="0"+str(cos.phone)
                user.address = cos.address
                user.time = i.time
                users.append(user)
            try:
                context = {'users':users}
            except:
                context = {'users':None}
        return render(request, 'em_delivery.html', context)

    @staticmethod
    def emdeliverychangepage(request):
        users = []
        for i in Delivery_interface.time_l:
            order = OrderList.objects.filter(Q(state=2)|Q(state=3)) & OrderList.objects.filter(Q(time=i))
            for i in order:
                try:
                    cos = CurruntOrder.objects.get(field_id = i.field_id)
                except:
                    continue
                try:
                    user = User.objects.get(phone=i.user)
                except:
                    user = User()
                user.name=cos.name
                user.phone="0"+str(cos.phone)
                user.address = cos.address
                user.time = i.time
                user.field_id=i.field_id
                users.append(user)
        try:
            context = {'users':users}
        except:
            context = {'users':None}
        return render(request, 'em_deliverychange.html', context)

class Delivery_main:
    state_l = ["readydelivery","nowdelivery","finishdelivery"]
    
    @staticmethod
    def emdelivery(request):
        if request.method =="POST":
            id=request.POST["name"]
            state = request.POST["state"]
            i = int(Delivery_main.state_l.index(state))+2
            change_data(3,id,i)
            id=int(id)
            s = CurruntOrder.objects.get(field_id = id)
            if i==4:
                s.delete()
        return redirect('edecp')
    

