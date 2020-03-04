from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, BookingForm, ProfileForm,UserForm
from django.contrib import messages
from .models import Event, Booking, Profile, UserFollowing
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def follow(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user.is_anonymous:
        return redirect('login')
    if UserFollowing.objects.filter(follower_user_id=request.user,following_user_id=user).count()>0:
        messages.warning(request, "You have already followed this user")
        return redirect('profile',user_id)
    follow= UserFollowing.objects.create(follower_user_id=request.user,following_user_id=user)
    follow.refresh_from_db()
    messages.success(request, ('You are following selected user'))
    return redirect ('profile',user_id)

# def unfollow(request, user_id):
#     user = User.objects.get(id=user_id)
#     follow = UserFollowing.objects.get(follower_user_id = request.user , following_user_id = user)
#     if not follow:
#         follow.delete()
#         follow.refresh_from_db()
#         messages.success(request, ('You have unfollowed selected user'))
#         return redirect ('profile',user_id)
#         messages.warning(request, ('You are not following this user'))
#         return redirect ('profile',user_id)
#     else:
#         messages.warning(request, ('You are not following this user'))
#         return redirect ('profile',user_id)
#

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
    user_form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            return redirect('profile', user_id)

    context = {
        'form': form,
        'profile': profile,
        'user_form':user_form
    }
    return render(request, 'edit_profile.html', context)



def profile(request, user_id):
    user = User.objects.get(id=user_id)
    my_events = user.my_events.filter(date__gte=datetime.now())
    context={
        'user': user,
        'my_events':my_events,
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
	event = Event.objects.get(id=event_id)
	booking = Booking.objects.filter(owner=request.user)
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
			subject = 'Event Ticket'
			html_message = render_to_string('ticket_event.html',{'event': event,'booking':booking})
			plain_message = strip_tags(html_message)
			from_email = 'anna.osama1234@gmail.com'
			to = booking.owner.email

			mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

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
