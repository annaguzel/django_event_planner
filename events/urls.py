from django.urls import path
from .views import (Login, Logout, Signup)
from events import views

urlpatterns = [

    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('', views.home, name='home'),
    path('event/create/', views.create , name='create'),
    path('dashboard/', views.dashboard , name='dashboard'),
	path('event/<int:event_id>/edit/', views.edit_event , name='edit-event'),
    path('event/<int:event_id>/detail/',views.event_detail, name='event-details'),
    path('event/<int:event_id>/book/',views.event_book, name='event-book'),



]
