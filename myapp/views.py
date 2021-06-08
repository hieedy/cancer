from django.shortcuts import render
from myapp.models import myreview
from myapp.models import myhelp
from myapp.models import mypatient
from myapp.models import mycontactus
from myapp.models import mydoctor
from django.shortcuts import redirect
from myapp.models import mymessages

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from myapp.models import mydiagnostic
from myapp.models import myhospital
from myapp.models import myclinic
from myapp.models import myappointment
from django.core import serializers
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
from matplotlib import pylab
from pylab import *
from PIL import Image, ImageDraw
import PIL, PIL.Image
from io import StringIO
# warnings.filterwarnings("ignore")
# plt.style.use('fivethirtyeight')
import statsmodels.api as sm
import matplotlib
from io import BytesIO
import io
import base64


# Create your views here.
def test(request):
    us = User.objects.all()

    for u  in us:
        print(u.username)

    return HttpResponse("<h1>Done</h1>")    

def form(request):
    return render(request,'form.html',{})

def index(request):
    return render(request,'index.html',{})

def register(request):

    if request.method == 'POST':
        name = request.POST.get('fn')
        email = request.POST.get('em')
        phone = request.POST.get('phn')
        opass = request.POST.get('npwd') 
        cpass = request.POST.get('cpwd')
        user_em = mypatient.objects.filter(pat_email = email)

        if len(user_em) > 0:
            return render(request, 'register.html', {'result':False})
        else:
            if opass == cpass:
                post = mypatient()
                post.pat_name = name
                post.pat_email = email
                post.pat_contact = phone
                post.pat_pass = opass
                post.save()

                post.generate_patient_id()
                post.save()
                # print("done")
                return render(request,'register.html',{'result':True})
            else:
                return render(request, 'register.html',{"result":False})

    return render(request,'register.html',{})


def contactus(request):
    if request.method == "POST":
        post = mycontactus()
        post.cs_name = request.POST.get('fn')
        post.cs_email = request.POST.get('em')
        post.cs_address = request.POST.get('add')
        post.cs_phone = request.POST.get('phn')
        post.cs_msg = request.POST.get('message')

        try:
            post.save()
            res = 1
        except Exception:
            res = 2

        return render(request, 'contactus.html',{'res':res})
    else:
        return render(request,'contactus.html',{})

def login(request):
    if request.method == "POST":
        formpost = True
        useremail = request.POST.get('em')
        pw = request.POST.get('npwd')
        errormessage = ""
        expert = mypatient.objects.filter(pat_email = useremail, pat_pass = pw)
        k = len(expert)
        if k>0:
            print("Valid Credentials")
            request.session['em'] = useremail
            request.session['user_id'] = expert[0].id
            request.session['doc_name'] = expert[0].doc_name
             # {{request.session.doc_name}}
            return redirect('/dashboard')

        else:
            res = 1
            print("Invalid Credentials")
            errormessage = "Invalid Credentials"
            return render(request,'login.html',{'formpost':formpost,'res':res})
    
    else:
        formpost = False
        return render(request,'login.html',{'formpost':formpost})


def recoverpassword(request):
    return render(request,'recoverpassword.html',{})

def footer(request):
    return render(request,'footer.html',{})

def help(request):
    if not request.session.has_key('em'):
        return redirect('/login')

    if request.method == "POST":
        post = myhelp()
        post.help_sub = request.POST.get('sub')
        post.help_msg = request.POST.get('msg')
        post.user_email = request.session.get('em')

        try:
            post.save()
            res = 1
        except Exception:
            res = 2

        return render(request, 'help.html',{'res':res})
    else:
        return render(request,'help.html',{})

def dochelp(request):
    if not request.session.has_key('docem'):
        return redirect('/login')
    if request.method == "POST":
        post = myhelp()
        post.help_sub = request.POST.get('sub')
        post.help_msg = request.POST.get('msg')
        post.user_email = request.session.get('docem')

        try:
            post.save()
            res = 1
        except Exception:
            res = 2

        return render(request, 'doctorF/dochelp.html',{'res':res})
    else:
        return render(request,'doctorF/dochelp.html',{})



