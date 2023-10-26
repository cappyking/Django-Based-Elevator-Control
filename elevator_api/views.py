# views.py
from datetime import datetime
from django.utils import timezone

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from elevator_api.models import Elevator, ElevatorRequest
from elevator_api.serializers import *

from elevator_api.services import (
    check_if_elevator_is_under_maintenance,
    fetch_all_incomplete_requests_for_elevator,
    get_elevator_flow,
)


class ElevatorInitializationView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        serializer = ElevatorInitializationSerializer(data=request.data)
        if serializer.is_valid():
            num_elevators = serializer.validated_data.get('num_elevators')
            name = serializer.validated_data.get('name')
            floor_numbers = serializer.validated_data.get('floors')

            # Create 'num_elevators' elevator instances
            current_datetime = datetime.now(timezone.get_current_timezone()).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            elevators = []

            # Create an ElevatorSystem instance
            name = str(name) + f" | Created at {current_datetime}"
            elevator_system = ElevatorSystem.objects.create(name=name)

            for i in range(num_elevators):
                elevator = Elevator(
                    name=f"Elevator {i + 1} | Elevator System {name} |Created at {current_datetime}",
                    elevator_number=i + 1,
                )
                elevator.save()
                elevators.append(elevator)

            # Create and associate floor instances
            floors = []
            for floor_number in range(floor_numbers):
                floor = Floor.objects.create(floor_number=floor_number + 1)
                floors.append(floor)

            elevator_system.floors.set(floors)
            elevator_system.elevators.set(elevators)

            all_elevators = Elevator.objects.all()
            elevator_serializer = ElevatorSerialzer(elevators, many=True)
            floor_serializer = FloorSerializer(floors, many=True)

            return Response(
                {
                    'message': f'{num_elevators} elevators have been initialized on floor 0 and associated with the elevator system: {elevator_system} with {floor_numbers} floors.',
                    'elevators': elevator_serializer.data,
                    "floors": floor_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElevatorRequestsView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request):
        integer_serializer = ElevatorIDSerializer(data=request.data)
        if integer_serializer.is_valid():
            elevator_number = integer_serializer.validated_data.get('elevator_number')
            elevator_system = integer_serializer.validated_data.get('elevator_system')
            current_elevator = Elevator.objects.get(
                elevator_number=elevator_number, elevatorsystem=elevator_system
            )
            all_pending_requests = ElevatorRequest.objects.filter(elevator=current_elevator)
            if not (current_elevator.operational):
                return Response(
                    "Elevator is under maintenance.", status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            if all_pending_requests:
                pending_requests_serializer_data = PendingRequestsSerializer(
                    all_pending_requests, many=True
                )
                return Response(pending_requests_serializer_data.data)
            else:
                return Response(
                    "No Completed/Pending requests found for this elevator",
                    status=status.HTTP_204_NO_CONTENT,
                )
        else:
            return Response(integer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serialized_data = CreateRequestSerializer(data=request.data)
        if serialized_data.is_valid():
            elevator_number = serialized_data.validated_data.get('elevator_number')
            from_floor = serialized_data.validated_data.get('from_floor')
            destination_floor = serialized_data.validated_data.get('destination_floor')
            elevator_system = serialized_data.validated_data.get('elevator_system')
            get_elevator = Elevator.objects.get(
                elevator_number=elevator_number, elevatorsystem=elevator_system
            )
            if not get_elevator.operational:
                return Response(
                    "Elevator is under maintenance", status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            elevator_request = ElevatorRequest(
                elevator=get_elevator,
                from_floor=Floor.objects.get(
                    floor_number=from_floor, elevatorsystem=elevator_system
                ),
                destination_floor=Floor.objects.get(
                    floor_number=destination_floor, elevatorsystem=elevator_system
                ),
            )
            elevator_request.save()
            return Response("Added to queue", status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ElevatorDoorOpenClose(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        serializer = DoorOpenCloseSerializer(data=request.data)
        if serializer.is_valid():
            elevator_number = serializer.validated_data.get('elevator_number')
            elevator_system = serializer.validated_data.get('elevator_system')
            door_open_close_request = serializer.validated_data.get('door_open')
            get_elevator = Elevator.objects.get(
                elevator_number=elevator_number, elevatorsystem=elevator_system
            )
            if not get_elevator.operational:
                return Response(
                    "Elevator is under maintenance", status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            else:
                if get_elevator.door_open == True and door_open_close_request == True:
                    return Response("Door already open", status=status.HTTP_200_OK)
                elif get_elevator.door_open == False and door_open_close_request == False:
                    return Response("Door already closed", status=status.HTTP_200_OK)
                else:
                    get_elevator.door_open = door_open_close_request
                    get_elevator.save()
                    return Response(
                        ElevatorSerialzer(get_elevator, many=False).data, status=status.HTTP_200_OK
                    )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElevatorMaintenanceToggle(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        serializer = ElevatorMaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            elevator_number = serializer.validated_data.get('elevator_number')
            elevator_system = serializer.validated_data.get('elevator_system')
            door_maintenance_request = serializer.validated_data.get('elevator_maintenance_request')
            load_distribution_text = "All pending requests have been marked cancelled since there are marked completed since no other elevator is available within this elevator system to fulfill the requests"
            get_elevator = Elevator.objects.get(
                elevator_number=elevator_number, elevatorsystem=elevator_system
            )
            if get_elevator.operational == True and door_maintenance_request == False:
                return Response("Elevator already operational", status=status.HTTP_200_OK)
            elif get_elevator.operational == False and door_maintenance_request == True:
                return Response("Elevator already under maintenance", status=status.HTTP_200_OK)
            elif get_elevator.operational == True and door_maintenance_request == True:
                get_elevator.operational = not door_maintenance_request
                get_elevator.save()
                # distributing load of the current elevator requests to other elevators if available
                available_elevators = Elevator.objects.filter(
                    elevatorsystem=elevator_system, operational=True
                )
                if available_elevators.count() > 1:
                    requests_to_transfer = ElevatorRequest.objects.filter(
                        elevator__elevatorsystem=elevator_system,
                        elevator__elevator_number=elevator_number,
                    )
                    if requests_to_transfer:
                        counter = 0
                        for req in requests_to_transfer:
                            if counter >= available_elevators.count():
                                counter = 0
                            req.elevator = available_elevators[counter]
                            print(counter, available_elevators.count())
                            counter = counter + 1
                            req.save()
                        load_distribution_text = "All available load for this elevator has been transferred to other operational elevators within the same elevator system."

            else:
                get_elevator.operational = not door_maintenance_request
                get_elevator.save()

            return Response(
                {
                    "note": load_distribution_text,
                    "elevator_status": ElevatorSerialzer(get_elevator, many=False).data,
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FetchNextDestinationFloor(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request):
        serializer = ElevatorIDSerializer(data=request.data)
        if serializer.is_valid():
            elevator_system = serializer.validated_data.get('elevator_system')
            elevator_number = serializer.validated_data.get('elevator_number')
            if check_if_elevator_is_under_maintenance(elevator_system, elevator_number):
                return Response(
                    {'error': "Elevator Under Maintenance"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            elevator_flow = get_elevator_flow(elevator_system, elevator_number)
            if elevator_flow:
                return Response(
                    {
                        'next_destination_floor': elevator_flow[0]
                        if elevator_flow[0]
                        != Elevator.objects.get(
                            elevatorsystem=elevator_system, elevator_number=elevator_number
                        ).current_floor
                        else elevator_flow[1],
                        'elevator_flow_path': elevator_flow,
                    }
                )
            else:
                return Response(
                    'No available requests for this elevator', status=status.HTTP_204_NO_CONTENT
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FetchElevatorDirection(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request):
        serializer = ElevatorIDSerializer(data=request.data)
        if serializer.is_valid():
            elevator_system = serializer.validated_data.get('elevator_system')
            elevator_number = serializer.validated_data.get('elevator_number')
            if check_if_elevator_is_under_maintenance(elevator_system, elevator_number):
                return Response(
                    {'error': "Elevator Under Maintenance"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            all_incomplete_requests = fetch_all_incomplete_requests_for_elevator(
                elevator_system, elevator_number
            )
            if all_incomplete_requests:
                return Response(
                    {
                        'direction': "Upwards"
                        if all_incomplete_requests.first().direction
                        else "Downwards"
                    }
                )
            else:
                return Response(
                    "No direction for the elevator, since the elevator is not moving.",
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
