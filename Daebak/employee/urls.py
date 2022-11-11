from django.contrib import admin
from django.urls import path
from employee import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.emmainpage, name='em'),
    # path('emloginpage/', views.emloginpage, name='elp'),
    path('emsignuppage/', views.emsignuppage, name='esp'),
    path('emchoosepage/', views.emchoosepage, name='ecp'),
    path('emstockpage/', views.emstockpage, name='estp'),
    path('emcookpage/', views.emcook, name='ecop'),
    path('emempage/', views.emempage, name='eep'),
    path('emdeliverypage/', views.emdeliverypage, name='edep'),


    path('emlogin/', views.emlogin, name='emlogin'),
    path('emsignup/', views.emsignup, name='emsignup'),
    path('emem/', views.emem, name='emem'),
    path('emstock/', views.emstock, name='emstock'),
    #path('emcook/', views.emcook, name='emcook'),
    path('emdelivery/', views.emdelivery, name='emdelivery'),
    path('root_check/', views.root_check, name='root_check')
]