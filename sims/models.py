from django.db import models


# Create your models here.
class Student(models.Model):
    student_no = models.CharField(max_length=32, unique=True)
    student_name = models.CharField(max_length=32)
    job_name = models.CharField(max_length=5000, null=True, blank=True)
    selected_targets_str = models.CharField(max_length=5000, null=True, blank=True)
