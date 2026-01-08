from django.urls import path
from .views import SignupView, LoginView, logout_view, success_view

urlpatterns = [
    path('signup/', SignupView, name="signup"),
    path('login/', LoginView, name="login"),
    path('logout/', logout_view, name="logout"),
   path("success/", success_view, name="success"),
    #  path("auth/delete/", delete_account, name="delete_account"),
]
