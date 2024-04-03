from rest_framework import serializers
from treatment.models import Treatment


class TreatmentSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    description = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = Treatment
        fields = ['id', 'name', 'description']
        partial = True


    def create(self, validated_data):
        return Treatment.objects.create(
            name=validated_data['name'],
            description=validated_data.get('description', '')
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

