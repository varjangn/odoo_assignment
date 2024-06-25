from django.db import models
from datetime import time, datetime, timedelta


def generate_time_slots(start_time, end_time, slot_duration):
    slots = []
    current_time = start_time
    while current_time < end_time:
        slot_end_time = (datetime.combine(datetime.today(), current_time) + slot_duration).time()
        slots.append((f"{current_time.strftime('%H:%M')}~{slot_end_time.strftime('%H:%M')}", f"{current_time.strftime('%H:%M')} - {slot_end_time.strftime('%H:%M')}"))
        current_time = slot_end_time
    return slots


class TimestampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(TimestampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Room(TimestampedModel):
    name = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()

    tags = models.ManyToManyField(Tag, related_name='rooms', blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    ROOM_BOOKING_START_TIME = time(10, 0)  # 10:00 AM
    ROOM_BOOKING_END_TIME = time(19, 0)    # 7:00 PM
    SLOT_DURATION = timedelta(minutes=30)
    SLOT_CHOICES = generate_time_slots(ROOM_BOOKING_START_TIME, ROOM_BOOKING_END_TIME, SLOT_DURATION)

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    slot = models.CharField(max_length=20, choices=SLOT_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Booking for {self.room.name} in slot {self.slot}"
