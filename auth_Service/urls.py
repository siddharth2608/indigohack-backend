from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'authapp'

urlpatterns = [
	
	path('signup',views.RegisterUser,name='register_user'),
	path('signin',views.LoginUser,name='login_user'),
	path('signout',views.LogoutUser,name='logout_user')

]