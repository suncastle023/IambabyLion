from django.urls import path
from .views import firstpage, signup, signup_success, login_view

urlpatterns = [
    path('', firstpage, name='firstpage'),  
    path('signup/', signup, name='signup'),  
    path('signup/signup_success/', signup_success, name='signup_success'),  
    path('login_view/', login_view, name='login_view'), 
]
