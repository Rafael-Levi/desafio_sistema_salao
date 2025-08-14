from django.urls import path
from django.contrib.auth import views as auth_views
from ..views.logout import logout_user
app_name = 'login'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', logout_user, name='logout' )
]