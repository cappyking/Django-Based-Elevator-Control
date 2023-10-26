from django.db.models import F, Case, When, BooleanField
from elevator_api.models import Elevator, ElevatorRequest


def fetch_all_incomplete_requests_for_elevator(elevator_system, elevator_number):
    fetch_all_requests = (
        ElevatorRequest.objects.filter(
            elevator__elevator_system__id=elevator_system,
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


# This function removes consecutive duplicates while calculating the elevator flow.
# If there is a pickup at 3 then drop at 1, followed by another pickup at 1 and
# then drop at 5, it should result in a floor list flow of [3, 1, 5], not
# [3, 1, 1, 5], since pickup and drop can happen together.


def remove_consecutive_duplicates(input_list):
    output_list = [input_list[0]]
    print(output_list)
    for i in range(1, len(input_list)):
        if input_list[i] != input_list[i - 1]:
            output_list.append(input_list[i])
    return output_list


def get_elevator_flow(elevator_system, elevator_number):
    # common query function to fetch all pending requests based on elevator_id
    fetch_all_requests = fetch_all_incomplete_requests_for_elevator(
        elevator_system, elevator_number
    )

    # select initial flow direction
    if fetch_all_requests:
        intial_flow = fetch_all_requests.first().direction
        elevator_flow = []
        split_up = fetch_all_requests.filter(direction=True)
        split_down = fetch_all_requests.filter(direction=False)
        split_up_list = []
        split_down_list = []
        print(fetch_all_requests)
        # Calculate elevator flow for upward movement.
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
        # Calculate elevator flow for downward movement.
        else:
            for i in split_down:
                split_down_list.append(i.from_floor.floor_number)
                split_down_list.append(i.destination_floor.floor_number)
            split_down_list = list(set(split_down_list))
            for i in split_up:
                split_up_list.append(i.from_floor.floor_number)
                split_up_list.append(i.destination_floor.floor_number)
            split_up_list = list(set(split_up_list))
            elevator_flow = sorted(split_down_list, reverse=True) + sorted(split_up_list)
        return remove_consecutive_duplicates(elevator_flow)
    else:
        return False


def check_if_elevator_is_under_maintenance(elevator_system, elevator_number):
    if Elevator.objects.get(
        elevator_number=elevator_number, elevator_system__id=elevator_system
    ).operational:
        return False
    else:
        return True
