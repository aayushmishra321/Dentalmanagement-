
from django.shortcuts import render, redirect
from home.models import UserDetail
from home.models import UserContacts
from home.models import DoctorsMessage
from home.models import DoctorDetail
from home.models import bookappointment
from home.models import appointmenthistory
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
import random
import logging

logger = logging.getLogger(__name__)
# --------------------------------Create your views here.-------------------------------------------------------------
# ----------------------------main homepage------------------------------
def homepage(request):
    # Check if user is logged in via session
    if request.session.get('user_logged_in') and request.session.get('user_email'):
        return redirect('userhp', request.session.get('user_email'))
    
    return render(request, "index.html", {
        'check': request.session.get('user_logged_in', False)
    })


# ---------------------------contact page-----------------------------------
def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('useremail')
        contact = request.POST.get('usercontact')
        message = request.POST.get('usermessage')
        
        if not all([name, email, contact, message]):
            messages.warning(request, "Fill all details!")
            return redirect('contact')
            
        try:
            user_contact = UserContacts(
                name=name, 
                email=email, 
                contact=contact, 
                message=message, 
                date=datetime.today()
            )
            user_contact.save()
            messages.success(request, "Message sent successfully")
        except Exception as e:
            messages.error(request, f"Failed to send message: {str(e)}")
        
        return redirect("contact")

    return render(request, "contactus.html", {
        'check': request.session.get('user_logged_in', False),
        'uemail': request.session.get('user_email', '')
    })


# -----------------------------------about page------------------------------------------
def about(request):
    return render(request, "aboutus.html", {
        'check': request.session.get('user_logged_in', False),
        'uemail': request.session.get('user_email', '')
    })


# ------------------------------------doctor page----------------------------------------
def fordoctor(request):
    # Check if user is already logged in
    if request.session.get('user_logged_in') and request.session.get('user_email'):
        return redirect('userhp', request.session.get('user_email'))
   
    if request.method == 'POST':
        if request.POST.get("form_type") == "contactOne":
            name = request.POST.get('doctorname')
            email = request.POST.get('doctoremail')
            contact = request.POST.get('doctorcontact')
            message = request.POST.get('doctormessage')
            
            if not all([name, email, contact, message]):
                messages.warning(request, "Fill all details!")
                return redirect('fordoctor')
                
            try:
                user_contact = DoctorsMessage(
                    name=name, 
                    email=email, 
                    contact=contact, 
                    message=message, 
                    date=datetime.today()
                )
                user_contact.save()
                messages.success(request, "Message sent successfully")
            except Exception as e:
                messages.error(request, f"Failed to send message: {str(e)}")
            
            return redirect("fordoctor")
        elif request.POST.get("form_type") == "loginOne":
            demail = request.POST.get('docemail')
            dpassword = request.POST.get('docpassword')
            if not demail or not dpassword:
                messages.warning(request, "Fill all details!")
                return redirect('fordoctor')
                
            try:
                if DoctorDetail.objects.filter(email=demail).exists():
                    doctor = DoctorDetail.objects.get(email=demail)
                    
                    if doctor.password == dpassword:
                        # Set session variables for doctor login
                        request.session['doctor_logged_in'] = True
                        request.session['doctor_email'] = demail
                        
                        messages.success(request, "Login successful")
                        return redirect("doctors", demail)
                    else:
                        messages.warning(request, "Password is incorrect!")
                        return redirect("fordoctor")
                else:
                    messages.warning(request, "Email does not exist!")
                    return redirect("fordoctor")
            except Exception as e:
                messages.error(request, f"Login failed: {str(e)}")
                return redirect("fordoctor")

    return render(request, "doctorpage.html", {
        'check': request.session.get('user_logged_in', False)
    })



# -----------------------------------login-------------------------------------------
def login(request):
    # Check if user is already logged in via session
    if request.session.get('user_logged_in') and request.session.get('user_email'):
        return redirect('userhp', request.session.get('user_email'))
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.warning(request, "Fill all details!")
            return redirect('login')
            
        try:
            if UserDetail.objects.filter(email=email).exists():
                user = UserDetail.objects.get(email=email)
                
                if user.password == password:
                    # Set session variables instead of global variables
                    request.session['user_logged_in'] = True
                    request.session['user_email'] = email
                    
                    messages.success(request, "Login successful")
                    return redirect("userhp", email)
                else:
                    messages.warning(request, "Password incorrect!")
                    return redirect("login")
            else:
                messages.warning(request, "Email does not exist!")
                return redirect("login")
                
        except Exception as e:
            messages.error(request, f"Login failed: {str(e)}")
            return redirect("login")

    return render(request, "login.html")



