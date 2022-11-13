from rest_framework.serializers import ModelSerializer
from .models import Stock, User, Employee, OrderList
from django.db import connection

        
def get_data(num,*args):
    
    if num == 0: ## 이름, 비밀번호 가져오기
        try:
            cursor = connection.cursor()
            strSql = "SELECT name,password from user where phone="+str(args[0])
            cursor.execute(strSql)
            result = cursor.fetchall()
            connection.close()
            if len(result)==0:
                return -1
            return result[0]
        except:
            connection.rollback()
            return -10 # 데이터 가져오기 실패 오류코드 
    if num == 1: ## order list 가져오기
        try:
            cursor = connection.cursor()
            strSql = "SELECT ordernum from order_list where user="+str(args[0])
            cursor.execute(strSql)
            result = cursor.fetchall()
            connection.close()
            return result
        except:
            connection.rollback()
            print("error")
            return -10
    if num ==2: ## currunt_order_state 가져오기
        try:
            cursor = connection.cursor()
            strSql = "SELECT  from currunt_order_state where TIME="+str(args[0])
            cursor.execute(strSql)
            result = [i for i in cursor.fetchall()[0][1:] if i != None]
            connection.close()
            if len(result) >=5:
                return -9 ## 이미 예약이 꽉참
            return result
        except:
            connection.rollback()
            print("error")
            return -10

def Insert_data(request,num):
    pass
    # reqData = request.data
    # f_d = {0:stockDataSerializer,1:userDataSerializer,
    #        2:employeeDataSerializer,3:orderDataSerializer}
    # serializer = f_d[num](data = reqData)

    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def change_data(request,num,*args):
    if num==0: ##stock 데이터 바꾸기
        _l = ["박스접시","도자기 접시","도자기 컵","발랜테인 접시","플라스틱 컵","스테이크","샐러드","계란","베이컨","빵","바게트빵","커피","와인","샴폐인"]
        _l2 = ["box","pot","cup","val","pla","steak","salad","egg","bacon","bread","bag","cof","wine","champ"]
        i = _l.index(args[0])
        try:
            cursor = connection.cursor()
            strSql = "UPDATE stock set quantity="+str(args[1])+"where name="+str(_l2[i])
            cursor.execute(strSql)
            result = cursor.fetchall()
            connection.close()
            return result
        except:
            connection.rollback()
            print("error")
            return -10
        
    