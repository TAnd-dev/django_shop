from django.urls import path

from users.views import SignUp, SignIn, logout_view, ProfileView, ChangeEmailView, ChangeDataView,\
    PurchaseView

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-email/', ChangeEmailView.as_view(), name='change_email'),
    path('profile/change-user-data/', ChangeDataView.as_view(), name='change_user_data'),
    path('profile/purchases/', PurchaseView.as_view(), name='purchases'),
    path('logout/', logout_view, name='logout'),
]
