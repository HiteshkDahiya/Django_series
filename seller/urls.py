from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('signupseller/', views.RegisterSellerView.as_view(), name="signupseller"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
]