def editprofile(request):

    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    if not request.session.has_key('em'):
        return redirect('/login')
    userdetail = mypatient.objects.get(pat_email = request.session['em'])
    if request.method == 'POST':
        type_form = request.POST.get('type')
        if type_form == "1":
            userdetail.pat_img = request.FILES.get('image')
            userdetail.save()
        else:
            detail = mypatient.objects.get(pat_email = request.session['em'])
            detail.pat_name = request.POST.get('fn')
            detail.pat_contact = request.POST.get('phn')
            detail.pat_dob = request.POST.get('dob')
            detail.pat_bloodgroup = request.POST.get('bg')
            detail.pat_pincode = request.POST.get('pin')
            detail.pat_city = request.POST.get('city')
            detail.pat_state = request.POST.get('state')
            detail.pat_address = request.POST.get('address')
            detail.pat_gender = request.POST.get('gen')

            detail.save()
            
            data = mypatient.objects.get(pat_email = request.session['em'])
            print('age is ',calculate_age(data.pat_dob))
            data.pat_age = int(calculate_age(data.pat_dob))
            data.save()
            return render(request,'dashboard.html',{'us':data})

    print(userdetail.id)
    patient_dob = None

    if userdetail.pat_dob!=None:
        patient_dob = userdetail.pat_dob.strftime("%Y-%m-%d")


    return render(request,'editprofile.html',{'us':userdetail, 'pat_dob':patient_dob})


def changepassword(request):
    if not request.session.has_key('em'):
       return redirect('/login')
    if request.method == 'POST':
        temp = mypatient.objects.get(pat_email = request.session['em'])
        password = request.POST.get('old')
        newpwd = request.POST.get('npwd')
        confirmpwd = request.POST.get('cpwd')
        
        if(newpwd == confirmpwd):
            p =temp.pat_pass
            #print("db password",p)
            if(password == p):
                temp.pat_pass = newpwd
                temp.save()
                rest = "Password Changed"
                print("Password Updated")
                return render(request,'Changepassword.html',{'rest':rest})
            else:
                print("Password not updated")
                res = "Invalid Current Password"
                return render(request,'changepassword.html',{'res':res})
        else:
            res = "Confirm password and new password don't match"
            return render(request,'changepassword.html',{'res':res})
    else:
        return render(request,'changepassword.html')


def review(request):                     
    if not request.session.has_key('em'):  
        return redirect('/login')          
    if request.method == "POST":           
        post = myreview()                        
        post.rev_sub = request.POST.get('name')   
        post.rev_msg = request.POST.get('msg')    
        post.user_email = request.session.get('em')

        try:
            post.save()
            res = 1
        except Exception:
            res = 2

        return render(request, 'review.html', {'res':res})
    else:
        return render(request,'review.html',{})


def base(request):
    return render(request,'base.html',{})


def sidebar(request):
    return render(request,'sidebar.html',{})


def logout(request):
    if not request.session.has_key('em'):
        return redirect("/login")
    del request.session['em']
    return redirect('/login')


def profile(request):
    if not request.session.has_key('em'):
        return redirect('/login')
    userdetail = mypatient.objects.get(pat_email= request.session['em'])
    return render(request,'profile.html',{'user':userdetail})


def dashboard(request):
    if not request.session.has_key('em'):
        return redirect('/login')
    return render(request,'dashboard.html',{})


def chatpage(request):

    if not  request.session.has_key('em'):
        return redirect('/login')

    # appointments = myappointment.objects.filter(patient_id = current_user, app_status = 'A')

    current_user = mypatient.objects.get(pat_email = request.session.get('em'))
    latest_user_approved_appointment = myappointment.objects.filter(patient_id = current_user, app_status='A', app_isactive = True).order_by('-id')[0]

    latest_user_appointed_doc_messages = mymessages.objects.filter(app_id = latest_user_approved_appointment)

    print(latest_user_appointed_doc_messages)


    
    
    return render(request,'chatpage.html',{'messages':latest_user_appointed_doc_messages, 'appointment':latest_user_approved_appointment})


