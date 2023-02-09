from django.urls import path

from users.views import SignUp, SignIn, logout_view

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('logout/', logout_view, name='logout'),
]
