from django.shortcuts import redirect, render




class Dinner_interface:
    @staticmethod
    def dfpage(request):
        if request.session["user"]:                                                 #
            name = request.session["user"][0]
        else:
            name = "Anonymous User"
        request.session["addition"]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        return render(request, 'dinnerfood.html', {'user_name': name})

    
    @staticmethod
    def dspage(request):
        if request.session["user"]:
            name = request.session["user"][0]
        else:
            name = "Anonymous User"
        chamno = request.session["dinner_menu"][3]
        return render(request, 'dinnerstyle.html', {'user_name': name, 'chamno':chamno})

    
    @staticmethod
    def addpage(request):
        if request.session["user"]:
            name = request.session["user"][0]
        else:
            name = "Anonymous User"
        return render(request, 'addition.html', {'user_name': name})