def getmessages(request):

    app_id = request.GET.get('app_id')

    user_appointment = myappointment.objects.get(id = int(app_id))

    messages = mymessages.objects.filter(app_id = user_appointment.id)

    ser_messages = serializers.serialize('json', messages)
    
    
    
    return JsonResponse({'messages':ser_messages}, safe=False)


def user_chat_update(request):
    if request.method == 'POST':
        message_text = request.POST.get('msg')
        attachment  = request.FILES.get('attachment')
        appointment_id = request.POST.get('app_id')
        doctor_id = request.POST.get('doc_id')

        today_time_date = datetime.datetime.now()


        message  =  mymessages()
        message.mess_from = mypatient.objects.get(pat_email = request.session.get('em')).id
        
        
        message.mess_to =   doctor_id

        message.mess_date = today_time_date.date()
        message.mess_time = today_time_date.time()

        message.mess_message = message_text
        if attachment:
            message.mess_attachment = attachment

        message.app_id = myappointment.objects.get(id = int(appointment_id))


        message.save()

        ser_message = serializers.serialize('json', [message,])

        print(message, attachment, appointment_id, doctor_id)
        return JsonResponse({'message': ser_message}, safe=False)




def doctorspage(request):
    if not request.session.has_key('em'):
        return redirect('/login')
    docdata = mydoctor.objects.all()
    return render(request,'doctorspage.html',{'doctors':docdata})


def labs(request):
    if not request.session.has_key('em'):
        return redirect('/login')

    labdata = mydiagnostic.objects.all()
    return render(request,'labs.html',{'labs':labdata})


def hospitals(request):
    if not request.session.has_key('em'):
        return redirect('/login')
        # city = mypatients.objects.get(email = request.session.get('em')).city
        # docs =  doc.objects.filter(city = city)
    hospitaldata = myhospital.objects.all()
    return render(request,'hospitals.html',{'hospitals':hospitaldata})


def clinics(request):
    if not request.session.has_key('em'):
        return redirect('/login')

    clinicdata = myclinic.objects.all()
    return render(request,'clinics.html',{'clinics':clinicdata})


def userappointment(request, id):
    
    if request.method =='POST':
        ap = myappointment()
        ap.patient_id = mypatient.objects.get(pat_email = request.session.get('em'))
        ap.doctor_id = mydoctor.objects.get(id= id)
        userapp_date = request.POST.get('dateforapp')
        userapp_dayoftime = request.POST.get('tofd')
        userapp_notes = request.POST.get('notes')
        ap.app_applyTime_Date = datetime.now()
        ap.app_timeofday = userapp_dayoftime
        ap.app_notes = userapp_notes
        ap.app_date = userapp_date
        # print(userapp_date,userapp_dayoftime,userapp_nates)
        ap.save()
       
    us = mypatient.objects.get(pat_email = request.session.get('em'))
    return render(request,'appointmentpage.html',{'user':us})


def docsidebar(request):
    # doctorName = mydoctor.objects.get(doc_name= request.session['name'])
    doctordetail = mydoctor.objects.get(doc_email= request.session['docem'])
    print(doctordetail)
    return render(request,'doctorF/docsidebar.html',{'doctor': doctordetail})


def docdashboard(request):
    if not request.session.has_key('docem'):
        return redirect('/doclogin')
    return render(request,'doctorF/docdashboard.html',{})


def docprofile(request):
    if not request.session.has_key('docem'):
        return redirect('/doclogin')
    docdetail = mydoctor.objects.get(doc_email= request.session['docem'])
    return render(request,'doctorF/docprofile.html',{'doctor': docdetail})


