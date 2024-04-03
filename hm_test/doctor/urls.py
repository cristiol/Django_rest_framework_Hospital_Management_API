from .views import DoctorRegistrationView, CustomAuthToken, DoctorProfileView
from django.urls import path


urlpatterns = [
    path('registration/', DoctorRegistrationView.as_view(), name='api_doctor_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_doctor_login'),
    path('doctor-profile/<int:pk>/', DoctorProfileView.as_view(), name='doctor-profile'),
]