# ----------------------------------------------Registration---------------------------------------
def register(request):
    # Check if user is already logged in via session
    if request.session.get('user_logged_in') and request.session.get('user_email'):
        return redirect('userhp', request.session.get('user_email'))
    
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('uemail')
        contact = request.POST.get('ucontact')
        dateofbirth = request.POST.get('udob')
        gender = request.POST.get('ugender')
        address = request.POST.get('uaddress')
        pincode = request.POST.get('upincode')
        password = request.POST.get('newpassword')
        cpassword = request.POST.get('confirmpassword')
        
        # Validation
        if not all([name, email, contact, dateofbirth, gender, address, pincode, password, cpassword]):
            messages.warning(request, "Fill all details!")
            return redirect('register')
        
        if password == cpassword:
            if UserDetail.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists!")
                return redirect("register")
            elif UserDetail.objects.filter(contact=contact).exists():
                messages.warning(request, "Phone number already exists!")
                return redirect("register")
            else:
                try:
                    # Create user
                    user_detail = UserDetail(
                        name=name, 
                        email=email, 
                        contact=contact, 
                        dateofbirth=dateofbirth, 
                        gender=gender, 
                        address=address, 
                        pincode=pincode, 
                        password=password
                    )
                    user_detail.save()
                    
                    # Set session variables instead of global variables
                    request.session['user_logged_in'] = True
                    request.session['user_email'] = email
                    
                    # Send welcome email
                    try:
                        send_mail(
                            "Welcome to DENTIST World",
                            f"Hi {name}, thank you for registering in DENTIST. We hope we can give you a beautiful smile. Thank you",
                            "dentalmanagement00@gmail.com",
                            [email],
                            fail_silently=True,  # Don't fail if email doesn't send
                        )
                    except Exception as e:
                        # Log email error but don't fail registration
                        print(f"Email sending failed: {e}")
                    
                    messages.success(request, "Registered successfully")
                    return redirect("userhp", email)
                    
                except Exception as e:
                    messages.error(request, f"Registration failed: {str(e)}")
                    return redirect("register")
        else:
            messages.warning(request, "Passwords do not match")
            return redirect("register")
   
    return render(request, "registrationpage.html")


    
    
# -------------------------------------------changepassword----------------------------------------------
def otp(request):
    # Check if user is already logged in via session
    if request.session.get('user_logged_in') and request.session.get('user_email'):
        return redirect('userhp', request.session.get('user_email'))
    
    if request.method == 'POST':
       
        if request.POST.get("form_type") == "useremail":
            uemail=request.POST.get('emailid')
            if UserDetail.objects.filter(email=uemail).exists():
                udetail=UserDetail.objects.get(email=uemail)
                name=udetail.name
                otp=random.randint(10000,99999)
                
                # Store OTP and email in session
                request.session['reset_otp'] = str(otp)
                request.session['reset_email'] = uemail
                
                try:
                    send_mail(
                        "Change Password",
                        f"Hi {name}, your otp(one time password) is {otp} for change password. Thank you",
                        "dentalmanagement00@gmail.com",
                        [uemail],
                        fail_silently=True,
                    )
                    messages.warning(request,"OTP sent to your email id successfully")
                except Exception as e:
                    print(f"Email sending failed: {e}")
                    messages.warning(request,f"OTP generated: {otp} (Email service unavailable)")
            else:
                messages.warning(request,"Email does not exist!")
                return redirect("otp")
        elif request.POST.get("form_type") == "changepassword":
            eotp=request.POST.get('enterotp')
            password = request.POST.get('newpassword')
            cpassword =request.POST.get('cnewpassword')
            if eotp == "" or password == "" or cpassword == "":
                    messages.warning(request,"Fill all details !")
                    return redirect('otp')
            
            # Get OTP and email from session
            stored_otp = request.session.get('reset_otp', '')
            stored_email = request.session.get('reset_email', '')
            
            if eotp == stored_otp:
                if password==cpassword:
                    udetail=UserDetail.objects.get(email=stored_email)
                    udetail.password=password
                    udetail.save()
                    
                    # Clear session data
                    request.session.pop('reset_otp', None)
                    request.session.pop('reset_email', None)
                    
                    messages.success(request,"Password changed successfully")
                    return redirect("login")
                else:
                    messages.warning(request,"Password not match")
                    return redirect("otp")
            else:
                messages.warning(request,"Enter correct OTP")
                return redirect("otp")


    
    return render(request,"otp.html")



#-------------------------------------------userhp-------------------------------------------
def userhomepage(request,uemailid):
    # Check if user is logged in via session
    if not request.session.get('user_logged_in'):
        return redirect('home')
    
    return render(request,"userhomepage.html",{'email':uemailid})



