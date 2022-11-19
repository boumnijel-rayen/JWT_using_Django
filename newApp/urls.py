from django.urls import path
from . import views

urlpatterns = [
    path('employee', views.emplyeeApiView.as_view()),
    path('employee/<int:pk>', views.emplyeeParamsApiView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
]
