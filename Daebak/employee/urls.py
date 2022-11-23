from django.contrib import admin
from django.urls import path, include
from employee import views
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    
    ##Staff_interface
    path('', views.Staff_Interface.emmainpage, name='em'),
    path('emsignuppage/', views.Staff_Interface.emsignuppage, name='esp'),
    path('emchoosepage/', views.Staff_Interface.emchoosepage, name='ecp'),
    path('emstockpage/', views.Staff_Interface.emstockpage, name='estp'),
    path('emstockchangepage/', views.Staff_Interface.emstockchangepage, name='estcp'),
    path('emcookpage/', views.Staff_Interface.emcookpage, name='ecop'),
    path('emcookchangepage/', views.Staff_Interface.emcookchangepage, name='ecocp'),
    path('emempage/', views.Staff_Interface.emempage, name='eep'),
    path('ememchangepage/', views.Staff_Interface.ememchangepage, name='eecp'),
    
    ##Delivery_interface
    path('emdeliverypage/', views.Delivery_interface.emdeliverypage, name='edep'),
    path('emdeliverychangepage/', views.Delivery_interface.emdeliverychangepage, name='edecp'),
    
    ## Login_Staff
    path('emlogin/', views.Login_Staff.emlogin, name='emlogin'),
    path('emsignup/', views.Login_Staff.emsignup, name='emsignup'),
    path('root_check/', views.Login_Staff.root_check, name='root_check'),
    
    ##Stock main
    path('emstock/', views.Stock_main.emstock, name='emstock'),
    
    ##cook main
    path('emcook/', views.Cook_main.emcook, name='emcook'),
    
    ##Staff_main
    path('emphone/', views.Staff_main.emphone, name='emphone'),
    path('emjob/', views.Staff_main.emjob, name='emjob'),
    path('emdelivery/', views.Delivery_main.emdelivery, name='emdelivery'),
    
]