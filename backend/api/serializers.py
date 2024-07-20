from rest_framework import serializers
from .models import Doctor, Patient, PDF, DoctorPatient

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['DoctorID', 'Name', 'Email', 'PasswordHash', 'Specialty']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['PatientID', 'Name', 'Email', 'PasswordHash']

class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ['PDFID', 'DoctorID', 'FilePath', 'UploadDate']

class DoctorPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPatient
        fields = ['DoctorID', 'PatientID']

