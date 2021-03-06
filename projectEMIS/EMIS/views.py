import uuid

from . forms import *
from django.shortcuts import *
from django.http import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token
from . models import *
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from . group_filter import *
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render_to_response


@requires_csrf_token
def login(request):
    return render(request, 'login.html')


@login_required(login_url='/')
def splash(request, usr_id, rec_id):
    return render(request, 'EMIS/splash.html', context={'user': request.user})


def verify_password(request):
    if request.method == 'GET':
        token = request.GET.get('token', None)
        try:
            EMISUser.objects.get(unlock_code=token)
        except EMISUser.DoesNotExist:
            return redirect('/')
        return render(request, 'EMIS/reset_password.html', context={'token': token})
    elif request.method == 'POST':
        token = request.POST.get('token', None)
        password = request.POST.get('password', None)
        verify_password_value = request.POST.get('verify_password', None)
        if password != verify_password_value:  # Todo - Make sure I change this to use a form in forms.py instead to enforce the password restrictions
            error = "Passwords do not match.  Please try again."
            return render(request, 'EMIS/reset_password.html', context={'form': {'errors': error}})
        if token:
            try:
                emis_user = EMISUser.objects.get(unlock_code=token)
                emis_user.locked_out = False
                emis_user.login_attempts = 0
                emis_user.save()
                user = User.objects.get(email=emis_user.user.email)
                user.set_password(password)
                user.save()
                return redirect('/')
            except EMISUser.DoesNotExist:
                return render(request, 'EMIS/reset_password.html',
                              context={'form': {'errors': 'SOMETHING WENT WRONG! THAT ACCOUNT DOES NOT EXIST!'}})
    else:
        return Http404


def forgot_password(request):
    def render_forgot_password_page(context=None):
        return render(request, 'EMIS/forgot_password.html', context=context)

    if request.method == 'GET':
        return render_forgot_password_page()
    elif request.method == 'POST':
        email = request.POST.get('email_address', None)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            emis_user = EMISUser.objects.get(user=user)
            token = uuid.uuid4()
            emis_user.unlock_code = token
            emis_user.save()
            message = """
                <a href="http://%s/verify_password/?token=%s">Click here</a> unlock your account.
            """ % (request.META.get('HTTP_HOST'), token)
            email = EmailMessage('EMIS - Forgot Password Notification', message, to=[user.email])
            email.content_subtype = 'html'
            email.send()
            return render_forgot_password_page(
                context={'form': {'message': 'An email was sent to %s.  Please follow the instructions' % user.email}})
        else:
            return render(request, 'EMIS/forgot_password.html', context={
                'form': {'errors': "We do not have record of that email address.  Please try another email address."}})
    else:
        return Http404


def logout_view(request):
    logout(request)
    template = loader.get_template('EMIS/logout.html')
    return HttpResponse(template.render(request))


@patient
def patient_home(request):
    return render(request, 'EMIS/patient.html', context={'user': request.user})


@login_required(login_url='/')
def patPI(request):
    if request.method == 'POST':
        user_form = ExtendUserForm(request.POST, instance=request.user)
        profile_form = PersonalInfoForm(request.POST, instance=request.user.personalinfo)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/pat_pers-info/')
        else:
            messages.error(request, 'Please correct the error above.')
    else:
        user_form = ExtendUserForm(instance=request.user)
        profile_form = PersonalInfoForm(instance=request.user.personalinfo)
    return render(request, 'EMIS/pat_pers-info.html', {
        'user_form': user_form,
        'profile_form': profile_form
        })


@login_required(login_url='/')
def patIns(request):
    if request.method == 'POST':
        user_form = ExtendUserForm(request.POST, instance=request.user)
        ins_form = InsInfoForm(request.POST, instance=request.user.personalinfo)
        if user_form.is_valid() and ins_form.is_valid():
            ins_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/pat_ins-info/')
        else:
            messages.error(request, 'Please correct the error above.')
    else:
        ins_form = InsInfoForm(instance=request.user.personalinfo)
    return render(request, 'EMIS/pat_ins-info.html', {
        'ins_form': ins_form
    })


@login_required(login_url='/')
def patViewMedRec(request):
    items = MedicalRecord.objects.all().filter(user=request.user)
    return render(request, 'EMIS/pat_view-medrec.html', {'items': items})


