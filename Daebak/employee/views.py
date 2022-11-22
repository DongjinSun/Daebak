from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse
from .module import *
from .datacontrol import *
from django.db.models import Q
from django.contrib import messages


# EMPLOYEE
# 메인 + 로그인
def emmainpage(request):
    return render(request, 'employeemain.html')

    # 배달직원 - 배달 조회 페이지는 'edep'입니다.
    # 요리직원 - 재고조회랑 주문조회 직원관리 선택 페이지는 'ecp'입니다.
def emlogin(request):
    if request.method == 'POST':
        _login = Login_main()
        try : 
            phone = int(request.POST['phonenumber'])
        except:
            messages.warning(request,"휴대폰 번호를 입력해주세요")
            return redirect('em')
        data=request.session["employee"]=_login._user_login_init(int(request.POST['phonenumber']),request.POST['password']) # session에 로그인 정보 저장
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

# 회원가입
def emsignuppage(request):
    return render(request, 'em_signup.html')

def emsignup(request):
    _login= Login_main()
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
        
        err=_login._login_check(user.phone)
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



# 로그인
# def emloginpage(request):
#    return render(request, 'em_login.html')


# 선택창
def emchoosepage(request):
    return render(request, 'em_choose.html')


# root 권한 확인
def root_check(request):
    if request.session["employee"][2] != 0:
        return redirect('ecp') ##root 권한 없을경우 선택 불가
    return redirect('eep')


# 재고 조회
def emstockpage(request):
    _l = ["박스접시","도자기 접시","도자기 컵","발랜테인 접시","플라스틱 컵","스테이크","샐러드","계란","베이컨","빵","바게트빵","커피","와인","샴폐인"]
    stock = Stock.objects.all()
    for i in zip(stock,_l):
        i[0].name = i[1]
    context = {'users':stock}
    return render(request, 'em_stock.html', context)


def emstock(request):
    if request.method == 'POST':
        name = request.POST["name"]
        num = request.POST["stockadd"]
        err = change_data(0,name,num)
    return redirect('estcp')

def emstockchangepage(request):
    _l = ["박스접시","도자기 접시","도자기 컵","발랜테인 접시","플라스틱 컵","스테이크","샐러드","계란","베이컨","빵","바게트빵","커피","와인","샴폐인"]
    stock = Stock.objects.all()
    for i in zip(stock,_l):
        i[0].name = i[1]
    context = {'users':stock}
    return render(request, 'em_stockchange.html', context)

# 주문 조회
def emcookpage(request):   
    data = get_currunt_order_list()
    users = list()
    d = Dinner_main()
    for i in data:
        for j in i[1:]:
            _ = OrderList()
            _.time = i[0]
            l = list(map(int,j[1]))
            _2 = d.make_dinner_data(l)
            _.person = _2[0]
            _.dinner = _2[1]
            _.style = _2[2]
            _.add = _2[3]
            _.state = j[2]
            if _.state!=2 :
                users.append(_)
    context = {'users':users}
    return render(request, 'em_cook.html', context)

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

def emcookchangepage(request):  
    data = get_currunt_order_list()
    users = list()
    
    d = Dinner_main()
    for i in data:
        for j in i[1:]:
            _ = OrderList()
            _.time = i[0]
            l = list(map(int,j[1]))
            _2 = d.make_dinner_data(l)
            _.person = _2[0]
            _.dinner = _2[1]
            _.style = _2[2]
            _.add = _2[3]
            _.state = j[2]
            _.field_id = j[0]
            if _.state!=2 :
                users.append(_)
    context = {'users':users} 
    return render(request, 'em_cookchange.html', context)


# 직원 관리
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

# 배달 조회
def emdeliverypage(request):
    state_l = ["배달준비","배달중","배달완료"]
    order = OrderList.objects.filter(Q(state=2)|Q(state=3))
    
    for i in order:
        cos = CurruntOrder.objects.get(field_id = i.field_id)
        users = User.objects.filter(phone=i.user)
        for j in users:
            j.state=state_l[i.state-2]
            j.phone="0"+str(j.phone)
            j.address = cos.address
    try:
        context = {'users':users}
    except:
        context = {'users':None}
    return render(request, 'em_delivery.html', context)

def emdeliverychangepage(request):
    state_l = ["배달준비","배달중","배달완료"]
    order = OrderList.objects.filter(Q(state=2)|Q(state=3))
    for i in order:
        cos = CurruntOrder.objects.get(field_id = i.field_id)
        users = User.objects.filter(phone=i.user)
        for j in users:
            j.state=state_l[i.state-2]
            j.field_id=i.field_id
            j.address = cos.address
    try:
        context = {'users':users}
    except:
        context = {'users':None}
    return render(request, 'em_deliverychange.html', context)

def emdelivery(request):
    state_l = ["readydelivery","nowdelivery","finishdelivery"]
    if request.method =="POST":
        id=request.POST["name"]
        state = request.POST["state"]
        i = int(state_l.index(state))+2
        change_data(3,id,i)
        id=int(id)
        s = CurruntOrder.objects.get(field_id = id)
        s.delete()
    return redirect('edecp')
    

def emphone(request):
    if request.method =="POST":
        name = request.POST["name"]
        phone = request.POST["newphone"]
        print(name,phone)
        err = change_data(1,name,phone)
        if err:
            pass
    return redirect("eecp")

def emjob(request):
    if request.method =="POST":
        name = request.POST["name"]
        job = request.POST["job"]
        err = change_data(2,name,job)
        if err:
            pass
    return redirect("eecp")
