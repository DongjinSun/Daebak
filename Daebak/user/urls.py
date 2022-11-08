# from django.urls import path
# from . import views

from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cusmain, name='cm'),
    path('', views.loginpage, name='lp'),
    path('', views.signuppage, name='sp'),
    path('', views.orderpage, name='op'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('order/', views.order, name='order'),
]