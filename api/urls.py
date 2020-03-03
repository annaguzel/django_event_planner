from django.urls import path
from api import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="apilogin"),

    path('register/', views.Register.as_view(), name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),


	path('ownerlist/<str:owner_username>', views.OwnerEventList.as_view(), name='owner-list'),

    path('bookedlist/', views.BookedEventsList.as_view(), name='user-booking-list'),
	path('create/', views.CreateEvent.as_view(), name='create-event-api'),

    path('<int:event_id>/update/', views.UpdateEvent.as_view(), name='update-event-api'),

    path('<int:event_id>/book/', views.BookEvent.as_view(), name='book-event-api'),

    path('event/<int:event_id>/detail/',views.EventDetails.as_view(), name="event-detail-api")
	]
