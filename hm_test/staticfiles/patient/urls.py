from .views import (PatientRegistrationView, CustomAuthToken, PatientProfileView, UpdateAppliedTreatmentView,
                    UpdateRecommendedTreatmentView, UpdateAssignedAssistantsView)
from django.urls import path


urlpatterns = [
    path('registration/', PatientRegistrationView.as_view(), name='api_patient_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_patient_login'),
    path('patient-profile/<int:pk>/', PatientProfileView.as_view(), name='patient-profile'),
    path('update-applied-treatment/<int:pk>/', UpdateAppliedTreatmentView.as_view(),
         name='update-applied-treatment'),
    path('update-recommended-treatment/<int:pk>/', UpdateRecommendedTreatmentView.as_view(),
         name='update-recommended-treatment'),
    path('assign-assistants/<int:pk>/', UpdateAssignedAssistantsView.as_view(),
         name='assign-assistants')
]
