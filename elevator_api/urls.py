# urls.py
from django.urls import path, include
from .views import (
    ElevatorInitializationView,
    ElevatorRequestsView,
    ElevatorDoorOpenClose,
    ElevatorMaintenanceToggle,
    FetchNextDestinationFloor,
)

urlpatterns = [
    path(
        'initialize-elevator-system/',
        ElevatorInitializationView.as_view(),
        name='initialize-elevator-system',
    ),
    path('elevator-requests/', ElevatorRequestsView.as_view(), name='elevator-requests'),
    path('toggle-door/', ElevatorDoorOpenClose.as_view(), name='toogle-door'),
    path('toggle-maintenance/', ElevatorMaintenanceToggle.as_view(), name='toogle-maintenance'),
    path('next-destination/', FetchNextDestinationFloor.as_view(), name='next-destination'),
]
