# views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from elevator_api.serializers import *
from elevator_api.models import Elevator, ElevatorRequest
from rest_framework.decorators import action
from datetime import datetime
from django.utils import timezone


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
            total_existing_elevators = Elevator.objects.all().count()
            elevators = []

            for i in range(num_elevators):
                elevator = Elevator(
                    name=f"Elevator {total_existing_elevators + i + 1} | Elevator System {name} |Created at {current_datetime}"
                )
                elevator.save()
                elevators.append(elevator)

            # Create an ElevatorSystem instance
            name = str(name) + f" | Created at {current_datetime}"
            elevator_system = ElevatorSystem.objects.create(name=name)

            # Create and associate floor instances
            floors = []
            for floor_number in range(floor_numbers):
                floor = Floor.objects.create(floor_number=floor_number)
                floors.append(floor)

            elevator_system.floors.set(floors)
            elevator_system.elevators.set(elevators)

            all_elevators = Elevator.objects.all()
            elevator_serializer = ElevatorSerialzer(elevators, many=True)

            return Response(
                {
                    'message': f'{num_elevators} elevators have been initialized on floor 0 and associated with the elevator system: {elevator_system} with {floor_numbers} floors.',
                    'elevators': elevator_serializer.data,
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
            elevator = integer_serializer.validated_data.get('elevator_id')
            all_pending_requests = ElevatorRequest.objects.filter(elevator=elevator)
            if all_pending_requests:
                pending_requests_serializer_data = PendingRequestsSerializer(
                    all_pending_requests, many=True
                )
                return Response(pending_requests_serializer_data.data)
            else:
                return Response(
                    {'error': "No Completed/Pending requests found for this elevator"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(integer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serialized_data = CreateRequestSerializer(data=request.data)
        if serialized_data.is_valid():
            elevator_id = serialized_data.validated_data.get('elevator_id')
            from_floor = serialized_data.validated_data.get('from_floor')
            destination_floor = serialized_data.validated_data.get('destination_floor')
            elevator_system = serialized_data.validated_data.get('elevator_system')
            elevator_request = ElevatorRequest(
                elevator=Elevator.objects.get(id=elevator_id),
                from_floor=Floor.objects.get(
                    floor_number=from_floor - 1, elevatorsystem=elevator_system
                ),
                destination_floor=Floor.objects.get(
                    floor_number=destination_floor - 1, elevatorsystem=elevator_system
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
            elevator_id = serializer.validated_data.get('elevator_id')
            door_open_close_request = serializer.validated_data.get('door_open_close_request')
            get_elevator = Elevator.objects.get(id=elevator_id)
            if get_elevator.operational:
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
                return Response("Elevator is under maintenance", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElevatorMaintenanceToggle(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        serializer = DoorMaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            elevator_id = serializer.validated_data.get('elevator_id')
            door_maintenance_request = serializer.validated_data.get('door_maintenance_request')
            get_elevator = Elevator.objects.get(id=elevator_id)
            if get_elevator.operational == True and door_maintenance_request == False:
                return Response("Elevator already operational", status=status.HTTP_200_OK)
            elif get_elevator.operational == False and door_maintenance_request == True:
                return Response("Door already under maintenance", status=status.HTTP_200_OK)
            else:
                get_elevator.operational = not door_maintenance_request
                get_elevator.save()
                return Response(
                    ElevatorSerialzer(get_elevator, many=False).data, status=status.HTTP_200_OK
                )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import F, Case, When, Value, BooleanField
from django.db.models import Sum, ExpressionWrapper, FloatField
from django.db.models.functions import Sign


class FetchNextDestinationFloor(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request):
        serializer = ElevatorIDSerializer(data=request.data)
        if serializer.is_valid():
            elevator_id = serializer.validated_data.get('elevator_id')
            fetch_all_requests = (
                ElevatorRequest.objects.filter(elevator__id=elevator_id, completed=False)
                .annotate(
                    direction=Case(  # marking true for up and false for down movement of elevator
                        When(from_floor__lt=F('destination_floor'), then=True),
                        default=False,
                        output_field=BooleanField(),
                    )
                )
                .order_by('timestamp')
            )
            # select initial flow#
            if fetch_all_requests:
                intial_flow = fetch_all_requests.first().direction
                elevator_flow = []
                split_up = fetch_all_requests.filter(direction=True)
                split_down = fetch_all_requests.filter(direction=False)
                split_up_list = []
                split_down_list = []

                if intial_flow:
                    for i in split_up:
                        split_up_list.append(i.from_floor.floor_number + 1)
                        split_up_list.append(i.destination_floor.floor_number + 1)
                    split_up_list = list(set(split_up_list))
                    for i in split_down:
                        split_down_list.append(i.from_floor.floor_number + 1)
                        split_down_list.append(i.destination_floor.floor_number + 1)
                    split_down_list = list(set(split_down_list))
                    elevator_flow = sorted(split_up_list) + sorted(split_down_list, reverse=True)
                else:
                    for i in split_down:
                        split_down_list.append(i.from_floor)
                        split_down_list.append(i.destination_floor)
                    split_down_list = list(set(split_down_list))
                    for i in split_up:
                        split_up_list.append(i.from_floor)
                        split_up_list.append(i.destination_floor)
                    split_up_list = list(set(split_up_list))
                    elevator_flow = sorted(split_down_list, reverse=True), sorted(split_up_list)

                return Response(
                    {
                        'next_destination_floor': elevator_flow[0]
                        if elevator_flow[0] != Elevator.objects.get(id=elevator_id).current_floor
                        else elevator_flow[1],
                        'elevator_flow_path': elevator_flow,
                    }
                )
            else:
                return Response('No available requests for this elevator')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
