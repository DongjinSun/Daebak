from django.contrib import admin
from django.urls import path, include


import employee.cook as cook
import employee.login as login
import employee.delivery as delivery
import employee.manage as manage
import employee.stock as stock

from django.conf import settings
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    
    ##Login_interface
    path('', login.Login_interface.emmainpage, name='em'),
    path('emsignuppage/', login.Login_interface.emsignuppage, name='esp'),
    path('emchoosepage/', login.Login_interface.emchoosepage, name='ecp'),
    
    ## Login_main
    path('emlogin/', login.Login_main.emlogin, name='emlogin'),
    path('emsignup/', login.Login_main.emsignup, name='emsignup'),
    path('root_check/', login.Login_main.root_check, name='root_check'),
    
    ##Stock_interface
    path('emstockpage/', stock.Stock_interface.emstockpage, name='estp'),
    path('emstockchangepage/', stock.Stock_interface.emstockchangepage, name='estcp'),

    ##Stock main
    path('emstock/', stock.Stock_main.emstock, name='emstock'),
    
    ##Cook_interface
    path('emcookpage/', cook.Cook_interface.emcookpage, name='ecop'),
    path('emcookchangepage/', cook.Cook_interface.emcookchangepage, name='ecocp'),
    
    ##cook main
    path('emcook/', cook.Cook_main.emcook, name='emcook'),
    
    ##Manage_interface
    path('emempage/', manage.Manage_interface.emempage, name='eep'),
    path('ememchangepage/', manage.Manage_interface.ememchangepage, name='eecp'),
    
    ##Manage_main
    path('emphone/', manage.Manage_main.emphone, name='emphone'),
    path('emjob/', manage.Manage_main.emjob, name='emjob'),    

    ##Delivery_interface
    path('emdeliverypage/', delivery.Delivery_interface.emdeliverypage, name='edep'),
    path('emdeliverychangepage/', delivery.Delivery_interface.emdeliverychangepage, name='edecp'),
    
    ##Delivery_main
    path('emdelivery/', delivery.Delivery_main.emdelivery, name='emdelivery'),
    

    

    

    

    

    
]