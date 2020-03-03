from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date
from events.models import Event, Booking


############################

class ListSerializer(serializers.ModelSerializer):
	owner_name = serializers.SerializerMethodField()

	class Meta:
		model= Event
		fields=['id','owner_name','title', 'date','time','location', 'seats', 'image']

	def get_owner_name(self, obj):
		return (obj.owner.username)

#############################

class BookingListSerializer(serializers.ModelSerializer):
	event = serializers.SerializerMethodField()
	class Meta:
		model= Booking
		fields = ['event', 'ticket',]

	def get_event(self, obj):
		return (obj.event.title)

################################

class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model= Event
		exclude=['owner']

################################

class UpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model= Event
		fields = [ 'title', 'description', 'location', 'date', 'time', 'seats', 'image']

####################################

class UserSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ["username", "name", "email"]

	def name(self, obj):
		return "%s %s"%(obj.first_name, obj.last_name)

#####################################

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password' , 'first_name' , 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        firstname = validated_data['first_name']
        lastname = validated_data['last_name']
        new_user = User(username=username, first_name=firstname, last_name=lastname)
        new_user.set_password(password)
        new_user.save()
        return validated_data

#####################################

class DetailSerializer(serializers.ModelSerializer):
	owner = serializers.SerializerMethodField()
	booking = serializers.HyperlinkedIdentityField(
		view_name = "book-event-api",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)
	class Meta:
		model = Event
		fields = ["title", "owner", "description", "location", "date", "time",
		"seats", "booking",]
	def get_owner(self, obj):
		return "%s"%(obj.owner.username)

##################################################

class OwnerDetailSerializer(serializers.ModelSerializer):

	owner = serializers.SerializerMethodField()
	attendees = serializers.SerializerMethodField()

	booking = serializers.HyperlinkedIdentityField(
		view_name = "book-event-api",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)
	class Meta:
		model = Event
		fields = ["title", "owner", "description", "location", "date", "time",
		"seats", "booking", "attendees",]

	def get_owner(self, obj):
		return "%s"%(obj.owner.username)

	def get_attendees(self, obj):
		bookings = obj.bookings.all()
		print ("Bookings: ", bookings)
		return BookingDetailsSerializer(bookings, many=True).data

#################################################

class BookingDetailsSerializer(serializers.ModelSerializer):
	owner = serializers.SerializerMethodField()
	class Meta:
		model = Booking
		fields = ["owner", "ticket",]

	def get_owner(self, obj):
		return "%s"%(obj.owner)

###################################################

class AttendSerializer(serializers.ModelSerializer):
    attendee = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['attendee', 'event_name']

    def get_attendee(self,obj):
        return obj.owner.username

    def get_event_name(self,obj):
        return obj.event.title
