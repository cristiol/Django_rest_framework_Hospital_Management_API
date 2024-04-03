from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from .models import Assistant
from .serializers import AssistantRegistrationSerializer, AssistantSerializer
from general_manager.views import IsGeneralManager
from drf_spectacular.utils import extend_schema


class IsAssistant(BasePermission):
    """custom Permission class for Assistant"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='assistant').exists())



class AssistantRegistrationView(APIView):
    """"API endpoint for Assistant Registration"""
    permission_classes = [IsGeneralManager]

    @extend_schema(request=AssistantRegistrationSerializer, responses=AssistantRegistrationSerializer)
    def post(self, request, format=None):
        registration_serializer = AssistantRegistrationSerializer(data=request.data.get('user_data'))
        profile_serializer = AssistantSerializer(data=request.data.get('profile_data'))
        check_registration = registration_serializer.is_valid()
        check_profile = profile_serializer.is_valid()
        if check_registration and check_profile:
            assistant = registration_serializer.save()
            profile_serializer.save(user=assistant)
            return Response({
                'user_data': registration_serializer.data,
                'profile_data': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registration_serializer.errors,
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class AssistantProfileView(APIView):
    permission_classes = [IsGeneralManager]

    @extend_schema(request=AssistantSerializer, responses=AssistantSerializer)
    def put(self, request, pk):
        assistant = get_object_or_404(Assistant, pk=pk)
        serializer = AssistantSerializer(assistant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(request=AssistantSerializer, responses=AssistantSerializer)
    def get(self, request, pk):
        assistant = get_object_or_404(Assistant, pk=pk)
        serializer = AssistantSerializer(assistant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        patient = get_object_or_404(Assistant, pk=pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CustomAuthToken(ObtainAuthToken):
    """This class returns custom Authentication token only for Assistant"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='assistant').exists()
        if not account_approval:
            return Response(
                {
                    'message': "You are not authorised to login as a assistant"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)

