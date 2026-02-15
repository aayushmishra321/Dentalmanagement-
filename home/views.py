
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
from django.contrib.auth.hashers import make_password, check_password
import random
import logging
import os
import json

logger = logging.getLogger(__name__)

# Stripe import with fallback
try:
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    logger.warning("Stripe not installed. Payment gateway features will be limited.")
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
                    
                    # Check if password is hashed (starts with pbkdf2_sha256$)
                    if doctor.password.startswith('pbkdf2_sha256$'):
                        # Use hashed password check
                        if check_password(dpassword, doctor.password):
                            # Set session variables for doctor login
                            request.session['doctor_logged_in'] = True
                            request.session['doctor_email'] = demail
                            
                            messages.success(request, "Login successful")
                            return redirect("doctors", demail)
                        else:
                            messages.warning(request, "Password is incorrect!")
                            return redirect("fordoctor")
                    else:
                        # Legacy plain text password - check and upgrade
                        if doctor.password == dpassword:
                            # Upgrade to hashed password
                            doctor.password = make_password(dpassword)
                            doctor.save()
                            
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
                
                # Check if password is hashed (starts with pbkdf2_sha256$)
                if user.password.startswith('pbkdf2_sha256$'):
                    # Use hashed password check
                    if check_password(password, user.password):
                        # Set session variables instead of global variables
                        request.session['user_logged_in'] = True
                        request.session['user_email'] = email
                        
                        messages.success(request, "Login successful")
                        return redirect("userhp", email)
                    else:
                        messages.warning(request, "Password incorrect!")
                        return redirect("login")
                else:
                    # Legacy plain text password - check and upgrade
                    if user.password == password:
                        # Upgrade to hashed password
                        user.password = make_password(password)
                        user.save()
                        
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
                    # Create user with hashed password
                    user_detail = UserDetail(
                        name=name, 
                        email=email, 
                        contact=contact, 
                        dateofbirth=dateofbirth, 
                        gender=gender, 
                        address=address, 
                        pincode=pincode, 
                        password=make_password(password)  # Hash the password
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
                    udetail.password=make_password(password)  # Hash the password
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
        
        # Get today's date in YYYY-MM-DD format for comparison
        today = datetime.today().strftime('%Y-%m-%d')
        
        
        if apdate!=None and aptime!=None and payment!=None:
            # Allow booking for today and future dates
            if apdate >= today:
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
                messages.warning(request,"Cannot book appointments for past dates!")
                
                return redirect('bookappointment',demailid)
        else:
            messages.warning(request,"Please select all the fields!")
            
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
    
    # Filter appointments to show today and future appointments
    appdetail = bookappointment.objects.filter(useremail=uemailid, appdate__gte=str(today)).order_by('appdate')
    
    # Check if there are any appointments
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
        
        # Rating distribution - pass as list of tuples for easy template iteration
        count_5 = ratings.filter(rating=5).count()
        count_4 = ratings.filter(rating=4).count()
        count_3 = ratings.filter(rating=3).count()
        count_2 = ratings.filter(rating=2).count()
        count_1 = ratings.filter(rating=1).count()
        
        rating_dist = [
            {'stars': 5, 'count': count_5},
            {'stars': 4, 'count': count_4},
            {'stars': 3, 'count': count_3},
            {'stars': 2, 'count': count_2},
            {'stars': 1, 'count': count_1},
        ]
        
        # Round avg_rating for star display
        avg_rating_rounded = round(avg_rating)
        
        context = {
            'doctor': doctor,
            'ratings': ratings[:10],  # Show latest 10
            'avg_rating': avg_rating_rounded,
            'avg_rating_exact': avg_rating,  # For display
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
    """Process payment for an appointment with Stripe integration"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        appointment = bookappointment.objects.get(id=appointment_id, useremail=user_email)
        doctor = DoctorDetail.objects.get(email=appointment.doctoremail)
        user = UserDetail.objects.get(email=user_email)
        
        # Calculate amount in paise (Stripe requires smallest currency unit)
        amount_str = appointment.consultationfee.replace('₹', '').replace('+', '').strip()
        amount = float(amount_str)
        amount_paise = int(amount * 100)  # Convert to paise for Stripe
        
        if request.method == 'POST':
            payment_method = request.POST.get('payment_method')
            
            if not payment_method:
                messages.warning(request, "Please select a payment method")
                return redirect('process_payment', appointment_id)
            
            # Handle Stripe payment for card/online methods
            if payment_method in ['card', 'online'] and STRIPE_AVAILABLE:
                try:
                    # Create Stripe Payment Intent
                    intent = stripe.PaymentIntent.create(
                        amount=amount_paise,
                        currency=settings.STRIPE_CURRENCY,
                        description=f"Consultation with Dr. {doctor.name}",
                        metadata={
                            'appointment_id': appointment_id,
                            'patient_email': user_email,
                            'doctor_email': doctor.email,
                        }
                    )
                    
                    # Create payment record with Stripe details
                    payment = Payment.objects.create(
                        appointment=appointment,
                        patient=user,
                        doctor=doctor,
                        amount=amount,
                        payment_method=payment_method,
                        payment_status='completed',
                        stripe_payment_intent_id=intent.id,
                        transaction_id=intent.id
                    )
                    
                    logger.info(f"Stripe payment created: {intent.id} for appointment {appointment_id}")
                    
                except stripe.error.StripeError as e:
                    logger.error(f"Stripe error: {str(e)}")
                    messages.error(request, f"Payment failed: {str(e)}")
                    return redirect('process_payment', appointment_id)
            else:
                # Handle non-Stripe payment methods (cash, UPI, etc.)
                payment = Payment.objects.create(
                    appointment=appointment,
                    patient=user,
                    doctor=doctor,
                    amount=amount,
                    payment_method=payment_method,
                    payment_status='completed' if payment_method == 'cash' else 'pending'
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
        
        # GET request - show payment form
        context = {
            'appointment': appointment,
            'doctor': doctor,
            'email': user_email,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY if STRIPE_AVAILABLE else '',
            'stripe_available': STRIPE_AVAILABLE,
            'amount_paise': amount_paise,
        }
        
        return render(request, "payment.html", context)
        
    except bookappointment.DoesNotExist:
        messages.error(request, "Appointment not found")
        return redirect('applist', user_email)
    except Exception as e:
        logger.error(f"Payment error: {str(e)}")
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



# ============================================================================
# PHASE 3: ADVANCED APPOINTMENT MANAGEMENT
# ============================================================================

from home.models import (
    RecurringAppointment, AppointmentReschedule, AppointmentWaitlist,
    AppointmentNoShow, TreatmentPlan, TreatmentSession
)


# -------------------------------------------Recurring Appointments-------------------------------------------
def create_recurring_appointment(request, doctor_email):
    """Create recurring appointment"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        doctor = DoctorDetail.objects.get(email=doctor_email)
        user = UserDetail.objects.get(email=user_email)
        
        if request.method == 'POST':
            frequency = request.POST.get('frequency')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date', None)
            time = request.POST.get('time')
            
            if not all([frequency, start_date, time]):
                messages.warning(request, "Please fill all required fields")
                return redirect('create_recurring_appointment', doctor_email)
            
            # Create recurring appointment
            recurring = RecurringAppointment.objects.create(
                patient=user,
                doctor=doctor,
                frequency=frequency,
                start_date=start_date,
                end_date=end_date if end_date else None,
                time=time,
                is_active=True
            )
            
            # Create notification
            create_notification(
                user=user,
                title="Recurring Appointment Created",
                message=f"Recurring {frequency} appointment with Dr. {doctor.name} created",
                notification_type="appointment"
            )
            
            messages.success(request, "Recurring appointment created successfully")
            return redirect('patient_dashboard', user_email)
        
        context = {
            'doctor': doctor,
            'email': user_email
        }
        
        return render(request, "create_recurring_appointment.html", context)
        
    except (DoctorDetail.DoesNotExist, UserDetail.DoesNotExist):
        messages.error(request, "User not found")
        return redirect('appointment', user_email)


# -------------------------------------------Reschedule Appointment-------------------------------------------
def reschedule_appointment(request, appointment_id):
    """Reschedule an existing appointment"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        appointment = bookappointment.objects.get(id=appointment_id, useremail=user_email)
        
        if request.method == 'POST':
            new_date = request.POST.get('new_date')
            new_time = request.POST.get('new_time')
            reason = request.POST.get('reason', '')
            
            if not all([new_date, new_time]):
                messages.warning(request, "Please select new date and time")
                return redirect('reschedule_appointment', appointment_id)
            
            # Create reschedule record
            AppointmentReschedule.objects.create(
                appointment=appointment,
                old_date=appointment.appdate,
                old_time=appointment.apptime,
                new_date=new_date,
                new_time=new_time,
                reason=reason,
                rescheduled_by='patient'
            )
            
            # Update appointment
            appointment.appdate = new_date
            appointment.apptime = new_time
            appointment.save()
            
            # Send email notification
            try:
                send_mail(
                    "Appointment Rescheduled",
                    f"Hi {appointment.username}, Your appointment with Dr. {appointment.doctorname} has been rescheduled to {new_date} at {new_time}. Thank you.",
                    "dentalmanagement00@gmail.com",
                    [user_email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Email sending failed: {e}")
            
            messages.success(request, "Appointment rescheduled successfully")
            return redirect('applist', user_email)
        
        context = {
            'appointment': appointment,
            'email': user_email
        }
        
        return render(request, "reschedule_appointment.html", context)
        
    except bookappointment.DoesNotExist:
        messages.error(request, "Appointment not found")
        return redirect('applist', user_email)


# -------------------------------------------Waitlist Management-------------------------------------------
def join_waitlist(request, doctor_email):
    """Join waitlist for a doctor"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        doctor = DoctorDetail.objects.get(email=doctor_email)
        user = UserDetail.objects.get(email=user_email)
        
        if request.method == 'POST':
            preferred_date = request.POST.get('preferred_date')
            preferred_time = request.POST.get('preferred_time', '')
            notes = request.POST.get('notes', '')
            
            if not preferred_date:
                messages.warning(request, "Please select preferred date")
                return redirect('join_waitlist', doctor_email)
            
            # Check if already in waitlist
            if AppointmentWaitlist.objects.filter(
                patient=user,
                doctor=doctor,
                preferred_date=preferred_date,
                is_active=True
            ).exists():
                messages.warning(request, "You are already in the waitlist for this date")
                return redirect('join_waitlist', doctor_email)
            
            # Add to waitlist
            AppointmentWaitlist.objects.create(
                patient=user,
                doctor=doctor,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                notes=notes,
                is_active=True
            )
            
            messages.success(request, "Added to waitlist successfully. We'll notify you when a slot opens.")
            return redirect('patient_dashboard', user_email)
        
        context = {
            'doctor': doctor,
            'email': user_email
        }
        
        return render(request, "join_waitlist.html", context)
        
    except (DoctorDetail.DoesNotExist, UserDetail.DoesNotExist):
        messages.error(request, "User not found")
        return redirect('appointment', user_email)


# -------------------------------------------Treatment Plans-------------------------------------------
def create_treatment_plan(request, patient_email):
    """Doctor creates treatment plan for patient"""
    if not request.session.get('doctor_logged_in'):
        return redirect('fordoctor')
    
    doctor_email = request.session.get('doctor_email')
    
    try:
        patient = UserDetail.objects.get(email=patient_email)
        doctor = DoctorDetail.objects.get(email=doctor_email)
        
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            total_sessions = request.POST.get('total_sessions')
            start_date = request.POST.get('start_date')
            estimated_end_date = request.POST.get('estimated_end_date')
            total_cost = request.POST.get('total_cost')
            
            if not all([title, description, total_sessions, start_date, estimated_end_date, total_cost]):
                messages.warning(request, "Please fill all required fields")
                return redirect('create_treatment_plan', patient_email)
            
            # Create treatment plan
            plan = TreatmentPlan.objects.create(
                patient=patient,
                doctor=doctor,
                title=title,
                description=description,
                total_sessions=int(total_sessions),
                start_date=start_date,
                estimated_end_date=estimated_end_date,
                total_cost=float(total_cost),
                is_active=True
            )
            
            # Create sessions
            for i in range(1, int(total_sessions) + 1):
                TreatmentSession.objects.create(
                    treatment_plan=plan,
                    session_number=i,
                    status='pending'
                )
            
            # Create notification
            create_notification(
                user=patient,
                title="New Treatment Plan",
                message=f"Dr. {doctor.name} created a treatment plan: {title}",
                notification_type="system"
            )
            
            messages.success(request, "Treatment plan created successfully")
            return redirect('doctor_dashboard', doctor_email)
        
        context = {
            'patient': patient,
            'email': doctor_email
        }
        
        return render(request, "create_treatment_plan.html", context)
        
    except (UserDetail.DoesNotExist, DoctorDetail.DoesNotExist):
        messages.error(request, "User not found")
        return redirect('doctors', doctor_email)


# -------------------------------------------View Treatment Plans-------------------------------------------
def view_treatment_plans(request, user_email):
    """View patient treatment plans"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    try:
        user = UserDetail.objects.get(email=user_email)
        plans = TreatmentPlan.objects.filter(patient=user).order_by('-created_at')
        
        context = {
            'plans': plans,
            'email': user_email
        }
        
        return render(request, "view_treatment_plans.html", context)
        
    except UserDetail.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('home')


# -------------------------------------------Treatment Plan Details-------------------------------------------
def treatment_plan_details(request, plan_id):
    """View treatment plan details with sessions"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    
    try:
        plan = TreatmentPlan.objects.get(id=plan_id, patient__email=user_email)
        sessions = TreatmentSession.objects.filter(treatment_plan=plan).order_by('session_number')
        
        # Calculate progress
        progress_percentage = (plan.completed_sessions / plan.total_sessions * 100) if plan.total_sessions > 0 else 0
        
        context = {
            'plan': plan,
            'sessions': sessions,
            'progress_percentage': progress_percentage,
            'email': user_email
        }
        
        return render(request, "treatment_plan_details.html", context)
        
    except TreatmentPlan.DoesNotExist:
        messages.error(request, "Treatment plan not found")
        return redirect('patient_dashboard', user_email)


# -------------------------------------------Mark No-Show-------------------------------------------
def mark_no_show(request, appointment_id):
    """Doctor marks patient as no-show"""
    if not request.session.get('doctor_logged_in'):
        return redirect('fordoctor')
    
    doctor_email = request.session.get('doctor_email')
    
    try:
        appointment = bookappointment.objects.get(id=appointment_id, doctoremail=doctor_email)
        doctor = DoctorDetail.objects.get(email=doctor_email)
        patient = UserDetail.objects.get(email=appointment.useremail)
        
        if request.method == 'POST':
            notes = request.POST.get('notes', '')
            
            # Create no-show record
            AppointmentNoShow.objects.create(
                appointment=appointment,
                patient=patient,
                doctor=doctor,
                appointment_date=appointment.appdate,
                appointment_time=appointment.apptime,
                notes=notes
            )
            
            # Delete appointment
            appointment.delete()
            
            # Send notification
            create_notification(
                user=patient,
                title="Missed Appointment",
                message=f"You missed your appointment with Dr. {doctor.name} on {appointment.appdate}",
                notification_type="appointment"
            )
            
            messages.success(request, "Appointment marked as no-show")
            return redirect('doctors', doctor_email)
        
        context = {
            'appointment': appointment,
            'email': doctor_email
        }
        
        return render(request, "mark_no_show.html", context)
        
    except (bookappointment.DoesNotExist, DoctorDetail.DoesNotExist, UserDetail.DoesNotExist):
        messages.error(request, "Appointment not found")
        return redirect('doctors', doctor_email)



# ============================================================================
# PHASE 4: TWO-FACTOR AUTHENTICATION VIEWS
# ============================================================================

from home.security import create_2fa_otp, verify_2fa_otp, enable_2fa, disable_2fa, is_2fa_enabled


def enable_2fa_view(request):
    """Enable 2FA for user"""
    if not request.session.get('user_logged_in') and not request.session.get('doctor_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email') or request.session.get('doctor_email')
    user_type = 'patient' if request.session.get('user_logged_in') else 'doctor'
    
    if request.method == 'POST':
        try:
            if user_type == 'patient':
                user = UserDetail.objects.get(email=user_email)
                enable_2fa(user=user)
                messages.success(request, "2FA enabled successfully")
            else:
                doctor = DoctorDetail.objects.get(email=user_email)
                enable_2fa(doctor=doctor)
                messages.success(request, "2FA enabled successfully")
            
            return redirect('patient_dashboard' if user_type == 'patient' else 'doctor_dashboard', user_email)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    context = {
        'email': user_email,
        'user_type': user_type,
        '2fa_enabled': is_2fa_enabled(
            user=UserDetail.objects.get(email=user_email) if user_type == 'patient' else None,
            doctor=DoctorDetail.objects.get(email=user_email) if user_type == 'doctor' else None
        )
    }
    
    return render(request, "enable_2fa.html", context)


def disable_2fa_view(request):
    """Disable 2FA for user"""
    if not request.session.get('user_logged_in') and not request.session.get('doctor_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email') or request.session.get('doctor_email')
    user_type = 'patient' if request.session.get('user_logged_in') else 'doctor'
    
    if request.method == 'POST':
        try:
            if user_type == 'patient':
                user = UserDetail.objects.get(email=user_email)
                disable_2fa(user=user)
                messages.success(request, "2FA disabled successfully")
            else:
                doctor = DoctorDetail.objects.get(email=user_email)
                disable_2fa(doctor=doctor)
                messages.success(request, "2FA disabled successfully")
            
            return redirect('patient_dashboard' if user_type == 'patient' else 'doctor_dashboard', user_email)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    return redirect('enable_2fa_view')


def request_2fa_otp(request):
    """Request 2FA OTP"""
    if request.method == 'POST':
        email = request.POST.get('email')
        user_type = request.POST.get('user_type', 'patient')
        
        try:
            if user_type == 'patient':
                user = UserDetail.objects.get(email=email)
                create_2fa_otp(user=user)
            else:
                doctor = DoctorDetail.objects.get(email=email)
                create_2fa_otp(doctor=doctor)
            
            request.session['2fa_email'] = email
            request.session['2fa_user_type'] = user_type
            messages.success(request, "OTP sent to your email")
            return redirect('verify_2fa_view')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('login')
    
    return redirect('login')


def verify_2fa_view(request):
    """Verify 2FA OTP"""
    email = request.session.get('2fa_email')
    user_type = request.session.get('2fa_user_type', 'patient')
    
    if not email:
        return redirect('login')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        
        try:
            if user_type == 'patient':
                user = UserDetail.objects.get(email=email)
                if verify_2fa_otp(otp_code, user=user):
                    request.session['2fa_verified'] = True
                    request.session['user_logged_in'] = True
                    request.session['user_email'] = email
                    messages.success(request, "2FA verified successfully")
                    return redirect('userhp', email)
            else:
                doctor = DoctorDetail.objects.get(email=email)
                if verify_2fa_otp(otp_code, doctor=doctor):
                    request.session['2fa_verified'] = True
                    request.session['doctor_logged_in'] = True
                    request.session['doctor_email'] = email
                    messages.success(request, "2FA verified successfully")
                    return redirect('doctors', email)
            
            messages.error(request, "Invalid or expired OTP")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    context = {
        'email': email,
        'user_type': user_type
    }
    
    return render(request, "verify_2fa.html", context)


# ============================================================================
# PHASE 4: ADVANCED SEARCH VIEWS
# ============================================================================

def advanced_search(request):
    """Advanced search across all resources"""
    if not request.session.get('user_logged_in'):
        return redirect('login')
    
    user_email = request.session.get('user_email')
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'doctors')
    
    results = {}
    
    if search_type == 'doctors':
        # Search doctors
        doctors = DoctorDetail.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(clinicname__icontains=query) |
            Q(experience__icontains=query)
        )
        
        # Apply filters
        city = request.GET.get('city')
        min_fee = request.GET.get('min_fee')
        max_fee = request.GET.get('max_fee')
        
        if city:
            doctors = doctors.filter(city__icontains=city)
        if min_fee:
            doctors = doctors.filter(consultationfee__gte=min_fee)
        if max_fee:
            doctors = doctors.filter(consultationfee__lte=max_fee)
        
        results['doctors'] = doctors
    
    elif search_type == 'appointments':
        # Search appointments
        appointments = bookappointment.objects.filter(
            useremail=user_email
        ).filter(
            Q(doctorname__icontains=query) |
            Q(clinicname__icontains=query) |
            Q(city__icontains=query)
        )
        results['appointments'] = appointments
    
    elif search_type == 'medical_records':
        # Search medical records
        records = MedicalRecord.objects.filter(
            patient__email=user_email
        ).filter(
            Q(diagnosis__icontains=query) |
            Q(treatment_provided__icontains=query) |
            Q(doctor__name__icontains=query)
        )
        results['medical_records'] = records
    
    context = {
        'email': user_email,
        'query': query,
        'search_type': search_type,
        'results': results
    }
    
    return render(request, "advanced_search.html", context)



