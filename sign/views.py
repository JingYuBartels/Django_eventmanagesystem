from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, get_list_or_404
# Create your views here.



def index(request):

    return render(request, "index.html")


def login_action(request):

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            #response.set_cookie('user', username, 3600)
            respond = HttpResponseRedirect('/event_manage/')
            return respond

    return render(request, "index.html", {"error": "username or password error!"})

    #return render(request, 'index.html')

@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('username', '')
    return render(request, 'event_manage.html', {'user': username, "events": event_list})

@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {'user': username, "guests": contacts})

@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get('phone', '')
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)

    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts, "search_phone": search_phone})

@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = len(get_list_or_404(Guest, event_id=eid))
    guest_sign = len(get_list_or_404(Guest, event_id=eid, sign=1))
    return render(request, 'sign_index.html', {'event': event, 'guest_list': guest_list, 'guest_sign': guest_sign})

@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = len(get_list_or_404(Guest, event_id=eid))
    guest_sign = len(get_list_or_404(Guest, event_id=eid, sign=1))
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, "hint": 'phone error.','guest_list': guest_list, 'guest_sign': guest_sign})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(result, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.', 'guest_list': guest_list, 'guest_sign': guest_sign})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': "user has sign in", 'guest_list': guest_list, 'guest_sign': guest_sign})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        guest_sign = guest_sign + 1
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!', 'guest': result, 'guest_list': guest_list, 'guest_sign': guest_sign})


@login_required
def logout(request):
    auth.logout(request)
    responses = HttpResponseRedirect('/index/')
    return responses
