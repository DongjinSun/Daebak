from rest_framework.serializers import ModelSerializer
from .models import Stock, User, Employee, OrderList

class stockDataSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        
class userDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class employeeDataSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class orderDataSerializer(ModelSerializer):
    class Meta:
        model = OrderList
        fields = '__all__'
        
def get_data(num):
    f_d = {0:stockDataSerializer,1:userDataSerializer,
           2:employeeDataSerializer,3:orderDataSerializer}
    data_l = [Stock,User,Employee, OrderList]
    datas = data_l[num].objects.all()
    serializer = f_d[num](datas, many=True)
    return dict(serializer.data[0])


def Insert_data(request,num):
    
    reqData = request.data
    f_d = {0:stockDataSerializer,1:userDataSerializer,
           2:employeeDataSerializer,3:orderDataSerializer}
    serializer = f_d[num](data = reqData)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def change_data(request, pk,num):
    reqData = request.data
    data_l = [Stock,User,Employee, OrderList]
    data = data_l[num].objects.get(id=pk)
    f_d = {0:stockDataSerializer,1:userDataSerializer,
           2:employeeDataSerializer,3:orderDataSerializer}
    serializer = f_d[num](instance=data, data=reqData)
    
    if serializer.is_valid():
        serializer.save()
        