# ============================================================================
# PHASE 5: ADVANCED FEATURES & OPTIMIZATION
# ============================================================================

from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from home.reports import generate_report, generate_daily_appointments_report, generate_monthly_revenue_report, generate_patient_statistics_report, generate_doctor_performance_report
from home.models import Report, ReportSchedule, AnalyticsCache
import json
from datetime import datetime, timedelta
import csv
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ============================================================================
# REPORT GENERATION VIEWS
# ============================================================================

def generate_report_view(request):
    """Generate and download reports"""
    if not request.session.get('user_logged_in'):
        messages.error(request, "Please login first")
        return redirect('login')
    
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        file_format = request.POST.get('file_format', 'pdf')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            # Convert dates if provided
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Generate report
            file_path, report_data = generate_report(report_type, file_format, start_date, end_date)
            
            # Create Report record
            Report.objects.create(
                report_type=report_type,
                title=f"{report_type.replace('_', ' ').title()} Report",
                file_format=file_format,
                file_path=file_path,
                status='completed'
            )
            
            # Serve file for download
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
                
        except Exception as e:
            messages.error(request, f"Report generation failed: {str(e)}")
            return redirect('analytics_dashboard')
    
    return render(request, 'generate_report.html', {
        'check': request.session.get('user_logged_in', False),
        'uemail': request.session.get('user_email', '')
    })


