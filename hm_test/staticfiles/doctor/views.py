from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import DoctorRegistrationSerializer, DoctorSerializer
from rest_framework.generics import get_object_or_404
from .models import Doctor
from general_manager.views import IsGeneralManager
from drf_spectacular.utils import extend_schema




class IsDoctor(BasePermission):
    """custom Permission class for Doctor"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='doctor').exists())


class CustomAuthToken(ObtainAuthToken):
    """This class returns custom Authentication token only for Doctor"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='doctor').exists()
        if not account_approval:
            return Response(
                {
                    'message': "You are not authorised to login as a doctor"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)


class DoctorRegistrationView(APIView):
    permission_classes = [IsGeneralManager | IsDoctor]

    @extend_schema(request=DoctorRegistrationSerializer, responses=DoctorRegistrationSerializer)
    def post(self, request, format=None):
        registration_serializer = DoctorRegistrationSerializer(data=request.data.get('user_data'))
        profile_serializer = DoctorSerializer(data=request.data.get('profile_data'))
        check_registration = registration_serializer.is_valid()
        check_profile = profile_serializer.is_valid()
        if check_registration and check_profile:
            doctor = registration_serializer.save()
            profile_serializer.save(user=doctor)
            return Response({
                'user_data': registration_serializer.data,
                'profile_data': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registration_serializer.errors,
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class DoctorProfileView(APIView):
    permission_classes = [IsGeneralManager]

    @extend_schema(request=DoctorSerializer, responses=DoctorSerializer)
    def put(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(responses=DoctorSerializer)
    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        patient = get_object_or_404(Doctor, pk=pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
