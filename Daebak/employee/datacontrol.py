# employee로 고쳐야함.

from rest_framework.serializers import ModelSerializer
from employee.models import Stock, User, Employee, OrderList
from django.db import connection

        
def get_data(num,*args):
    if num == 0: ## 이름, 비밀번호 가져오기
        try:
            cursor = connection.cursor()
            strSql = "SELECT name,password,type from employee where phone="+str(args[0])
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
        cursor = connection.cursor()
        time = f"{args[0]:02d}{args[1]:02d}"

        strSql = "SELECT * from currunt_order_state where TIME > "+time
        cursor.execute(strSql)
        result = cursor.fetchall()

        data = list()
        for i in range(len(result)):
            data.append(list())
            data[i].append(result[i][0])
            for j in range(1,6):
                if result[i][j] == None:
                    break
                strSql = "SELECT _id,ordernum,state from order_list where _id="+str(result[i][j])
                cursor.execute(strSql)
                result_ = cursor.fetchall()
                data[i].append(result_[0])
        return data
        # try:
        #     cursor = connection.cursor()
        #     time = f"{args[0]:02d}{args[1]:02d}"
        #     print(time)
        #     strSql = "SELECT * from currunt_order_state where TIME > "+time
        #     cursor.execute(strSql)
        #     result = cursor.fetchall()
        #     print(1)
        #     data = list()
        #     for i in range(len(result)):
        #         data.append(list())
        #         data[i].append(result[i][0])
        #         for j in range(1,6):
        #             if result[i][j] == None:
        #                 break
        #             strSql = "SELECT _id,ordernum,state from order_list where _id="+str(result[i][j])
        #             cursor.execute(strSql)
        #             result_ = cursor.fetchall()
        #             data[i].append(result_[0])
        #     print(2)
        #     return data
        # except:
        #     connection.rollback()
        #     return -10
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
    
    if num == 3:
        try:
            cursor = connection.cursor()
            strSql = "SELECT state from ordernum where _id="+str(args[0])
            cursor.execute(strSql)
            result = cursor.fetchall()
            connection.close()
            return result[0]
        except:
            connection.rollback()
            return -10

def change_data(num,*args):
    if num == 0: ##stock 데이터 바꾸기
        _l = ["박스접시","도자기 접시","도자기 컵","발랜테인 접시","플라스틱 컵","스테이크","샐러드","계란","베이컨","빵","바게트빵","커피","와인","샴폐인"]
        _l2 = ["box","pot","cup","val","pla","steak","salad","egg","bacon","bread","bag","cof","wine","champ"]
        i = _l.index(args[0])
        try:
            cursor = connection.cursor()
            strSql = "UPDATE stock set quantity="+str(args[1])+" where name=\""+str(_l2[i])+"\""
            cursor.execute(strSql)
            connection.commit()
            connection.close()
            return 0
        except:
            connection.rollback()
            print("error")
            return -10
    if num==1:
        try:
            cursor = connection.cursor()
            strSql = "UPDATE employee set phone="+str(args[1])+" where name=\""+str(args[0])+"\""
            cursor.execute(strSql)

            connection.commit()
            connection.close()
            return 0
        except:
            connection.rollback()
            print("error")
            return -10
    if num==2:
        try:
            _l = ["manage","cook","delivery"]
            i = _l.index(args[1])
            cursor = connection.cursor()
            strSql = "UPDATE employee set type="+str(i)+" where name=\""+str(args[0])+"\""

            cursor.execute(strSql)
            connection.commit()
            connection.close()
            return 0
        except:
            connection.rollback()
            print("error")
            return -10
    if num==3:
        try:
            cursor = connection.cursor()
            strSql = "UPDATE order_list set state="+str(args[1])+" where _id="+str(args[0])

            cursor.execute(strSql)
            connection.commit()
            connection.close()
            return 0
        except:
            connection.rollback()
            print("error")
            return -10