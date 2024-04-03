from django.urls import path
from .views import TreatmentCreationView, TreatmentDetailView

urlpatterns = [
    path('creation/', TreatmentCreationView.as_view(), name='treatment_creation'),
    path('treatment-detail/<int:pk>/', TreatmentDetailView.as_view(), name='treatment-detail'),
]