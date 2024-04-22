

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app01 import views

urlpatterns = [
    path('sendVerifycode/',views.SendVerifyCode.as_view(), name='sendVerifycode'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('userList/',views.UserInfoView.as_view(), name='userList'),
    path('banList/', views.BanlistView.as_view(), name='banList'),
    path('search/', views.SearchView.as_view(), name='search'),
]