from django.db import models
from account.models import User


class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name

    def delete(self, *args, **kwargs):
        if self.user:
            user = User.objects.get(pk=self.user.id)
            user.delete()

        super().delete(*args, **kwargs)