def doceditprofile(request):
    if not request.session.has_key('docem'):
        return redirect('/doclogin')
    docdetail = mydoctor.objects.get(doc_email = request.session['docem'])
    if request.method == 'POST':
        type_form = request.POST.get('type')
        if type_form == "1":
            docdetail.pat_img = request.FILES.get('image')
            docdetail.save()
        else:
            detail = mydoctor.objects.get(doc_email = request.session['docem'])
            detail.doc_name = request.POST.get('fn')
            detail.doc_contact = request.POST.get('phn')
            detail.doc_gender = request.POST.get('gen')
            detail.doc_experience = request.POST.get('exp')
            detail.doc_pincode = request.POST.get('pin')
            detail.doc_city = request.POST.get('city')
            detail.doc_state = request.POST.get('state')
            detail.qualification = request.POST.get('quali')
            detail.specialization = request.POST.get('specia')
            detail.save()
            data = mydoctor.objects.get(doc_email = request.session['docem'])
            return render(request,'doctorF/docdashboard.html',{'us':data})

    return render(request,'doctorF/doceditprofile.html',{'us':docdetail})

def doclogin(request):
    if request.method == "POST":
        formpost = True
        doctoremail = request.POST.get('docem')
        pw = request.POST.get('npwd')
        errormessage = ""
        expert = mydoctor.objects.filter(doc_email = doctoremail, doc_pass = pw)
        if len(expert)>0:
            print("Valid Credentials")
            request.session['docem'] = doctoremail
            request.session['doc_id'] = expert[0].id
            return redirect('/docdashboard')
        else:
            print("Invalid Credentials")
            errormessage = "Invalid Credentials"
            return render(request,'doctorF/doclogin.html',{})
    
    else:
        formpost = False
        return render(request,'doctorF/doclogin.html',{})




def doclogout(request):
    if not request.session.has_key('docem'):
        return redirect("/doclogin")
    del request.session['docem']
    # del request.session['doc_name']
    return redirect('doclogin')

def docappointment(request):
    doc = mydoctor.objects.get(doc_email = request.session['docem'])

    if request.method == 'POST':
        type_of_form = request.POST.get('type')

        if type_of_form  == "1":
            app_id = request.POST.get('app_id')
            appointment = myappointment.objects.get(id = int(app_id))

            appointment.app_time = request.POST.get('timing')
            appointment.app_reason = None
            appointment.app_status = 'A'
            appointment.app_isactive = True
            appointment.save()

        elif type_of_form == "2":
            app_id = request.POST.get('app_id')
            print(app_id)
            appointment = myappointment.objects.get(id = int(app_id))

            appointment.app_time = None
            appointment.app_reason = request.POST.get('reason')
            appointment.app_status = 'NA'
            appointment.save()

        elif type_of_form == "3":
            app_filter = request.POST.get('filter')
            filter_date = request.POST.get('date')
            print(app_filter,filter_date)

            if app_filter == 'pending_appointments':
                appointments = myappointment.objects.filter(app_status='P', app_date = filter_date, doctor_id = doc)
                return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'selected_field': app_filter, 'entered_date': filter_date})

            elif app_filter == 'approved_appointments':
                appointments = myappointment.objects.filter(app_status='A', app_date = filter_date,doctor_id = doc)
                return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'selected_field': app_filter, 'entered_date': filter_date})
            elif app_filter == 'all_appointments':
                appointments = myappointment.objects.filter(app_date = filter_date,doctor_id = doc)
                return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'selected_field': app_filter, 'entered_date': filter_date})    

            elif app_filter == 'rejected_appointments':
                appointments = myappointment.objects.filter(app_status='NA', app_date = filter_date,doctor_id = doc)
                return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'selected_field': app_filter, 'entered_date': filter_date})    

  
    # will show all apointments of today
    appointments = myappointment.objects.filter(doctor_id = doc, app_date = date.today())
    return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'entered_date': date.today().strftime('%Y-%m-%d')} )

