from django.urls import path
from user.views import (
    user,
    user_login,
    user_logout,
)


urlpatterns = [
    path('', user, name='user'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')
]
