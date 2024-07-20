from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import boto3
from .models import Doctor, Patient, PDF, DoctorPatient
from .serializers import PatientSerializer, PDFSerializer

@api_view(['POST'])
def register_doctor(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    specialty = request.data.get('specialty')

    if not all([name, email, password]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            user = User.objects.create_user(username=email, email=email, password=password)
            Doctor.objects.create(Name=name, Email=email, PasswordHash=user.password, Specialty=specialty)
        return Response({'message': 'Doctor registered successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_doctor(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register_patient(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([name, email, password]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            user = User.objects.create_user(username=email, email=email, password=password)
            Patient.objects.create(Name=name, Email=email, PasswordHash=user.password)
        return Response({'message': 'Patient registered successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_patient(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_pdf(request):
    try:
        doctor = Doctor.objects.get(Email=request.user.email)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    pdf_file = request.FILES.get('pdf')

    if not pdf_file:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)

    file_name = f'doctor_{doctor.DoctorID}/{pdf_file.name}'
    s3.upload_fileobj(pdf_file, settings.AWS_STORAGE_BUCKET_NAME, file_name)

    PDF.objects.create(DoctorID=doctor, FilePath=file_name)
    
    return Response({'message': 'PDF uploaded successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def link_patient(request):
    try:
        doctor = Doctor.objects.get(Email=request.user.email)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)

    patient_email = request.data.get('patient_email')
    if not patient_email:
        return Response({'error': 'Patient email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient = Patient.objects.get(Email=patient_email)
        DoctorPatient.objects.get_or_create(DoctorID=doctor, PatientID=patient)
        return Response({'message': 'Patient linked successfully'}, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DoctorPDFList(generics.ListAPIView):
    serializer_class = PDFSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        try:
            doctor = Doctor.objects.get(Email=self.request.user.email)
        except Doctor.DoesNotExist:
            return PDF.objects.none()
        return PDF.objects.filter(DoctorID=doctor)

class DoctorPatientList(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        try:
            doctor = Doctor.objects.get(Email=self.request.user.email)
        except Doctor.DoesNotExist:
            return Patient.objects.none()
        return Patient.objects.filter(doctorpatient__DoctorID=doctor)