def userappointmentstatus(request):
    user = mypatient.objects.get(pat_email = request.session['em'])
    selected_field = 'all_appointments'
    if request.method == 'POST':
        type_of_form = request.POST.get('type')

        app_filter = request.POST.get('filter')
        print(app_filter)

        if app_filter == 'pending_appointments':
            userappointments = myappointment.objects.filter(app_status='P', patient_id = user )
            return render(request,'userappointmentstatus.html',{'userappointments':userappointments, 'selected_field': app_filter})

        elif app_filter == 'approved_appointments':
            userappointments = myappointment.objects.filter(app_status='A',  patient_id = user )
            return render(request,'userappointmentstatus.html',{'userappointments':userappointments, 'selected_field': app_filter})
        elif app_filter == 'all_appointments':
            userappointments = myappointment.objects.filter( patient_id = user )
            return render(request,'userappointmentstatus.html',{'userappointments':userappointments, 'selected_field': app_filter})    

        elif app_filter == 'rejected_appointments':
            userappointments = myappointment.objects.filter(app_status='NA', patient_id = user )
            return render(request,'userappointmentstatus.html',{'userappointments':userappointments, 'selected_field': app_filter})    

  
    # will show all apointments of today
    appointments = myappointment.objects.filter(patient_id = user)
    return render(request,'userappointmentstatus.html',{'userappointments':appointments,'selected_field':selected_field} )


# def get_today_appointments(request):
#     doc= mydoctor.objects.get(doc_email = request.session['docem'])
#     appointments = list(myappointment.objects.filter(doctor_id = doc, app_status = 'P', app_date = date.today()))

#     content = {
#         'appointments': serializers.serialize('json',appointments)
#     }
#     return JsonResponse(content)
   

def docchangepassword(request):
    if not request.session.has_key('docem'):
        return redirect("/doclogin")
    if request.method == 'POST':
        temp = mydoctor.objects.get(doc_email = request.session['docem'])
        password = request.POST.get('old')
        newpwd = request.POST.get('npwd')
        confirmpwd = request.POST.get('cpwd')
        
        if(newpwd == confirmpwd):
            p =temp.doc_pass
            if(password == p):
                temp.doc_pass = newpwd
                temp.save()
                rest = "Password Changed"
                print("Password Updated")
                return render(request,'doctorF/docchangepassword.html',{'rest':rest})
            else:
                print("Password not updated")
                res = "Invalid Current Password"
                return render(request,'doctorF/docchangepassword.html',{'res':res})
        else:
            res = "Confirm password and new password don't match"
            return render(request,'doctorF/docchangepassword.html',{'res':res})
    else:
        return render(request,'doctorF/docchangepassword.html',{})


def docpatients(request):
    if not request.session.has_key('docem'):
        return redirect("/doclogin")

    curr_doc = mydoctor.objects.get(doc_email = request.session.get('docem'))

    appointments = myappointment.objects.filter(doctor_id = curr_doc, app_isactive = True)
    selected_field = 'enabled'

    if request.method == 'POST':
        selected_field = request.POST.get('apply_filter')

        if selected_field == 'enabled':
            appointments = myappointment.objects.filter(doctor_id = curr_doc, app_isactive = True, app_status = 'A')
            

        elif selected_field == 'disabled':
            appointments = myappointment.objects.filter(doctor_id = curr_doc, app_isactive = False, app_status = 'A') # otheriwise it will show pending and not approved patients also


    return render(request,'doctorF/docpatients.html',{'appointments':appointments,'selected_field':selected_field})
    
def enable_disable(request):
    app_id = request.GET.get('app_id')
    status = request.GET.get('status')

    print(app_id, status)
    appointment = myappointment.objects.get(id = app_id)

    if status == "enable":
        appointment.app_isactive = True
    elif status == "disable":
        appointment.app_isactive = False

    appointment.save()

    print(app_id , status)
    return JsonResponse({'res': True})

def docchatpage(request, appid=None):
    if not request.session.has_key('docem'):
        return redirect("/doclogin")




    if request.method == 'POST':
        message_text = request.POST.get('msg')
        attachment  = request.FILES.get('attachment')
        appointment_id = request.POST.get('app_id')
        patient_id = request.POST.get('pat_id')

        today_time_date = datetime.datetime.now()


        message  =  mymessages()

        message.mess_from = mydoctor.objects.get(doc_email = request.session.get('docem')).id

        print(mydoctor.objects.get(doc_email = request.session.get('docem')).id)
        print(request.session.get('docem'))

        message.mess_to = patient_id

        message.mess_date = today_time_date.date()
        message.mess_time = today_time_date.time()

        message.mess_message = message_text

        if attachment:
            message.mess_attachment = attachment

        message.app_id = myappointment.objects.get(id = int(appointment_id))


        message.save()

        ser_message = serializers.serialize('json', [message,])

        print(message, attachment, appointment_id, patient_id)
        
        return JsonResponse({'message': ser_message}, safe=False)

    
    appointment = myappointment.objects.get(id = appid)
    all_messages = mymessages.objects.filter(app_id = appointment)

   

    return render(request,'doctorF/docchatpage.html',{'all_messages':all_messages, 'appointment' : appointment})

