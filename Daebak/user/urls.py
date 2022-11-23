from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    ##Login_interface
    path('', views.Login_interface.cusmainpage, name='cm'),
    path('loginpage/', views.Login_interface.loginpage, name='lp'),
    path('signuppage/', views.Login_interface.signuppage, name='sp'),
    path('userorderlistpage/', views.Login_interface.userorderlistpage, name='uolp'),
    path('anorder/', views.Login_interface.anoorder, name='ao'),
    
    ##Login_main
    path('reorder/', views.Login_main.reorder, name='ro'),
    path('logout/', views.Login_main.logout, name='logout'),
    path('login/', views.Login_main.login, name='login'),
    path('signup/', views.Login_main.signup, name='signup'),
    
    ##Dinner_interface
    path('dfpage/', views.Dinner_interface.dfpage, name='dfp'),
    path('dspage/', views.Dinner_interface.dspage, name='dsp'),
    path('addpage/', views.Dinner_interface.addpage, name='ap'),


    ##Dinner_main
    path('df/', views.Dinner_main.dinner_food, name='df'), 
    path('ds/', views.Dinner_main.dinner_style, name='ds'),
    path('add/', views.Dinner_main.add, name='add'),
    path('addorder/', views.Dinner_main.addorder, name='addorder'),
    
    
    ##Order_interface
    path('orderpage/', views.Order_interface.orderpage, name='op'),
    path('orderfin/', views.Order_interface.orderfin, name='of'),
    
    ##Order_main
    path('order/', views.Order_main.order, name='order'),
    
]
