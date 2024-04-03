from rest_framework import status
from rest_framework.views import APIView
from doctor.models import Doctor
from patient.models import Patient
from rest_framework.response import Response
from treatment.serializers import TreatmentSerializers
from general_manager.views import IsGeneralManager
from doctor.views import IsDoctor


class DoctorPatientReportView(APIView):
    permission_classes = [IsGeneralManager]

    def get(self, request):
        doctors = Doctor.objects.prefetch_related('patient_set')
        report_data = []
        for doctor in doctors:
            patients = [patient.name for patient in doctor.patient_set.all() if
                        patient.name]  # Filter patients with name
            report_data.append({
                'doctor': doctor.get_name,  # Use get_name property for full name
                'patients': patients,
            })
        return Response(report_data)


class PatientTreatmentReportView(APIView):
    permission_classes = [IsGeneralManager | IsDoctor]

    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        applied_treatments = []
        if patient.applied_treatment:
            serializer = TreatmentSerializers(patient.applied_treatment)
            applied_treatments.append(serializer.data)

        return Response({"patient": patient.name, "applied_treatments": applied_treatments})
