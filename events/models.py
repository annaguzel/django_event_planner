from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Event(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE , related_name='my_events',null=True)
	title = models.CharField(max_length= 150)
	description = models.TextField()
	location = models.TextField()
	date = models.DateField()
	time = models.TimeField()
	seats = models.IntegerField()
	created_on = models.DateTimeField(auto_now=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return (self.title)

	def booked_seats(self):
		return sum(self.bookings.all().values_list('ticket', flat=True))

	def get_seats_left(self):
		return self.seats - self.booked_seats()


class Booking(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
	owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name="my_booking")
	ticket = models.IntegerField()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	bio = models.TextField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return str(self.user)


def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile.objects.create(user = instance)

post_save.connect(create_profile, sender = User)
