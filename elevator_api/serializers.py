# serializers.py
from rest_framework import serializers
from .models import *


class ElevatorInitializationSerializer(serializers.Serializer):
    num_elevators = serializers.IntegerField()
    name = serializers.CharField()
    floors = serializers.IntegerField()


class ElevatorIDSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField()
    elevator_system = serializers.IntegerField()

    def validate(self, data):
        elevator_number = data.get('elevator_number')
        elevator_system = data.get('elevator_system')

        try:
            elevator = Elevator.objects.get(
                elevator_number=elevator_number, elevatorsystem=elevator_system
            )
        except Elevator.DoesNotExist:
            raise serializers.ValidationError(
                "Elevator Number is either invalid or not associated with this Elevator System"
            )

        return data


class ElevatorSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'


class PendingRequestsSerializer(serializers.ModelSerializer):
    elevator_number = serializers.ReadOnlyField(source='elevator.elevator_number')
    from_floor_number = serializers.ReadOnlyField(source='from_floor.floor_number')
    destination_floor_number = serializers.ReadOnlyField(source='destination_floor.floor_number')

    class Meta:
        model = ElevatorRequest
        fields = [
            'elevator_number',
            'from_floor_number',
            'destination_floor_number',
            'timestamp',
            'completed',
        ]


class DoorOpenCloseSerializer(serializers.Serializer):
    door_open = serializers.BooleanField()
    elevator_number = serializers.IntegerField()
    elevator_system = serializers.IntegerField()

    def validate(self, data):
        elevator_number = data.get('elevator_number')
        elevator_system = data.get('elevator_system')

        # Extra validation for managing form-data boolean based input
        if self.initial_data.get('door_open') is None:
            raise serializers.ValidationError("door_open is a mandatory field")

        # Check if the elevator one is trying to reach is valid
        try:
            elevator = Elevator.objects.get(
                elevator_number=elevator_number, elevatorsystem=elevator_system
            )
        except Elevator.DoesNotExist:
            raise serializers.ValidationError(
                "Elevator Number is either invalid or not associated with this Elevator System"
            )

        return data


class ElevatorMaintenanceSerializer(serializers.Serializer):
    elevator_maintenance_request = serializers.BooleanField()
    elevator_number = serializers.IntegerField()
    elevator_system = serializers.IntegerField()

    def validate(self, data):
        validated_data = super().validate(data)
        elevator_number = validated_data.get('elevator_number')
        elevator_system = validated_data.get('elevator_system')

        # Extra validation for managing form-data boolean based input
        if self.initial_data.get('elevator_maintenance_request') is None:
            raise serializers.ValidationError("elevator_maintenance_request is a mandatory field")

        try:
            elevator = Elevator.objects.get(
                elevator_number=elevator_number, elevatorsystem=elevator_system
            )
        except Elevator.DoesNotExist:
            raise serializers.ValidationError(
                "Elevator Number is either invalid or not associated with this Elevator System"
            )
        return validated_data


class CreateRequestSerializer(serializers.Serializer):
    elevator_system = serializers.IntegerField()
    elevator_number = serializers.IntegerField()
    destination_floor = serializers.IntegerField()
    from_floor = serializers.IntegerField()

    def validate(self, data):
        validated_data = super().validate(data)
        elevator_system_id = data.get('elevator_system')
        elevator_number = data.get('elevator_number')
        destination_floor = data.get('destination_floor')
        from_floor = data.get('from_floor')

        try:
            elevator_system = ElevatorSystem.objects.get(id=elevator_system_id)
        except ElevatorSystem.DoesNotExist:
            raise serializers.ValidationError("Invalid Elevator System")

        try:
            elevator = Elevator.objects.get(
                elevatorsystem=elevator_system_id, elevator_number=elevator_number
            )
        except Elevator.DoesNotExist:
            raise serializers.ValidationError(
                "Elevator Number is either invalid or not associated with this Elevator System"
            )

        try:
            # Check if the floor exists within the specified elevator_system
            floor = Floor.objects.get(
                floor_number=destination_floor, elevatorsystem=elevator_system_id
            )
        except Floor.DoesNotExist:
            raise serializers.ValidationError("Invalid Destination Floor")

        try:
            # Check if the floor exists within the specified elevator_system
            floor = Floor.objects.get(floor_number=from_floor, elevatorsystem=elevator_system_id)
        except Floor.DoesNotExist:
            raise serializers.ValidationError("Invalid From Floor")

        return validated_data


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = "__all__"
