from datetime import date

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):		# naming
	message="You must be the Event's Organizer"

	def has_object_permission(self,request,view,obj):
		if request.user == obj.owner:
			return True
		else:
			return False
