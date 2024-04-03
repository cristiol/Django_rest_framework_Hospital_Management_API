from rest_framework import serializers
from django.contrib.auth.models import Group
from account.models import User
from treatment.models import Treatment
from assistant.models import Assistant
from doctor.models import Doctor
from .models import Patient


class PatientRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(label='Username:')
    first_name = serializers.CharField(label='First name:')
    last_name = serializers.CharField(label='Last name:', required=False)
    password = serializers.CharField(label='Password:', style={'input_type': 'password'}, write_only=True, min_length=8,
                                     help_text="Your password must contain at least 8 characters and should not be entirely numeric."
                                     )
    password2 = serializers.CharField(label='Confirm password:', style={'input_type': 'password'}, write_only=True)


    def validate_username(self, username):
        username_exists = User.objects.filter(username__iexact=username)
        if username_exists:
            raise serializers.ValidationError({'username': 'This username already exists'})
        return username


    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password


    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password': 'password must match'})
        return data


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            status=False
        )
        user.set_password(validated_data['password'])
        user.save()
        group_patient, created = Group.objects.get_or_create(name='patient')
        group_patient.user_set.add(user)
        return user


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctors = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), many=True, required=False, allow_null=True)
    assistants = serializers.PrimaryKeyRelatedField(queryset=Assistant.objects.all(), many=True, required=False, allow_null=True)
    recommended_treatment = serializers.PrimaryKeyRelatedField(queryset=Treatment.objects.all(), required=False, allow_null=True)
    applied_treatment = serializers.PrimaryKeyRelatedField(queryset=Treatment.objects.all(), required=False, allow_null=True)


    class Meta:
        model = Patient
        fields = '__all__'  # Include all fields if desired, customize as needed
        partial = True  # Allow partial updates



