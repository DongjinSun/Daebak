from django.shortcuts import render

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
