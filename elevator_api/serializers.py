# serializers.py
from rest_framework import serializers
from .models import *


class ElevatorInitializationSerializer(serializers.Serializer):
    num_elevators = serializers.IntegerField()
    name = serializers.CharField()
    floors = serializers.IntegerField()


class ElevatorIDSerializer(serializers.Serializer):
    elevator_id = serializers.IntegerField()

    def validate_elevator_id(self, value):
        try:
            elevator = Elevator.objects.get(id=value)
        except Elevator.DoesNotExist:
            raise serializers.ValidationError("Invalid Elevator ID")
        return value


class ElevatorSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'


class PendingRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = '__all__'


class DoorOpenCloseSerializer(serializers.Serializer):
    door_open_close_request = serializers.BooleanField()
    elevator_id = serializers.IntegerField()

    def validate_elevator_system(self, value):
        try:
            elevator_system = ElevatorSystem.objects.get(id=value)
        except ElevatorSystem.DoesNotExist:
            raise serializers.ValidationError("Invalid Elevator System ID")
        return value


class DoorMaintenanceSerializer(serializers.Serializer):
    door_maintenance_request = serializers.BooleanField()
    elevator_id = serializers.IntegerField()

    def validate_elevator_system(self, value):
        try:
            elevator_system = ElevatorSystem.objects.get(id=value)
        except ElevatorSystem.DoesNotExist:
            raise serializers.ValidationError("Invalid Elevator System ID")
        return value


class CreateRequestSerializer(serializers.Serializer):
    elevator_system = serializers.IntegerField()
    elevator_id = serializers.IntegerField()
    destination_floor = serializers.IntegerField()
    from_floor = serializers.IntegerField()

    def validate_elevator_system(self, value):
        try:
            elevator_system = ElevatorSystem.objects.get(id=value)
        except ElevatorSystem.DoesNotExist:
            raise serializers.ValidationError("Invalid Elevator System")
        return value

    def validate_elevator_id(self, value):
        try:
            elevator = Elevator.objects.get(id=value)
        except Elevator.DoesNotExist:
            raise serializers.ValidationError("Invalid Elevator ID")
        return value

    def validate_destination_floor(self, value):
        elevator_system_id = self.initial_data.get('elevator_system')
        try:
            # Check if the floor exists within the specified elevator_system
            floor = Floor.objects.get(floor_number=value - 1, elevatorsystem=elevator_system_id)
        except Floor.DoesNotExist:
            raise serializers.ValidationError("Invalid Destination Floor")
        return value

    def validate_from_floor(self, value):
        elevator_system_id = self.initial_data.get('elevator_system')
        try:
            # Check if the floor exists within the specified elevator_system
            floor = Floor.objects.get(floor_number=value - 1, elevatorsystem=elevator_system_id)
        except Floor.DoesNotExist:
            raise serializers.ValidationError("Invalid From Floor")
        return value
