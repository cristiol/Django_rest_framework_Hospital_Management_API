from account.models import User
from treatment.models import Treatment
from assistant.models import Assistant
from doctor.models import Doctor
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    doctors = models.ManyToManyField(Doctor, blank=True)
    assistants = models.ManyToManyField(Assistant, blank=True)
    recommended_treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, blank=True, null=True, related_name='recommended_treatment')
    applied_treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, blank=True, null=True, related_name='applied_treatment')

    def __str__(self):
        return self.name

    @property
    def get_id(self):
        return self.user.id


    def delete(self, *args, **kwargs):
        if self.user:
            user = User.objects.get(pk=self.user.id)
            user.delete()

        super().delete(*args, **kwargs)
