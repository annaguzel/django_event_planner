from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, BookingForm, ProfileForm
from django.contrib import messages
from .models import Event, Booking, Profile
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User


def home(request):
    events = Event.objects.filter(date__gte=datetime.now())
    query = request.GET.get('q')
    if query:
        events = events.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(owner__username__contains=query))
    context = {
    'events': events,
    }
    return render(request, 'home.html',context)


def edit_profile(request, user_id):
    profile = Profile.objects.get(user_id = user_id)
    if request.user != profile.user:
        return redirect('home')
    form= ProfileForm(instance = profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)



def profile(request, user_id):
    user = User.objects.get(id=user_id)
    events = user.my_events.all()
    context={
        'user': user,
        'events': events,
    }
    return render(request, 'profile.html', context)


def dashboard(request):
	my_events = request.user.my_events.all()
	my_bookings = request.user.my_booking.filter(event__date__lt = datetime.today())
	context = {
	'my_events': my_events,
	'my_bookings': my_bookings,
	}
	return render(request, 'dashboard.html', context)


def create(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.owner = request.user
            user.save()
            return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)



def event_detail(request,event_id):

        event = Event.objects.get(id = event_id)
        context={
         "event":event
        }
        return render(request,'event_detail.html', context)

def edit_event(request, event_id):
        event_obj = Event.objects.get(id = event_id)
        if request.user != event_obj.owner:
            return redirect('home')
        form= EventForm(instance = event_obj)
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES, instance=event_obj)
            if form.is_valid():
                form.save()
            return redirect('home')

        context = {
        'form': form,
        'event': event_obj,
        }
        return render(request,'edit_event.html', context)


def event_book(request,event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event= Event.objects.get(id=event_id)
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.event= event
        booking.owner = request.user
        seats = event.get_seats_left()
        if booking.ticket <= seats:
            booking.save()
            return redirect("event-details", event_id)
        else:
            messages.warning(request, "Not enough seats!")
    context = {
    "form":form,
    "event":event,
    }
    return render(request, 'book_event.html', context)



class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")
