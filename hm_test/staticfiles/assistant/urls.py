from .views import AssistantRegistrationView, CustomAuthToken, AssistantProfileView
from django.urls import path

urlpatterns = [
    path('registration/', AssistantRegistrationView.as_view(), name='api_assistant_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_assistant_login'),
    path('assistant-profile/<int:pk>/', AssistantProfileView.as_view(), name='assistant-profile'),
]