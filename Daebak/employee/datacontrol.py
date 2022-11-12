# employee로 고쳐야함.

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
    if num == 1: ## currunt_order_list 가져오기
        try:
            cursor = connection.cursor()
            print(str(args[0])+str(args[1]))
            strSql = "SELECT * from currunt_order_state where TIME >"+str(args[0])+str(args[1])
            cursor.execute(strSql)
            result = cursor.fetchall()
            data = list()
            print(result)
            for i in range(len(result)):
                data.append(list())
                data[i].append(result[i][0])
                for j in range(1,6):
                    if result[i][j] == None:
                        break
                    strSql = "SELECT ordernum from order_list where _id"+str(result[i][j])
                    cursor.execute(strSql)
                    result = cursor.fetchall()
                    data[i].append(result[0])
            return data
        except:
            connection.rollback()
            return -10
    if num == 2:
        try:
            cursor = connection.cursor()
            strSql = "SELECT name,password from user where phone="+str(args[0])
            cursor.execute(strSql)
            result = cursor.fetchall()
            connection.close()
            return result[0]
        except:
            connection.rollback()
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


def change_data(request, pk,num):
    reqData = request.data
    data_l = [Stock,User,Employee, OrderList]
    data = data_l[num].objects.get(id=pk)
    f_d = {0:stockDataSerializer,1:userDataSerializer,
           2:employeeDataSerializer,3:orderDataSerializer}
    serializer = f_d[num](instance=data, data=reqData)
    
    if serializer.is_valid():
        serializer.save()
        