def lungsprediction(request):
    return render(request,'doctorF/lungsprediction.html',{})


def prostateprediction(request):
    return render(request,'doctorF/prostateprediction.html',{})

def newPage(request):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    print(os.path.abspath(os.getcwd()))
    df = pd.read_csv(os.path.abspath(os.getcwd())+'/total_cancer_deaths_by_type_mine_cleandata.csv')
    df.head()
    df1 = df[df['Entity'] == 'World']

    df2=df1.sum(axis=0)

    df2 = df2.iloc[3:]
    df2 = df2.sort_values(ascending= False)
    df2 = pd.DataFrame(df2)
    print(df2)
    return render(request,'doctorF/new.html',{'data':df2})

## Visualizations 

def visLungSurvival(request):
    return render(request,'visLungSurvival.html',{}) 

def visLSTopCY(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(17, 12), dpi=90,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        matplotlib.rcParams['axes.titlepad'] = 0   #The offset of the title from the top of the axes, in points. Default is None

        # visualization code

        df = pd.read_csv('five-year-survival-rates-from-lung-cancer.csv')
        print(df)

        yr = int(request.POST.get('year'))
        df1 = df[df['Year'] == yr]

        n = int(request.POST.get('topc'))

        df1 = df1.sort_values('Lung',ascending = False)
        df1 = df1.iloc[:n,:]

        #plt.figure(figsize=(15, 10))
        ax = sns.barplot(x = 'Lung', y = 'Entity',data=df1)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right',fontdict={'verticalalignment': 'baseline'})

        plt.grid()
        plt.ylabel(ylabel=None)
        plt.xlabel(None)
        plt.title("Survival Lung Cancer Rates in Top "+str(n) +" Countries",loc='left')
                
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visLSTopCY.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visLSTopCY.html',{})

def visLSYear(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 6), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code

        df = pd.read_csv('five-year-survival-rates-from-lung-cancer.csv')
        
        yr = int(request.POST.get('year'))

        df1 = df[df['Year'] == yr]

        df1 = df1.sort_values('Lung',ascending = False)

        #plt.figure(figsize=(17, 10),dpi=100)
        ax = sns.barplot(x = 'Entity', y = 'Lung',data=df1)
        #ax = sns.barplot(x = 'Lung', y = 'Entity',data=df1)
        ax.tick_params(axis='both', which='major', pad=20)
        ax.tick_params(axis='both', which='minor', pad=20)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
        #ax.set_xticklabels(rotation = (45), fontsize = 10, va='bottom', ha='left')

        plt.grid()
        ax.set_ylabel("Total Lung Survival Counts")
        plt.title("Survival Lung Cancer Rates")
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visLSYear.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visLSYear.html',{})

def visLSCountry(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 6), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code

        df = pd.read_csv('five-year-survival-rates-from-Lung-cancer.csv')

        country = str(request.POST.get('country'))
        # print(country)
        df1 = df[df['Entity'] == country]

        #plt.figure(figsize=(10, 7))
        ax = sns.barplot(x = 'Year', y = 'Lung',data=df1,palette = 'hls')
        ax.tick_params(axis='both', which='major', pad=20)
        ax.tick_params(axis='both', which='minor', pad=20)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        
        ax.set_ylabel(ylabel=None)
        ax.set_xlabel(None)
        plt.title("Survival Lung Cancer Rates in "+country)
        

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visLSCountry.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visLSCountry.html',{})