def view_reports(request):
    """View all generated reports"""
    if not request.session.get('user_logged_in'):
        messages.error(request, "Please login first")
        return redirect('login')
    
    reports = Report.objects.all().order_by('-generated_at')[:50]
    
    return render(request, 'view_reports.html', {
        'reports': reports,
        'check': request.session.get('user_logged_in', False),
        'uemail': request.session.get('user_email', '')
    })


# ============================================================================
# ANALYTICS DASHBOARD
# ============================================================================

def analytics_dashboard(request):
    """Main analytics dashboard with charts and statistics"""
    if not request.session.get('user_logged_in'):
        messages.error(request, "Please login first")
        return redirect('login')
    
    try:
        user_email = request.session.get('user_email', '')
        
        # Get analytics data
        total_patients = UserDetail.objects.count()
        total_doctors = DoctorDetail.objects.count()
        total_appointments = bookappointment.objects.count()
        
        # Revenue data
        from home.models import Payment
        total_revenue = Payment.objects.filter(payment_status='completed').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        # Recent appointments (last 30 days)
        from datetime import timedelta
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        recent_appointments = bookappointment.objects.filter(
            appdate__gte=thirty_days_ago
        ).count()
        
        # Monthly revenue trend (last 6 months)
        monthly_revenue = []
        for i in range(6):
            month_date = datetime.now() - timedelta(days=30*i)
            month_revenue = Payment.objects.filter(
                payment_status='completed',
                payment_date__year=month_date.year,
                payment_date__month=month_date.month
            ).aggregate(total=models.Sum('amount'))['total'] or 0
            monthly_revenue.append({
                'month': month_date.strftime('%B %Y'),
                'revenue': float(month_revenue)
            })
        monthly_revenue.reverse()
        
        # Top doctors by appointments
        from django.db.models import Count
        top_doctors = appointmenthistory.objects.values('doctorname').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Patient demographics
        gender_distribution = UserDetail.objects.values('gender').annotate(
            count=Count('email')
        )
        
        context = {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_appointments': total_appointments,
            'total_revenue': total_revenue,
            'recent_appointments': recent_appointments,
            'monthly_revenue': json.dumps(monthly_revenue),
            'top_doctors': list(top_doctors),
            'gender_distribution': list(gender_distribution),
            'check': request.session.get('user_logged_in', False),
            'uemail': user_email,
            'email': user_email
        }
        
        return render(request, 'analytics_dashboard.html', context)
        
    except Exception as e:
        logger.error(f"Analytics dashboard error: {str(e)}")
        messages.error(request, f"Failed to load analytics: {str(e)}")
        # Redirect back to appropriate page based on user type
        user_email = request.session.get('user_email', '')
        if user_email:
            # Check if doctor
            try:
                DoctorDetail.objects.get(email=user_email)
                return redirect('doctors', user_email)
            except DoctorDetail.DoesNotExist:
                return redirect('userhp', user_email)
        return redirect('home')


