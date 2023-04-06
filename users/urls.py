from django.urls import path
from . import views

urlpatterns = [
    path('authorization/', views.AuthorizationAPIView.as_view()),
    path('registration/', views.RegistartionAPIView.as_view()),
    path('confirm/', views.ConfirmAPIView.as_view())
]