# ----------------------------------------appointment page------------------------------------
def appointment(request,uemailid):
    # Check if user is logged in via session
    if not request.session.get('user_logged_in'):
        return redirect('home')
    doctordetail=DoctorDetail.objects.all().order_by('name')
    

    paginator=Paginator(doctordetail, 5)
    pagenumber=request.GET.get('page')
    doctordetailfinal=paginator.get_page(pagenumber)  
    totalpage=doctordetailfinal.paginator.num_pages
    

    if request.method == 'POST':
        
        
        if request.POST.get("form_type") == "search_location":
            dlocation=request.POST.get('dlocation')
            if dlocation!=None :
                doctordetailfinal=DoctorDetail.objects.filter(city__icontains=dlocation)

        elif request.POST.get("form_type") == "search_doctor":
            dname=request.POST.get('dname')
            if dname!=None :
                doctordetailfinal=DoctorDetail.objects.filter(name__icontains=dname)
                
        elif request.POST.get("form_type") == "email_doctor":
            demail=request.POST.get('doctoremail')
            return redirect('bookappointment',demail)
       

        
    doctorinfo={
        
        'email':uemailid,
        # 'doctordetail':doctordetail,
        'lastpage':totalpage,
        
        'doctordetailfinal':doctordetailfinal,
        'totalpagelist':[n+1 for n in range(totalpage)]
        
        
    }
    return render(request,"appointmentpage.html",doctorinfo)

