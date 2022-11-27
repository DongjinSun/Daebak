from django.shortcuts import redirect
from django.contrib import messages
from employee.models import Employee
from employee.datacontrol import get_data


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
