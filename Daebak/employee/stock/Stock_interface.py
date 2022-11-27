import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from employee.models import Stock
from django.shortcuts import redirect, render


class Stock_interface:
    stock_list = ["상자 접시","도자기 접시","도자기 컵","발렌타인 접시","플라스틱 잔","스테이크","샐러드","계란","베이컨","빵","바게트빵","커피","와인","샴페인"]
    
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
