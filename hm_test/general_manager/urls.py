from .views import CustomAuthToken, GeneralManageRegistrationView
from django.urls import path


urlpatterns = [
    path('registration/', GeneralManageRegistrationView.as_view(), name='api_general-manager_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_general-manager_login'),
]