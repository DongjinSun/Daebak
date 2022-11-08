from django.shortcuts import render

# Create your views here.
def home(request):
    chat = 'Hello'
    return render(request, 'em_stock.html', {'user_chat': chat})