# ---------------------------------------book appointment----------------------------------------------
def bookuserappointment(request,demailid):
    # Check if user is logged in via session
    if not request.session.get('user_logged_in'):
        return redirect('home')
    
    if request.method == 'POST':
        
        
        doctordetail=DoctorDetail.objects.get(email=demailid)
        userdetail=UserDetail.objects.get(email=request.session.get('user_email'))
        
        user_name=userdetail.name
        user_email=userdetail.email
        doctorname=doctordetail.name
        doctoremail=doctordetail.email
        clinicname=doctordetail.clinicname
        city=doctordetail.city
        consultationfee=doctordetail.consultationfee
        apdate = request.POST.get('ad')
        aptime = request.POST.get('select_time')
        payment = request.POST.get('select_payment')
        
        date=str(datetime.today())
        
        
        if apdate!=None and aptime!=None and payment!=None:
            if apdate > date or apdate == date:
                if bookappointment.objects.filter(doctoremail=demailid,appdate=apdate,apptime=aptime).exists():
                    messages.warning(request,"Please change date or time. Doctor is not available")
                    return redirect('bookappointment',demailid)
                
                if bookappointment.objects.filter(appdate=apdate,useremail=user_email).exists():
                    messages.warning(request,"Please change date. You already booked an appointment on selected date.")
                    return redirect('bookappointment',demailid)
                 
                user_appoint = bookappointment(username=user_name, useremail=user_email, doctorname=doctorname, doctoremail=doctoremail,clinicname=clinicname,city=city, appdate=apdate, apptime=aptime, consultationfee=consultationfee, payment=payment)
                user_appoint.save()
                try:
                    send_mail(
                        "Appointment Confirmation",
                        f"Hi {user_name}, Your appointment is confrimed with Dentist {doctorname} on {apdate} at {aptime}. Address of dentist is {clinicname}, {city} and dentist consultation fee is {consultationfee}. Be on time please. Thank you",
                        "dentalmanagement00@gmail.com",
                        [user_email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Email sending failed: {e}")
                messages.success(request,"Appointment booked successfully")
                
                return redirect('appointment',user_email)
            else:
                messages.success(request,"Select valid date!")
                
                return redirect('bookappointment',demailid)
        else:
            messages.success(request,"Select all the fields!")
            
            return redirect('bookappointment',demailid)
    return render(request,"bookappointment.html",{'demail':demailid})


# ----------------------------------emergency appointment page----------------------------------------------
def emergencyappointment(request,uemailid):
    # Check if user is logged in via session
    if not request.session.get('user_logged_in'):
        return redirect('home')
    doctordetail=DoctorDetail.objects.all().order_by('name')
    

    paginator=Paginator(doctordetail, 5)
    pagenumber=request.GET.get('page')
    doctordetailfinal=paginator.get_page(pagenumber)  
    totalpage=doctordetailfinal.paginator.num_pages
    

    if request.method == 'POST':
        
        
        if request.POST.get("form_type") == "search_location":
            dlocation=request.POST.get('dlocation')
            if dlocation!=None :
                doctordetailfinal=DoctorDetail.objects.filter(city__icontains=dlocation)

        elif request.POST.get("form_type") == "search_doctor":
            dname=request.POST.get('dname')
            if dname!=None :
                doctordetailfinal=DoctorDetail.objects.filter(name__icontains=dname)
                
        elif request.POST.get("form_type") == "email_doctor":
            demail=request.POST.get('doctoremail')
            return redirect('bookemergencyappointment',demail)
       

        
    doctorinfo={
        
        'email':uemailid,
        # 'doctordetail':doctordetail,
        'lastpage':totalpage,
        'doctordetailfinal':doctordetailfinal,
        'totalpagelist':[n+1 for n in range(totalpage)]
        
        
    }
    return render(request,"emergencyappointmentpage.html",doctorinfo)

# -------------------------------------book emergency appointment--------------------------------------------------
def bookemergencyappointment(request,demailid):
    # Check if user is logged in via session
    if not request.session.get('user_logged_in'):
        return redirect('home')
    
    date=str(datetime.today())
    todaysdate=date[0:10]
        
    if request.method == 'POST':
        
        
        doctordetail=DoctorDetail.objects.get(email=demailid)
        userdetail=UserDetail.objects.get(email=request.session.get('user_email'))
        
        user_name=userdetail.name
        user_email=userdetail.email
        doctorname=doctordetail.name
        doctoremail=doctordetail.email
        clinicname=doctordetail.clinicname
        city=doctordetail.city
        consultationfee=doctordetail.consultationfee
        consultfee=consultationfee+" + 150"
        aptime = request.POST.get('select_time')
        payment = request.POST.get('select_payment')
        
        
        
        if aptime!=None and payment!=None:
            if bookappointment.objects.filter(doctoremail=demailid,appdate=todaysdate,apptime=aptime).exists():
                appdetail=bookappointment.objects.get(doctoremail=demailid,appdate=todaysdate,apptime=aptime)
                cuser_name=appdetail.username
                cuser_email=appdetail.useremail
                consultationfee=appdetail.consultationfee
                t=aptime[0:2]+":30 "+aptime[6:8]
                upayment=appdetail.payment
                user_appoint = bookappointment(username=cuser_name, useremail=cuser_email, doctorname=doctorname, doctoremail=doctoremail,clinicname=clinicname,city=city, appdate=todaysdate, apptime=t, consultationfee=consultationfee, payment=upayment)
                user_appoint.save()   
                appdetail.delete()
                try:
                    send_mail(
                        "Appointment Confirmation",
                        f"Hi {cuser_name}, Your appointment time with Dentist {doctorname} on {todaysdate} at {aptime} is changed due to emergency!.The new appointment time is {t}. Address of dentist is {clinicname}, {city} and dentist consultation fee is {consultationfee}. Be on time please. Sorry for the inconvenience. Thank you",
                        "dentalmanagement00@gmail.com",
                        [cuser_email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Email sending failed: {e}")
                
            if bookappointment.objects.filter(appdate=todaysdate,useremail=user_email).exists():
                messages.warning(request,"You cannot take an appointment. You already booked an appointment on selected date.")
                return redirect('bookemergencyappointment',demailid)
                
            user_appoint = bookappointment(username=user_name, useremail=user_email, doctorname=doctorname, doctoremail=doctoremail,clinicname=clinicname,city=city, appdate=todaysdate, apptime=aptime, consultationfee=consultfee, payment=payment)
            user_appoint.save()
            try:
                send_mail(
                    "Appointment Confirmation",
                    f"Hi {user_name}, Your appointment is confrimed with Dentist {doctorname} on {todaysdate} at {aptime}. Address of dentist is {clinicname}, {city} and dentist consultation fee is {consultfee}. Be on time please. Thank you.",
                    "dentalmanagement00@gmail.com",
                    [user_email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            messages.success(request,"Appointment booked successfully")
            
            return redirect('userhp',user_email)
            
        else:
            messages.success(request,"Select all the fields!")
            
            return redirect('bookemergencyappointment',demailid)
    return render(request,"bookemergencyappointment.html",{'demail':demailid,'date':todaysdate})



# -----------------------------------user current appointment list----------------------------------------------
def appointmentlist(request, uemailid):
    # Check if user is logged in via session
    if not request.session.get('user_logged_in'):
        return redirect('home')

    # Get today's date in the correct format (without time)
    today = datetime.today().date()
    
    # Filter appointments to show only those after today (future appointments)
    appdetail = bookappointment.objects.filter(useremail=uemailid, appdate__gt=today).order_by('appdate')
    
    # Check if there are any future appointments
    noappointment = not appdetail.exists()

    # Context for rendering the template
    info = {
        'noappointment': noappointment,
        'email': uemailid,
        'appdetail': appdetail,
        'currentdate': today
    }

    # Handle the POST request (for appointment cancellation)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctorname = request.POST.get('doctorname')
        
        # Fetch the specific appointment for cancellation
        appdetail = bookappointment.objects.get(useremail=uemailid, appdate=date, apptime=time, doctorname=doctorname)
        user_name = appdetail.username
        
        # Delete the appointment and send cancellation email
        appdetail.delete()
        try:
            send_mail(
                "Appointment Cancelled",
                f"Hi {user_name}, Your appointment is cancelled with Dentist {doctorname} on {date} at {time} successfully. Thank you.",
                "dentalmanagement00@gmail.com",
                [uemailid],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        # Notify the user and redirect to the updated appointment list
        messages.success(request, "Appointment cancelled successfully!")
        return redirect('applist', uemailid)

    # Render the appointments page with the updated context
    return render(request, "appointmentlist.html", info)



# -----------------------------------------doctor schedule page----------------------------------------------------
def doctorschedule(request,demail):
    # Check if doctor is logged in via session
    if not request.session.get('doctor_logged_in'):
        return redirect('home')
    
    tdate=str(datetime.today())
    todaysdate=tdate[0:10]
    
    userdetail=bookappointment.objects.filter(doctoremail=demail,appdate=todaysdate).order_by('apptime')
    noappointment=True
    if not userdetail:
        noappointment=False
    userinfo={
        'noappointment':noappointment,
        'email':demail,
        'userdetail':userdetail
    }

    if request.method == 'POST':
        if request.POST.get("form_type") == "email_user":
            date = request.POST.get('date')
            time = request.POST.get('time')
            useremail = request.POST.get('useremail')
            doctorname = request.POST.get('doctorname')
            
            appdetail= bookappointment.objects.get(useremail=useremail,appdate=date,apptime=time,doctorname=doctorname)
            user_name=appdetail.username
            appdetail.delete()
            try:
                send_mail(
                    "Appointment Cancelled",
                    f"Hi {user_name}, Your appointment is cancelled with Dentist {doctorname} on {date} at {time} successfully.This appointment is canclled by dentist because you not come for appointment. Thank you.",
                    "dentalmanagement00@gmail.com",
                    [useremail],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            messages.success(request,"Appointment cancelled successfully!")
            return redirect('doctors',demail)
        
        elif request.POST.get("form_type") == "prescription":
            uemail=request.POST.get('useremail')
            
            
            return redirect('prescription',uemail)

    
    return render(request,"doctorschedule.html",userinfo)


# ---------------------------------------------------prescription---------------------------------------------------------
def prescription(request,uemail):
    # Check if doctor is logged in via session
    if not request.session.get('doctor_logged_in'):
        return redirect('home')
    userdetail=UserDetail.objects.get(email=uemail)
    tdate=str(datetime.today())
    todate=tdate[0:4]
    
    dob=userdetail.dateofbirth
    doy=dob[0:4]
    
    age=int(todate) - int(doy)
    userinfo={
        'age':age,
        'email':uemail,
        'userdetail':userdetail
    }
    todaysdate=tdate[0:10]

    if request.method == 'POST':
        prescription=request.POST.get('pres')
        if prescription == "":
            messages.warning(request,"Please write prescription!")
            return redirect('prescription',uemail)
        doctor_email = request.session.get('doctor_email')
        doctordetail=DoctorDetail.objects.get(email=doctor_email)
        userdetail=UserDetail.objects.get(email=uemail)
        appdetail=bookappointment.objects.get(useremail=uemail,doctoremail=doctor_email,appdate=todaysdate)
        user_name=userdetail.name
        user_email=userdetail.email
        doctorname=doctordetail.name
        docemail=doctordetail.email
        
        date=appdetail.appdate
        time=appdetail.apptime
        payment=appdetail.payment
        consultationfee=doctordetail.consultationfee

        user_appoint = appointmenthistory(username=user_name, useremail=user_email, doctorname=doctorname, doctoremail=docemail,appdate=date, apptime=time, consultationfee=consultationfee, payment=payment,prescription=prescription)
        user_appoint.save()
        appdetail= bookappointment.objects.get(useremail=user_email,appdate=date,doctorname=doctorname)
        appdetail.delete()
        messages.success(request,"Appointment completed! ")
        
        return redirect('doctors',doctor_email)

    return render(request,"prescription.html",userinfo)

# -------------------------------------------logout---------------------------------------------------
def userlogout(request):
    # Clear session data
    request.session.flush()  # This removes all session data
    messages.success(request, "Logged out successfully")
    return redirect("home")

# -------------------------------------------user history---------------------------------------------------
def history(request, uemailid):
    # Check if user is logged in via session
    if not request.session.get('user_logged_in'):
        return redirect('home')
    
    # Get appointment history for the user
    history_data = appointmenthistory.objects.filter(useremail=uemailid).order_by('-appdate')
    
    context = {
        'email': uemailid,
        'history_data': history_data,
        'no_history': not history_data.exists()
    }
    
    return render(request, "userhistory.html", context)

# -------------------------------------------user detail---------------------------------------------------
def userdetail(request, uemailid):
    # Check if user is logged in via session
    if not request.session.get('user_logged_in'):
        return redirect('home')
    
    try:
        user_data = UserDetail.objects.get(email=uemailid)
        context = {
            'email': uemailid,
            'user_data': user_data
        }
        return render(request, "userdetail.html", context)
    except UserDetail.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('home')



# ============================================================================
# PHASE 2: ADVANCED FEATURES VIEWS
# ============================================================================

from home.models import (
    DoctorRating, MedicalRecord, MedicalImage, PatientAllergy,
    Payment, AppointmentFeedback, Notification
)
from home.utils import (
    generate_invoice_pdf, send_invoice_email, calculate_doctor_average_rating,
    create_notification, get_unread_notifications_count
)
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg, Q
from datetime import datetime, timedelta
import json


# -------------------------------------------Doctor Rating & Review-------------------------------------------
def rate_doctor(request, doctor_email):
    """Submit rating and review for a doctor"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        doctor = DoctorDetail.objects.get(email=doctor_email)
        user = UserDetail.objects.get(email=user_email)
        
        # Check if user has had an appointment with this doctor
        has_appointment = appointmenthistory.objects.filter(
            useremail=user_email,
            doctoremail=doctor_email
        ).exists()
        
        if request.method == 'POST':
            rating_value = request.POST.get('rating')
            review_text = request.POST.get('review', '')
            
            if not rating_value:
                messages.warning(request, "Please select a rating")
                return redirect('rate_doctor', doctor_email)
            
            # Create or update rating
            rating, created = DoctorRating.objects.update_or_create(
                doctor=doctor,
                patient=user,
                defaults={
                    'rating': int(rating_value),
                    'review': review_text,
                    'is_verified': has_appointment
                }
            )
            
            # Create notification for doctor
            create_notification(
                doctor=doctor,
                title="New Rating Received",
                message=f"{user.name} rated you {rating_value} stars",
                notification_type="system"
            )
            
            messages.success(request, "Thank you for your feedback!")
            return redirect('doctor_profile', doctor_email)
        
        # Get existing rating if any
        existing_rating = DoctorRating.objects.filter(
            doctor=doctor,
            patient=user
        ).first()
        
        context = {
            'doctor': doctor,
            'email': user_email,
            'has_appointment': has_appointment,
            'existing_rating': existing_rating
        }
        
        return render(request, "rate_doctor.html", context)
        
    except DoctorDetail.DoesNotExist:
        messages.error(request, "Doctor not found")
        return redirect('appointment', user_email)
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('appointment', user_email)


# -------------------------------------------Doctor Profile with Ratings-------------------------------------------
def doctor_profile(request, doctor_email):
    """View doctor profile with ratings and reviews"""
    try:
        doctor = DoctorDetail.objects.get(email=doctor_email)
        
        # Get all verified ratings
        ratings = DoctorRating.objects.filter(
            doctor=doctor,
            is_verified=True
        ).order_by('-created_at')
        
        # Calculate statistics
        avg_rating = calculate_doctor_average_rating(doctor)
        total_ratings = ratings.count()
        
        # Rating distribution
        rating_dist = {
            5: ratings.filter(rating=5).count(),
            4: ratings.filter(rating=4).count(),
            3: ratings.filter(rating=3).count(),
            2: ratings.filter(rating=2).count(),
            1: ratings.filter(rating=1).count(),
        }
        
        context = {
            'doctor': doctor,
            'ratings': ratings[:10],  # Show latest 10
            'avg_rating': avg_rating,
            'total_ratings': total_ratings,
            'rating_dist': rating_dist,
            'email': request.session.get('user_email', ''),
            'check': request.session.get('user_logged_in', False)
        }
        
        return render(request, "doctor_profile.html", context)
        
    except DoctorDetail.DoesNotExist:
        messages.error(request, "Doctor not found")
        return redirect('home')


# -------------------------------------------Payment Processing-------------------------------------------
def process_payment(request, appointment_id):
    """Process payment for an appointment"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        appointment = bookappointment.objects.get(id=appointment_id, useremail=user_email)
        doctor = DoctorDetail.objects.get(email=appointment.doctoremail)
        user = UserDetail.objects.get(email=user_email)
        
        if request.method == 'POST':
            payment_method = request.POST.get('payment_method')
            
            if not payment_method:
                messages.warning(request, "Please select a payment method")
                return redirect('process_payment', appointment_id)
            
            # Create payment record
            payment = Payment.objects.create(
                appointment=appointment,
                patient=user,
                doctor=doctor,
                amount=float(appointment.consultationfee.replace('₹', '').replace('+', '').strip()),
                payment_method=payment_method,
                payment_status='completed'
            )
            
            # Generate and send invoice
            try:
                send_invoice_email(payment)
            except Exception as e:
                logger.error(f"Failed to send invoice: {str(e)}")
            
            # Create notification
            create_notification(
                user=user,
                title="Payment Successful",
                message=f"Payment of ₹{payment.amount} completed successfully",
                notification_type="payment"
            )
            
            messages.success(request, "Payment successful! Invoice sent to your email.")
            return redirect('payment_success', payment.id)
        
        context = {
            'appointment': appointment,
            'doctor': doctor,
            'email': user_email
        }
        
        return render(request, "payment.html", context)
        
    except bookappointment.DoesNotExist:
        messages.error(request, "Appointment not found")
        return redirect('applist', user_email)
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('applist', user_email)


# -------------------------------------------Payment Success-------------------------------------------
def payment_success(request, payment_id):
    """Payment success page with invoice download"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        payment = Payment.objects.get(id=payment_id, patient__email=user_email)
        
        context = {
            'payment': payment,
            'email': user_email
        }
        
        return render(request, "payment_success.html", context)
        
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found")
        return redirect('userhp', user_email)


# -------------------------------------------Download Invoice-------------------------------------------
def download_invoice(request, payment_id):
    """Download PDF invoice"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        payment = Payment.objects.get(id=payment_id, patient__email=user_email)
        
        # Generate PDF
        pdf_buffer = generate_invoice_pdf(payment)
        
        # Create response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{payment.invoice_number}.pdf"'
        
        return response
        
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found")
        return redirect('userhp', user_email)
    except Exception as e:
        messages.error(request, f"Error generating invoice: {str(e)}")
        return redirect('userhp', user_email)


# -------------------------------------------Payment History-------------------------------------------
def payment_history(request, user_email):
    """View all payment history"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    try:
        user = UserDetail.objects.get(email=user_email)
        payments = Payment.objects.filter(patient=user).order_by('-payment_date')
        
        context = {
            'payments': payments,
            'email': user_email
        }
        
        return render(request, "payment_history.html", context)
        
    except UserDetail.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('home')


# -------------------------------------------Medical Records-------------------------------------------
def medical_records(request, user_email):
    """View patient medical records"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    try:
        user = UserDetail.objects.get(email=user_email)
        records = MedicalRecord.objects.filter(patient=user).order_by('-created_at')
        allergies = PatientAllergy.objects.filter(patient=user)
        
        context = {
            'records': records,
            'allergies': allergies,
            'email': user_email
        }
        
        return render(request, "medical_records.html", context)
        
    except UserDetail.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('home')


# -------------------------------------------Add Medical Record (Doctor)-------------------------------------------
def add_medical_record(request, patient_email):
    """Doctor adds medical record for patient"""
    if not request.session.get('doctor_logged_in'):
        return redirect('fordoctor')
    
    doctor_email = request.session.get('doctor_email')
    
    try:
        patient = UserDetail.objects.get(email=patient_email)
        doctor = DoctorDetail.objects.get(email=doctor_email)
        
        if request.method == 'POST':
            diagnosis = request.POST.get('diagnosis')
            treatment = request.POST.get('treatment')
            medications = request.POST.get('medications', '')
            notes = request.POST.get('notes', '')
            teeth_treated = request.POST.get('teeth_treated', '')
            procedure_type = request.POST.get('procedure_type', '')
            follow_up = request.POST.get('follow_up') == 'on'
            follow_up_date = request.POST.get('follow_up_date', None)
            
            if not diagnosis or not treatment:
                messages.warning(request, "Diagnosis and treatment are required")
                return redirect('add_medical_record', patient_email)
            
            # Create medical record
            record = MedicalRecord.objects.create(
                patient=patient,
                doctor=doctor,
                diagnosis=diagnosis,
                treatment_provided=treatment,
                medications=medications,
                notes=notes,
                teeth_treated=teeth_treated,
                procedure_type=procedure_type,
                follow_up_required=follow_up,
                follow_up_date=follow_up_date if follow_up_date else None
            )
            
            # Handle image uploads
            images = request.FILES.getlist('medical_images')
            for image in images:
                MedicalImage.objects.create(
                    medical_record=record,
                    image=image,
                    image_type=request.POST.get('image_type', 'photo')
                )
            
            # Create notification
            create_notification(
                user=patient,
                title="New Medical Record",
                message=f"Dr. {doctor.name} added a new medical record",
                notification_type="system"
            )
            
            messages.success(request, "Medical record added successfully")
            return redirect('doctors', doctor_email)
        
        context = {
            'patient': patient,
            'email': doctor_email
        }
        
        return render(request, "add_medical_record.html", context)
        
    except (UserDetail.DoesNotExist, DoctorDetail.DoesNotExist):
        messages.error(request, "User not found")
        return redirect('doctors', doctor_email)


# -------------------------------------------Notifications-------------------------------------------
def notifications(request):
    """View all notifications"""
    if request.session.get('user_logged_in'):
        user_email = request.session.get('user_email')
        user = UserDetail.objects.get(email=user_email)
        notifs = Notification.objects.filter(user=user).order_by('-created_at')
        recipient_type = 'user'
    elif request.session.get('doctor_logged_in'):
        doctor_email = request.session.get('doctor_email')
        doctor = DoctorDetail.objects.get(email=doctor_email)
        notifs = Notification.objects.filter(doctor=doctor).order_by('-created_at')
        recipient_type = 'doctor'
    else:
        return redirect('login')
    
    context = {
        'notifications': notifs,
        'email': user_email if recipient_type == 'user' else doctor_email,
        'recipient_type': recipient_type
    }
    
    return render(request, "notifications.html", context)


# -------------------------------------------Mark Notification as Read-------------------------------------------
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'error'})


# -------------------------------------------Patient Dashboard-------------------------------------------
def patient_dashboard(request, user_email):
    """Patient dashboard with statistics"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    try:
        user = UserDetail.objects.get(email=user_email)
        
        # Get statistics
        total_appointments = appointmenthistory.objects.filter(useremail=user_email).count()
        upcoming_appointments = bookappointment.objects.filter(useremail=user_email).count()
        total_payments = Payment.objects.filter(patient=user).count()
        total_spent = Payment.objects.filter(patient=user, payment_status='completed').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        # Recent appointments
        recent_appointments = appointmenthistory.objects.filter(
            useremail=user_email
        ).order_by('-appdate')[:5]
        
        # Upcoming appointments
        upcoming = bookappointment.objects.filter(
            useremail=user_email
        ).order_by('appdate')[:5]
        
        # Recent payments
        recent_payments = Payment.objects.filter(
            patient=user
        ).order_by('-payment_date')[:5]
        
        # Unread notifications
        unread_count = get_unread_notifications_count(user=user)
        
        context = {
            'user': user,
            'email': user_email,
            'total_appointments': total_appointments,
            'upcoming_appointments': upcoming_appointments,
            'total_payments': total_payments,
            'total_spent': total_spent,
            'recent_appointments': recent_appointments,
            'upcoming': upcoming,
            'recent_payments': recent_payments,
            'unread_notifications': unread_count
        }
        
        return render(request, "patient_dashboard.html", context)
        
    except UserDetail.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('home')


# -------------------------------------------Doctor Dashboard-------------------------------------------
def doctor_dashboard(request, doctor_email):
    """Doctor dashboard with statistics"""
    if not request.session.get('doctor_logged_in'):
        return redirect('fordoctor')
    
    try:
        doctor = DoctorDetail.objects.get(email=doctor_email)
        
        # Get today's date
        today = datetime.today().strftime('%Y-%m-%d')
        
        # Get statistics
        today_appointments = bookappointment.objects.filter(
            doctoremail=doctor_email,
            appdate=today
        ).count()
        
        total_patients = appointmenthistory.objects.filter(
            doctoremail=doctor_email
        ).values('useremail').distinct().count()
        
        total_revenue = Payment.objects.filter(
            doctor=doctor,
            payment_status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        avg_rating = calculate_doctor_average_rating(doctor)
        total_ratings = DoctorRating.objects.filter(doctor=doctor, is_verified=True).count()
        
        # Today's schedule
        today_schedule = bookappointment.objects.filter(
            doctoremail=doctor_email,
            appdate=today
        ).order_by('apptime')
        
        # Recent reviews
        recent_reviews = DoctorRating.objects.filter(
            doctor=doctor,
            is_verified=True
        ).order_by('-created_at')[:5]
        
        # Unread notifications
        unread_count = get_unread_notifications_count(doctor=doctor)
        
        context = {
            'doctor': doctor,
            'email': doctor_email,
            'today_appointments': today_appointments,
            'total_patients': total_patients,
            'total_revenue': total_revenue,
            'avg_rating': avg_rating,
            'total_ratings': total_ratings,
            'today_schedule': today_schedule,
            'recent_reviews': recent_reviews,
            'unread_notifications': unread_count
        }
        
        return render(request, "doctor_dashboard.html", context)
        
    except DoctorDetail.DoesNotExist:
        messages.error(request, "Doctor not found")
        return redirect('fordoctor')
