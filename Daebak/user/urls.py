from django.contrib import admin
from django.urls import path

import user.login as login
import user.order as order
import user.dinner as dinner

urlpatterns = [
    path('admin/', admin.site.urls),
    
    ##Login_interface
    path('', login.Login_interface.cusmainpage, name='cm'),
    path('loginpage/', login.Login_interface.loginpage, name='lp'),
    path('signuppage/', login.Login_interface.signuppage, name='sp'),
    path('userorderlistpage/', login.Login_interface.userorderlistpage, name='uolp'),
    path('anorder/', login.Login_interface.anoorder, name='ao'),
    
    ##Login_main
    path('reorder/', login.Login_main.reorder, name='ro'),
    path('logout/', login.Login_main.logout, name='logout'),
    path('login/', login.Login_main.login, name='login'),
    path('signup/', login.Login_main.signup, name='signup'),
    
    ##Dinner_interface
    path('dfpage/', dinner.Dinner_interface.dfpage, name='dfp'),
    path('dspage/', dinner.Dinner_interface.dspage, name='dsp'),
    path('addpage/', dinner.Dinner_interface.addpage, name='ap'),


    ##Dinner_main
    path('df/', dinner.Dinner_main.dinner_food, name='df'), 
    path('ds/', dinner.Dinner_main.dinner_style, name='ds'),
    path('add/', dinner.Dinner_main.add, name='add'),
    path('addorder/', dinner.Dinner_main.addorder, name='addorder'),
    
    
    ##Order_interface
    path('orderpage/', order.Order_interface.orderpage, name='op'),
    path('orderfin/', order.Order_interface.orderfin, name='of'),
    
    ##Order_main
    path('order/', order.Order_main.order, name='order'),
    
]
