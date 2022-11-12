from django.contrib import admin
from django.urls import path, include
from employee import views
from django.conf import settings
import debug_toolbar

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
    path('emstock/', views.emstock, name='emstock'),
    #path('emcook/', views.emcook, name='emcook'),
    path('emdelivery/', views.emdelivery, name='emdelivery'),
    path('root_check/', views.root_check, name='root_check'),
    path('__debug__/', include(debug_toolbar.urls))
]