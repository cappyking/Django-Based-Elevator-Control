from django.db import models


class ElevatorSystem(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Elevator(models.Model):
    STATUS_CHOICES = (
        ('stopped', 'Stopped'),
        ('moving_up', 'Moving Up'),
        ('moving_down', 'Moving Down'),
        ('maintenance', 'Maintenance'),
    )

    name = models.CharField(max_length=100)
    current_floor = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='stopped')
    operational = models.BooleanField(default=True)
    door_open = models.BooleanField(default=False)
    elevator_number = models.PositiveIntegerField(null=True)
    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Floor(models.Model):
    floor_number = models.PositiveIntegerField()
    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Floor {self.floor_number}"


class ElevatorRequest(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    destination_floor = models.ForeignKey(
        Floor, on_delete=models.CASCADE, related_name='requests_to'
    )
    from_floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='requests_from')
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Request for {self.elevator} from {self.from_floor} to {self.destination_floor}"
