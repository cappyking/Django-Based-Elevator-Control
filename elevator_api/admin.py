from django.contrib import admin
from elevator_api.models import Elevator, Floor, ElevatorRequest, ElevatorSystem


class ElevatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'elevator_system', 'elevator_number', 'operational', 'status')


class FloorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'floor_number',
        'elevator_system',
    )


class ElevatorRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'elevator',
        'from_floor',
        'destination_floor',
        'completed',
    )


class ElevatorSystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Register the models with the custom admin classes
admin.site.register(Elevator, ElevatorAdmin)
admin.site.register(Floor, FloorAdmin)
admin.site.register(ElevatorRequest, ElevatorRequestAdmin)
admin.site.register(ElevatorSystem, ElevatorSystemAdmin)
