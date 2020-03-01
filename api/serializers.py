from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from events.models import Event, Booking


class ListSerializer(serializers.ModelSerializer):
	description = serializers.HyperlinkedIdentityField(
		view_name = "event-detail",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)
	class Meta:
		model = Event
		fields = ['title', 'description']

class DetailSerializer(serializers.ModelSerializer):
	owner = serializers.SerializerMethodField()
	booking = serializers.HyperlinkedIdentityField(
		view_name = "book-event",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)
	class Meta:
		model = Event
		fields = ["title", "owner", "description", "location", "date", "time",
		"seats", "booking",]

	def get_owner(self, obj):
		return "%s"%(obj.owner.username)
