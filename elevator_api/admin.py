from django.contrib import admin
from elevator_api.models import Elevator, Floor, ElevatorRequest, ElevatorSystem

admin.site.register(Elevator)
admin.site.register(Floor)
admin.site.register(ElevatorRequest)
admin.site.register(ElevatorSystem)