def patMedRecDetail(request, usr_id, rec_id):
    try:
        rec = MedicalRecord.objects.get(pk=rec_id)
    except MedicalRecord.DoesNotExist:
        raise Http404("Medical Record does not exist.")
    person = User.objects.get(pk=usr_id)
    form = MedRecForm(instance=rec)
    return render(request, 'EMIS/pat_view-medRecDetail.html', {
        'medrec': form,
        'person': person
        })


@login_required(login_url='/')
def patAddMedRec(request):
    if request.method == 'POST':
        user_form = ExtendUserForm(request.POST, instance=request.user)
        medrec_form = AddMedRecForm(request.POST)
        if user_form.is_valid() and medrec_form.is_valid():
            temp_rec = medrec_form.save(commit=False)
            temp_rec.user = request.user
            temp_rec.save()
            messages.success(request, 'Record added successfully!')
            return redirect('/pat_add-medrec/')
        else:
            messages.error(request, 'Please correct the error above.')
    else:
        medrec_form = AddMedRecForm()
    return render(request, 'EMIS/pat_add-medrec.html', {
        'medrec_form': medrec_form
    })


@login_required(login_url='/')
def docViewPatients(request):
    items = User.objects.all()
    return render(request, 'EMIS/doc_view-patients.html', {'items': items})


@login_required(login_url='/')
def docViewMedRec(request, usr_id):
    person = User.objects.get(pk=usr_id)
    items = MedicalRecord.objects.all().filter(user=person)
    return render(request, 'EMIS/doc_view-medrec.html', {'items': items})


def docViewMedRecDetail(request, usr_id, rec_id):
    try:
        rec = MedicalRecord.objects.get(pk=rec_id)
    except MedicalRecord.DoesNotExist:
        raise Http404("Medical Record does not exist.")
    person = User.objects.get(pk=usr_id)
    form = MedRecForm(instance=rec)
    return render(request, 'EMIS/doc_view-medRecDetail.html', {
        'detail': form,
        'person': person
        })


def docAddMedRec(request):
    if request.method == 'POST':
        medrec_form = docAddMedRecForm(request.POST)
        patient = User.objects.get(id=request.POST.get('patient'))
        if medrec_form.is_valid():
            temp_rec = medrec_form.save(commit=False)
            temp_rec.user = patient
            temp_rec.save()
            messages.success(request, 'Record added successfully!')
            return redirect('/doc_add-medrec/')
        else:
            messages.error(request, 'Please correct the error above.')
    else:
        medrec_form = docAddMedRecForm()
    return render(request, 'EMIS/doc_add-medrec.html', {
        'medrec_form': medrec_form
    })


@doctor
def doctor_home(request):
    return render(request, 'EMIS/doctor.html', context={'user': request.user})


@clinical_staff
def cstaff_home(request):
    return render(request, 'EMIS/clinical_staff.html', context={'user': request.user})


@nurse
def nurse_home(request):
    return render(request, 'EMIS/nurse.html', context={'user': request.user})


@lab
def lab_home(request):
    return render(request, 'EMIS/lab.html', context={'user': request.user})


@pharmacy
def pharmacy_home(request):
    return render(request, 'EMIS/pharmacy.html', context={'user': request.user})


@insurance
def insurance_home(request):
    return render(request, 'EMIS/insurance.html', context={'user': request.user})


@login_required(login_url='/')
def user_not_auth(request):
    return render(request, 'EMIS/user_not_auth.html', context={'user': request.user})