# ============================================================================
# DATA EXPORT VIEWS
# ============================================================================

def export_appointments_csv(request):
    """Export appointments to CSV"""
    if not request.session.get('user_logged_in'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Patient', 'Email', 'Doctor', 'Date', 'Time', 'Clinic', 'Fee', 'Payment'])
    
    appointments = bookappointment.objects.all()
    for apt in appointments:
        writer.writerow([
            apt.username,
            apt.useremail,
            apt.doctorname,
            apt.appdate,
            apt.apptime,
            apt.clinicname,
            apt.consultationfee,
            apt.payment
        ])
    
    return response


def export_payments_csv(request):
    """Export payments to CSV"""
    if not request.session.get('user_logged_in'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    from home.models import Payment
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Invoice', 'Patient', 'Doctor', 'Amount', 'Method', 'Status', 'Date'])
    
    payments = Payment.objects.all()
    for payment in payments:
        writer.writerow([
            payment.invoice_number,
            payment.patient.name if payment.patient else 'N/A',
            payment.doctor.name if payment.doctor else 'N/A',
            payment.amount,
            payment.payment_method,
            payment.payment_status,
            payment.payment_date.strftime('%Y-%m-%d')
        ])
    
    return response


def export_medical_records_csv(request):
    """Export medical records to CSV"""
    if not request.session.get('user_logged_in'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    from home.models import MedicalRecord
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="medical_records.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Patient', 'Doctor', 'Diagnosis', 'Treatment', 'Procedure', 'Date'])
    
    records = MedicalRecord.objects.all()
    for record in records:
        writer.writerow([
            record.patient.name if record.patient else 'N/A',
            record.doctor.name if record.doctor else 'N/A',
            record.diagnosis,
            record.treatment,
            record.procedure_type,
            record.created_at.strftime('%Y-%m-%d')
        ])
    
    return response


def export_data_view(request):
    """Data export page"""
    if not request.session.get('user_logged_in'):
        messages.error(request, "Please login first")
        return redirect('login')
    
    return render(request, 'export_data.html', {
        'check': request.session.get('user_logged_in', False),
        'uemail': request.session.get('user_email', '')
    })


# ============================================================================
# ANALYTICS API ENDPOINTS
# ============================================================================

def api_revenue_analytics(request):
    """API endpoint for revenue analytics"""
    if not request.session.get('user_logged_in'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    from home.models import Payment
    
    # Get date range from request
    days = int(request.GET.get('days', 30))
    start_date = datetime.now() - timedelta(days=days)
    
    # Daily revenue
    daily_revenue = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        revenue = Payment.objects.filter(
            payment_status='completed',
            payment_date__date=date.date()
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        daily_revenue.append({
            'date': date.strftime('%Y-%m-%d'),
            'revenue': float(revenue)
        })
    
    return JsonResponse({'daily_revenue': daily_revenue})


def api_appointment_trends(request):
    """API endpoint for appointment trends"""
    if not request.session.get('user_logged_in'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    # Get date range
    days = int(request.GET.get('days', 30))
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    # Daily appointments
    daily_appointments = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d')
        count = bookappointment.objects.filter(appdate=date).count()
        
        daily_appointments.append({
            'date': date,
            'count': count
        })
    
    return JsonResponse({'daily_appointments': daily_appointments})


def api_doctor_performance(request):
    """API endpoint for doctor performance"""
    if not request.session.get('user_logged_in'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    from django.db.models import Count, Avg
    from home.models import DoctorRating, Payment
    
    doctors = DoctorDetail.objects.all()
    performance_data = []
    
    for doctor in doctors:
        # Appointments
        appointments = appointmenthistory.objects.filter(doctoremail=doctor.email).count()
        
        # Revenue
        revenue = Payment.objects.filter(
            doctor=doctor,
            payment_status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        # Rating
        avg_rating = DoctorRating.objects.filter(
            doctor=doctor,
            is_verified=True
        ).aggregate(avg=Avg('rating'))['avg'] or 0
        
        performance_data.append({
            'name': doctor.name,
            'appointments': appointments,
            'revenue': float(revenue),
            'rating': round(float(avg_rating), 2)
        })
    
    return JsonResponse({'doctors': performance_data})



# ============================================================================
# PWA OFFLINE PAGE
# ============================================================================

def offline_page(request):
    """Offline page for PWA"""
    return render(request, 'offline.html')
