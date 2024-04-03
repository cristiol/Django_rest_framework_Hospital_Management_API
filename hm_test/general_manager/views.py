from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from account.views import IsAdmin
from .serializer import GeneralManagerRegistrationSerializer, GeneralManagerSerializer
from drf_spectacular.utils import extend_schema



class IsGeneralManager(BasePermission):
    """custom Permission class for General Manager"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='general_manager').exists())


class GeneralManageRegistrationView(APIView):
    """"API endpoint for General Manage Registration"""
    permission_classes = [IsAdmin]

    def post(self, request, format=None):
        registration_serializer = GeneralManagerRegistrationSerializer(data=request.data.get('user_data'))
        profile_serializer = GeneralManagerSerializer(data=request.data.get('profile_data'))
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


class CustomAuthToken(ObtainAuthToken):
    """This class returns custom Authentication token only for General Manager"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='general_manager').exists()
        if not account_approval:
            return Response(
                {
                    'message': "You are not authorised to login as a general_manager"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)
