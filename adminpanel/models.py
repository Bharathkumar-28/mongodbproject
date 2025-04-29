from django.db import models
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    skills = models.JSONField()
    experience = models.JSONField()
    internships = models.JSONField()

    def __str__(self):
        return self.name

