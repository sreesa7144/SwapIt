from django.urls import path
from . import views
from django.contrib.auth.views import auth_login,auth_logout
app_name = 'accounts'
urlpatterns=[
    path('signup/',views.UserFormView.as_view(),name='signup'),
   # path('login/', auth_login(),{'template_name':'accounts/login.html'},name='login'),
    path('',views.MainPage,name='main'),
    #path('connection/',views.formView,name='loginform'),
    #path('logout/', auth_logout, {'template_name': 'accounts/mainpage.html'}, name='logout'),
    ]
