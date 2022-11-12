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
    # path('cpage/', views.cpage, name='cp'),
    path('addpage/', views.addpage, name='ap'),
    
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    ## 디너 종류
    path('df/', views.df, name='df'), 
    #디너 스타일
    #path('ds/', views.ds, name='ds'),
    path('simnum/', views.simnum, name='simnum'),
    path('granum/', views.granum, name='granum'),
    path('delnum/', views.delnum, name='delnum'),
    path('add/', views.add, name='add'),
    path('addorder/', views.addorder, name='addorder'),
    path('order/', views.order, name='order'),
]