from django.contrib import admin
from .models import Event,Booking,Profile,UserFollowing

admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(Profile)
admin.site.register(UserFollowing)
