from .views import DoctorPatientReportView, PatientTreatmentReportView
from django.urls import path


urlpatterns = [
    path('doctor-patient-report/', DoctorPatientReportView.as_view(), name='doctor-patient-report'),
    path('patient-treatment-report/<int:pk>/', PatientTreatmentReportView.as_view(), name='treatment-patient-report'),
]