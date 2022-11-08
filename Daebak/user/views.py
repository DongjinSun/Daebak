from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Stock, Employee, OrderList
from .datacontrol import *

# Create your views here.


# userorderlist.html
# 주문내역 전달하기

# order.html
# 주문 상품

# 주문자 정보
# 회원: 이름, 전화번호, 주소, 카드번호를 전달해야 함.

