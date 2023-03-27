from hashlib import sha256

from django.contrib.auth.hashers import make_password
from django.db import models


class Credentials(models.Model):
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving the model
        self.password = sha256(str(self.password).encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)
