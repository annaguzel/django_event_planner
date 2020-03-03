from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from datetime import datetime
from events.models import Event, Booking
from .permissions import IsOwner

# Create your views here.
from .serializers import(
ListSerializer,
BookingListSerializer,
CreateEventSerializer,
UpdateSerializer,
BookingListSerializer,
UserCreateSerializer,
UserSerializer,
DetailSerializer,
OwnerDetailSerializer,
BookingDetailsSerializer,
)
from rest_framework import serializers

##############################

class OwnerEventList(ListAPIView):
	serializer_class = ListSerializer
	filter_backends=[SearchFilter,]
	search_fields=['username']

	def get_queryset(self):
		owner = self.kwargs['owner_username']
		today = datetime.today()
		return Event.objects.filter(owner__username = owner)

###############################

#List of Event A user have booked for

class BookedEventsList(ListAPIView):
	serializer_class = BookingListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		query = Booking.objects.filter(name=self.request.user)
		return query

###############################


class CreateEvent(CreateAPIView):
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(owner=self.request.user)

###############################

class UpdateEvent(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = UpdateSerializer
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'

###############################


##########################################

class EventDetails(RetrieveAPIView):
	queryset = Event.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'

	def get_serializer_class(self):
		print (self.kwargs['event_id'])
		event = Event.objects.get(id=self.kwargs['event_id'])
		if self.request.user == event.owner:
			return OwnerDetailSerializer
		else:
			return DetailSerializer

###############################

class BookEvent(CreateAPIView):
	serializer_class = BookingListSerializer
	# permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(owner=self.request.user, event_id=self.kwargs['event_id'])

###############################

class Register(CreateAPIView):
	serializer_class = UserCreateSerializer

###############################

class Profile(RetrieveAPIView):
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user

################################
