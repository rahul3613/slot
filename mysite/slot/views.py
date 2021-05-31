from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
import smtplib, ssl
from django.utils import timezone
import datetime
from .models import Cent, Day, Dist, Dist_new, Slice, Time
from .models import User
from .models import Pin


def index(request):
    dist = Dist.objects.order_by('dist_name')
    return render(request, 'slot/index.html', {'dist': dist})


def getdata(request):

    dtm = Time.objects.get(pk = 1)
    if dtm.time != datetime.date.today():
            dtm.change()
            dtm.time = datetime.date.today()
            dtm.save()

    dist = Dist.objects.order_by('dist_name')
    slice = Slice.objects.get(pk = 1)
    leng = len(dist)
    if slice.k == leng:
        slice.j = 0
        slice.k = 0
    slice.j = slice.k
    slice.k = slice.k + 20
    if slice.k>leng:
        slice.k = leng
    slice.save()

    dist = Dist.objects.order_by('dist_name')[slice.j:slice.k]

    return render(request, 'slot/getdata.html', {'dist': dist})


def dist(request):
    dist = Dist.objects.order_by('dist_name')
    try:
        dist_1 = Dist_new.objects.get(dist_name = request.POST['dist'])
    except Dist_new.DoesNotExist:
        dist_1 = Dist_new(dist_name = request.POST['dist'], dist_numb = 1)
        dist_1.save()
    else:
        dist_1.dist_numb += 1
        dist_1.save()  
        
    return render(request, 'slot/new_index.html', {'dist': dist, 'val' : 4})


def login(request):
    try:
        user = User.objects.get(email = request.POST['email'], pin = request.POST['pin'])
    except User.DoesNotExist:
        dist = Dist.objects.order_by('dist_name')
        return render(request, 'slot/new_index.html', {'dist': dist, 'val' : 1})
    else:
        pin_c = get_object_or_404(Pin, pin_code = request.POST['pin'])
        dist = Dist.objects.get(dist_code = pin_c.dist.dist_code)  
        return render(request, 'slot/detail.html', {'user': user, 'dist': dist, 'pin_c': pin_c})


def register(request):
    usr_eml = User.objects.all().values('email')
    if request.POST['email'] in [u['email'] for u in usr_eml]:
        dist = Dist.objects.order_by('dist_name')
        return render(request, 'slot/new_index.html', {'dist': dist, 'val' : 2})
    else:
        lst = ['notify', 'd1', 'd2', 'eight', 'five', 'free', 'paid', 'cvsh', 'covax', 'sptk']
        val = []
        cond = request.POST.getlist("condition")

        for i in range(len(lst)):
            if lst[i] in cond:
                val.append(True)
            else:
                val.append(False)

        dist = Dist.objects.get(dist_code = request.POST['d_code'])

        try:
            pinc = Pin.objects.get(pin_code = request.POST['pin'])
        except Pin.DoesNotExist:
            pinc = Pin(dist = dist, pin_code = request.POST['pin'])
            pinc.save()
            user = User(pin = pinc, email = request.POST['email'], notify = val[0], d1 = val[1], d2 = val[2], eight = val[3], five = val[4], free = val[5], paid = val[6], cvsh = val[7], covax = val[8], sptk = val[9], not_times = 0, time = timezone.now())
            user.save()
        else:
            user = User(pin = pinc, email = request.POST['email'], notify = val[0], d1 = val[1], d2 = val[2], eight = val[3], five = val[4], free = val[5], paid = val[6], cvsh = val[7], covax = val[8], sptk = val[9], not_times = 0, time = timezone.now())
            user.save()

        for i in range(1,6):
            day = Day(usr = user, notify = True, day_numb = i)
            day.save()

        dist = Dist.objects.order_by('dist_name')
        return render(request, 'slot/new_index.html', {'dist': dist, 'val' : 3})


def change(request):
    lst = ['notify', 'd1', 'd2', 'eight', 'five', 'free', 'paid', 'cvsh', 'covax', 'sptk']
    val = []
    cond = request.POST.getlist("condition")

    for i in range(len(lst)):
        if lst[i] in cond:
            val.append(True)
        else:
            val.append(False)

    user = User.objects.get(email = request.POST['email'])

    user.notify = val[0]
    user.d1 = val[1]
    user.d2 = val[2]
    user.eight = val[3]
    user.five = val[4]
    user.free = val[5]
    user.paid = val[6]
    user.cvsh = val[7]
    user.covax = val[8]
    user.sptk = val[9]
    user.save()

    return HttpResponseRedirect(reverse('index',))



def putdata(request, email, day, id):
    days = Day.objects.get(usr = email, day_numb = day)

    try:
        cent = Cent.objects.get(day = days, cent_id = id)
    except Cent.DoesNotExist:
        cent = Cent(day = days, cent_id = id)
        cent.save()
        user = User.objects.get(email = email)
        if user.not_times < 10:
            if user.time < (timezone.now() - datetime.timedelta(minutes = 10)):
                notify(email, 'early')
                user.not_times += 1
                user.time = timezone.now()
                user.save()
        else:
            notify(email, 'last')
            user.not_times = 0
            user.notify = False
            user.save()
    else:
        pass

    return HttpResponse("Task completed")




def notify(email, time):
    message1 = """\
Subject: Slot Alert

Hi..
There is/are new "VACANT" slots available (in the next 6 days) with the conditions you had requested. Please visit CoWIN website (https://www.cowin.gov.in/home) to check them and to book your slot.

This alert is purely based on CoWIN API data. If you think this is not useful then feel free to turn off the nitifications.

If you don't need mail alert anymore. Please log in at () to turn off the notification.

Yours,
Rahul"""

    message2 = """\
Subject: Last Slot Alert

Hi..
There is/are new "VACANT" slots available (in the next 6 days) with the conditions you had requested. Please visit CoWIN website (https://www.cowin.gov.in/home) to check them and to book your slot.

This is your 10th Slot Alert mail please login at () to turn on your notification again.

Yours,
Rahul"""


    if time == 'last':
        message = message2
    else:
        message = message1
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    s_email = "slot.update@gmail.com"  # Enter your address
    password = "second@wave"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(s_email, password)
        server.sendmail(s_email, email, message)
        