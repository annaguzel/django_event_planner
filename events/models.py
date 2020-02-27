from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE , related_name='my_events')
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
