from django.urls import path
from .views import ( EventList, EventDetails,)

urlpatterns = [
    #path('register/', Register.as_view(), name="register"),
    #path('login/', TokenObtainPairView.as_view(), name="login"),

    path('events/', EventList.as_view(), name="event-list"),
    path('event/<int:event_id>/details/', EventDetails.as_view(), name="event-detail"),
]
