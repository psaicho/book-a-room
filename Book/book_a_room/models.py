from django.db import models


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector_availability = models.BooleanField(default=False)


class RoomReservation(models.Model):
    date = models.DateField(null=False)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_id')
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('date', 'room_id',)
