
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
import random
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