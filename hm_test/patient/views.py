from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from assistant.models import Assistant
from doctor.models import Doctor
from .models import Patient
from .serializers import PatientRegistrationSerializer, PatientSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from doctor.views import IsDoctor
from general_manager.views import IsGeneralManager
from drf_spectacular.utils import extend_schema



class IsPatient(BasePermission):
    """custom Permission class for Patient"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='patient').exists())


class PatientRegistrationView(APIView):
    """"API endpoint for patient Registration"""
    permission_classes = [IsDoctor | IsGeneralManager]

    @extend_schema(request=PatientRegistrationSerializer,responses=PatientRegistrationSerializer)
    def post(self, request, format=None):
        registration_serializer = PatientRegistrationSerializer(data=request.data.get('user_data'))
        profile_serializer = PatientSerializer(data=request.data.get('profile_data'))
        check_registration = registration_serializer.is_valid()
        check_profile = profile_serializer.is_valid()
        if check_registration and check_profile:
            patient = registration_serializer.save()
            profile_serializer.save(user=patient)
            return Response({
                'user_data': registration_serializer.data,
                'profile_data': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registration_serializer.errors,
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class PatientProfileView(APIView):

    permission_classes = [IsGeneralManager]

    @extend_schema(request=PatientSerializer, responses=PatientSerializer)
    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=PatientSerializer, responses=PatientSerializer)
    def put(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateAppliedTreatmentView(APIView):

    @extend_schema(request=PatientSerializer,responses=PatientSerializer)
    def put(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk) # Get the patient object or return a 404 if not found
        user_id = request.user.id # Get the ID of the current user (assistant)

        try:
            assistant = Assistant.objects.get(user_id=user_id)
            assistant_id = assistant.id
        except Assistant.DoesNotExist:
            assistant_id = None

        if assistant_id is not None and assistant_id in patient.assistants.all().values_list('id', flat=True):
            applied_treatment_data = request.data.get('applied_treatment')
            if applied_treatment_data is not None:
                # Create a partial serializer with only the applied_treatment field
                serializer = PatientSerializer(patient, data={'applied_treatment': applied_treatment_data},
                                               partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"detail": "The assistant does not have permission to modify anny other fields"},
                    status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)


class UpdateRecommendedTreatmentView(APIView):

    @extend_schema(request=PatientSerializer,responses=PatientSerializer)
    def put(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)  # Get the patient object or return a 404 if not found
        user_id = request.user.id # Get the ID of the current user (assistant)
        # Try to get the Doctor object corresponding to the user ID
        try:
            doctor = Doctor.objects.get(user_id=user_id)
            doctor_id = doctor.id
        except Doctor.DoesNotExist:
            doctor_id = None

        if doctor_id is not None and doctor_id in patient.doctors.all().values_list('id', flat=True):
            recommended_treatment_data = request.data.get('recommended_treatment')
            if recommended_treatment_data:
                # Create a partial serializer with only the recommended_treatment field
                serializer = PatientSerializer(patient, data={'recommended_treatment': recommended_treatment_data},
                                               partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"detail": "The doctor does not have permission to modify anny other fields"},
                    status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)


class UpdateAssignedAssistantsView(APIView):

    @extend_schema(request=PatientSerializer,responses=PatientSerializer)
    def put(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)  # Get the patient object or return a 404 if not found
        user_id = request.user.id  # Get the ID of the current user (doctor)
        # Try to get the Doctor object corresponding to the user ID
        try:
            doctor = Doctor.objects.get(user_id=user_id)
            doctor_id = doctor.id
        except Doctor.DoesNotExist:
            doctor_id = None

        if doctor_id is not None and doctor_id in patient.doctors.all().values_list('id', flat=True):

            assigned_assistants_data = request.data.get('assistants')
            if assigned_assistants_data is not None:
                # Create a partial serializer with only the recommended_treatment field
                serializer = PatientSerializer(patient, data={'assistants': assigned_assistants_data},
                                               partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"detail": "The doctor does not have permission to modify anny other fields"},
                    status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)


class CustomAuthToken(ObtainAuthToken):
    """This class returns custom Authentication token only for Patient"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='patient').exists()
        if not account_approval:
            return Response(
                {
                    'message': "You are not authorised to login as a patient"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)