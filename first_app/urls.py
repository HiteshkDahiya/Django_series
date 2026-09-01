from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.Index.as_view(), name='index'),
    path('contactus/', views.contactus2, name="contact"),
    path('contactusclass/', views.ContactUs.as_view(), name="contactclass"),

    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
]