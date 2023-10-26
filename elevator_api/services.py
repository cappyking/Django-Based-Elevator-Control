from django.db.models import F, Case, When, BooleanField
from elevator_api.models import Elevator, ElevatorRequest


def fetch_all_incomplete_requests_for_elevator(elevator_system, elevator_number):
    fetch_all_requests = (
        ElevatorRequest.objects.filter(
            elevator__elevatorsystem=elevator_system,
            elevator__elevator_number=elevator_number,
            completed=False,
        )
        .annotate(
            direction=Case(  # marking true for up and false for down movement of elevator
                When(from_floor__lt=F('destination_floor'), then=True),
                default=False,
                output_field=BooleanField(),
            )
        )
        .order_by('timestamp')
    )
    return fetch_all_requests


def get_elevator_flow(elevator_system, elevator_number):
    # common query function to fetch all pending requests based on elevator_id
    fetch_all_requests = fetch_all_incomplete_requests_for_elevator(
        elevator_system, elevator_number
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
                split_up_list.append(i.from_floor.floor_number)
                split_up_list.append(i.destination_floor.floor_number)
            split_up_list = list(set(split_up_list))
            for i in split_down:
                split_down_list.append(i.from_floor.floor_number)
                split_down_list.append(i.destination_floor.floor_number)
            split_down_list = list(set(split_down_list))
            elevator_flow = sorted(split_up_list) + sorted(split_down_list, reverse=True)
        else:
            for i in split_down:
                split_down_list.append(i.from_floor.floor_number)
                split_down_list.append(i.destination_floor.floor_number)
            split_down_list = list(set(split_down_list))
            for i in split_up:
                split_up_list.append(i.from_floor.floor_number)
                split_up_list.append(i.destination_floor.floor_number)
            split_up_list = list(set(split_up_list))
            elevator_flow = sorted(split_down_list, reverse=True), sorted(split_up_list)
        return elevator_flow
    else:
        return False


def check_if_elevator_is_under_maintenance(elevator_system, elevator_number):
    if Elevator.objects.get(
        elevator_number=elevator_number, elevatorsystem=elevator_system
    ).operational:
        return False
    else:
        return True