def auth_view(request):
    def render_locked_out_page():
        return render(request, 'login.html',
                      context={'form': {'locked_out': True}})

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        try:
            emisuser = EMISUser.objects.get(user__username=username)
        except EMISUser.DoesNotExist:
            emisuser = None
        attempts = 0
        if user is not None:
            auth.login(request, user)
            if emisuser:
                if emisuser.locked_out:
                    return render_locked_out_page()
                emisuser.login_attempts = 0
                emisuser.save()
            if user.groups.filter(name='Patient'):
                return HttpResponseRedirect(reverse('patient_home'))
            elif user.groups.filter(name='Doctor'):
                return HttpResponseRedirect(reverse('doctor_home'))
            elif user.groups.filter(name='Clinical_Staff'):
                return HttpResponseRedirect(reverse('cstaff_home'))
            elif user.groups.filter(name='Nurse'):
                return HttpResponseRedirect(reverse('nurse_home'))
            elif user.groups.filter(name='Lab'):
                return HttpResponseRedirect(reverse('lab_home'))
            elif user.groups.filter(name='Pharmacy'):
                return HttpResponseRedirect(reverse('pharmacy_home'))
            elif user.groups.filter(name='Insurance'):
                return HttpResponseRedirect(reverse('insurance_home'))
            else:
                return HttpResponseRedirect(reverse('splash'))
        else:
            if emisuser:
                emisuser.login_attempts += 1
                emisuser.save()
                attempts = emisuser.login_attempts
                if attempts > 3:
                    emisuser.locked_out = True
                    emisuser.save()
                    return render_locked_out_page()
            return render(request, 'login.html',
                          context={'form': {'errors': 'Invalid Credentials', 'attempts': attempts}})


def create_account(request):
    if request.method == "POST":
        print("******")
        form = UserForm(request.POST)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('username', None)
        if form.is_valid():
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.groups.add(Group.objects.get(name='Patient'))
                user.set_password(password)  # This line will hash the password
                print("USER PASSWORD IS: " + username + " " + password + "*******************************************")
                user.save()  # DO NOT FORGET THIS LINE
                EMISUser.objects.create(user=user)
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return HttpResponseRedirect('/patient_home/')  ##created account is successfully logged on now
                return HttpResponseRedirect('/login/')
    else:
        form = UserForm()
    return render(request, 'create_account.html', {'form': form})


def addCalendar(request):
    if request.method == 'POST':
        addevent_form = docAddEvent(request.POST)
        patient = User.objects.get(id=request.POST.get('patient'))
        if addevent_form.is_valid():
            temp_rec = addevent_form.save(commit=False)
            temp_rec.user = patient
            temp_rec.save()
            messages.success(request, 'Record added successfully!')
            return redirect('/doc_add-cal/')
        else:
            messages.error(request, 'Please correct the error above.')
    else:
        addevent_form = docAddEvent()

    return render_to_response('EMIS/doc_add-cal.html', {'medrec_form': addevent_form})


@login_required(login_url='/')
def docCalPatients(request):
    items = User.objects.all()
    return render(request, 'EMIS/doc_cal-patients.html', {'items': items})


@login_required(login_url='/')
def viewCalendar(request, usr_id):
    person = User.objects.get(pk=usr_id)
    items = Event.objects.all().filter(user=person)
    return render(request, 'EMIS/doc_view-cal.html', {
        'items': items,
        'person': person
    })


# @login_required(login_url='/')
def contact(request):
    """
    Contact form from which one can send emails. Basic text only so far.
    TODO: need link to contact form instead of directly typing in URL
    """
    form_class = ContactForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name',
                ''
            )
            contact_email = request.POST.get(
                'contact_email',
                ''
            )

            user_email = request.user.email
            form_content = request.POST.get('content', '')
            # Email the profile with the contact information
            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'user_email': user_email,
                'contact_email': contact_email,
                'form_content': form_content,
                })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                [contact_email],
                headers = {'Reply-To': contact_email}
            )
            email.send()
            return redirect('contact')
    return render(request, 'contact.html', {
        'form': form_class,
    })

def schedule_appointment(request):
    """
    Like contact, but specifically to email the admin.
    """
    form_class = ScheduleAppointmentForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name',
                ''
            )
            contact_email = 'cs3773team2@gmail.com'
            user_email = request.user.email
            form_content = request.POST.get('content', '')

            # Email the profile with the contact information
            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'user_email': user_email,
                'form_content': form_content,
            })
            content = template.render(context)
            subject = 'Patient %s requesting an appointment scheduling.' % contact_name
            email = EmailMessage(
                subject,
                content,
                "Your website" +'',
                [contact_email],
                headers = {'Reply-To': contact_email}
            )
            email.send()
            return redirect('schedule_appointment')
    return render(request, 'schedule_appointment.html', {
        'form': form_class,
    })
