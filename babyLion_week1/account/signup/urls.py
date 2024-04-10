from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import firstpage, signup, signup_success, login_view, home, profile_update_view

urlpatterns = [
    path('', firstpage, name='firstpage'),  
    path('signup/', signup, name='signup'),  
    path('signup/signup_success/<str:pk>', signup_success, name='signup_success'),  
    path('login_view/', login_view, name='login_view'), 
    path('home/', home, name='home'),
    path('profile/update/', profile_update_view, name='profile_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
