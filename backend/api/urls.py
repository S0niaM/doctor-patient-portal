from django.urls import path
from .views import register_doctor, login_doctor, register_patient, login_patient, upload_pdf, link_patient, DoctorPDFList, DoctorPatientList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/doctor/', register_doctor, name='register_doctor'),
    path('login/doctor/', login_doctor, name='login_doctor'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register_doctor/', register_doctor, name='register_doctor'),
    path('register/patient/', register_patient, name='register_patient'),
    path('login/patient/', login_patient, name='login_patient'),
    path('upload_pdf/', upload_pdf, name='upload_pdf'),
    path('link_patient/', link_patient, name='link_patient'),
    path('doctor_pdfs/', DoctorPDFList.as_view(), name='doctor_pdfs'),
    path('doctor_patients/', DoctorPatientList.as_view(), name='doctor_patients'),
]
