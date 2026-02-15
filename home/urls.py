from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("",views.homepage,name="home"),
    path("contactus/",views.contactus,name="contact"),
    path("about/",views.about,name="about"),
    path("fordoctor/",views.fordoctor,name="fordoctor"),
    path("login/",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("otp/",views.otp,name="otp"),
    path("userhp/<uemailid>/",views.userhomepage,name="userhp"),
    path("appoitment/<uemailid>/",views.appointment,name="appointment"),
    path("emergencyappoitment/<uemailid>/",views.emergencyappointment,name="emergencyappointment"),
    path("applist/<uemailid>/",views.appointmentlist,name="applist"),
    path("history/<uemailid>/",views.history,name="history"),
    path("userdetail/<uemailid>/",views.userdetail,name="userdetail"),
    path("doctorschedule/<demail>/",views.doctorschedule,name="doctors"),
    path("prescriptionpage/<uemail>/",views.prescription,name="prescription"),
    path("userlogout/",views.userlogout,name="userlogout"),
    path("bookappoitment/<demailid>",views.bookuserappointment,name="bookappointment"),
    path("bookemergencyappoitment/<demailid>",views.bookemergencyappointment,name="bookemergencyappointment"),
    
    # Phase 2: Advanced Features URLs
    path("rate-doctor/<doctor_email>/", views.rate_doctor, name="rate_doctor"),
    path("doctor-profile/<doctor_email>/", views.doctor_profile, name="doctor_profile"),
    path("payment/<int:appointment_id>/", views.process_payment, name="process_payment"),
    path("payment-success/<int:payment_id>/", views.payment_success, name="payment_success"),
    path("download-invoice/<int:payment_id>/", views.download_invoice, name="download_invoice"),
    path("payment-history/<user_email>/", views.payment_history, name="payment_history"),
    path("medical-records/<user_email>/", views.medical_records, name="medical_records"),
    path("add-medical-record/<patient_email>/", views.add_medical_record, name="add_medical_record"),
    path("notifications/", views.notifications, name="notifications"),
    path("mark-notification-read/<int:notification_id>/", views.mark_notification_read, name="mark_notification_read"),
    path("patient-dashboard/<user_email>/", views.patient_dashboard, name="patient_dashboard"),
    path("doctor-dashboard/<doctor_email>/", views.doctor_dashboard, name="doctor_dashboard"),
]
