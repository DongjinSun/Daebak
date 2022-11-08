from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cusmainpage, name='cm'),
    path('loginpage/', views.loginpage, name='lp'),
    path('signuppage/', views.signuppage, name='sp'),
    path('userorderlistpage/', views.userorderlistpage, name='uolp'),
    path('orderpage/', views.orderpage, name='op'),
    path('dfpage/', views.dfpage, name='dfp'),
    path('dspage/', views.dspage, name='dsp'),
    path('addpage/', views.addpage, name='ap'),
    
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('order/', views.order, name='order'),
]