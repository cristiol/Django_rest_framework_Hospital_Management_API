from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from .serializers import TreatmentSerializers
from rest_framework.response import Response
from .models import Treatment
from general_manager.views import IsGeneralManager
from doctor.views import IsDoctor
from drf_spectacular.utils import extend_schema



class TreatmentCreationView(APIView):
    permission_classes = [IsGeneralManager | IsDoctor]

    @extend_schema(request=TreatmentSerializers, responses=TreatmentSerializers)
    def post(self, request):
        serializer = TreatmentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TreatmentDetailView(APIView):
    permission_classes = [IsGeneralManager | IsDoctor]

    @extend_schema(request=TreatmentSerializers, responses=TreatmentSerializers)
    def get(self, request, pk):
        treatment = self.get_object(pk)
        serializer = TreatmentSerializers(treatment)
        return Response(serializer.data)

    @extend_schema(request=TreatmentSerializers, responses=TreatmentSerializers)
    def put(self, request, pk):
        treatment = self.get_object(pk)
        serializer = TreatmentSerializers(treatment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        treatment = self.get_object(pk)
        treatment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404
