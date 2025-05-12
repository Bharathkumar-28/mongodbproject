from django.db import models
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    skills = models.TextField()
    experience = models.TextField()
    internships = models.TextField(blank=True, null=True)


