from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.validators import EmailValidator, MinLengthValidator
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Doctor(AbstractBaseUser):
    DoctorID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True, validators=[EmailValidator()])
    PasswordHash = models.CharField(max_length=255)
    Specialty = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['Name', 'Specialty']

    objects = CustomUserManager()

    def __str__(self):
        return self.Name

class Patient(AbstractBaseUser):
    PatientID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True, validators=[EmailValidator()])
    PasswordHash = models.CharField(max_length=255)

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['Name']

    objects = CustomUserManager()

    def __str__(self):
        return self.Name

class PDF(models.Model):
    PDFID = models.AutoField(primary_key=True)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    FilePath = models.CharField(max_length=255)
    UploadDate = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.FilePath:
            file_name = os.path.basename(self.FilePath)
            content = default_storage.open(self.FilePath).read()
            content_file = ContentFile(content, name=file_name)
            self.FilePath = default_storage.save(file_name, content_file)
        super().save(*args, **kwargs)

class DoctorPatient(models.Model):
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('DoctorID', 'PatientID')

    def __str__(self):
        return f'Doctor: {self.DoctorID.Name}, Patient: {self.PatientID.Name}'
