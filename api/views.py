from datetime import datetime
from django.contrib.auth.models import User


from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .serializers import ListSerializer,DetailSerializer

from events.models import Booking, Event

class EventList(ListAPIView):
	queryset = Event.objects.all()
	serializer_class = ListSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['owner__username']

	def get_queryset(self):
		today = datetime.today()
		return Event.objects.filter(date__gte=today)

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
			return NormalDetailsSerializer
