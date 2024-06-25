import pytz
import math
from django.db.transaction import atomic
from datetime import time, datetime, UTC, timedelta
from rest_framework import serializers
from collections import defaultdict
from apps.room.models import Tag, Room, Booking, generate_time_slots
from rest_framework.exceptions import ValidationError, NotAcceptable, NotFound

timeslots = generate_time_slots(
    Booking.ROOM_BOOKING_START_TIME,
    Booking.ROOM_BOOKING_END_TIME,
    Booking.SLOT_DURATION
)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class RoomSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'seat_capacity', 'availability', 'tags')

    def get_availability(self, obj: Room) -> str:
        timezone = pytz.timezone('Asia/Kolkata')
        today = datetime.now(timezone).date()
        bookings = Booking.objects.filter(
            room=obj, start_time__date__gte=today, end_time__date__lte=today,
        ).order_by('end_time')
        total_bookings = len(bookings)

        availability: str = ''
        if total_bookings == 0:
            availability = 'currently available'
        elif total_bookings == len(timeslots):
            # total bookings are equals to all slots in
            availability = 'available at tomorrow'
        else:
            curr_time = datetime.combine(
                today, datetime.now(timezone).time()
            ).replace(tzinfo=timezone)

            for b in bookings:
                etime: time = b.end_time.astimezone(timezone)
                if etime >= curr_time:
                    diff: timedelta = (etime - curr_time)
                    minutes = int(math.ceil(round(diff.seconds / 60, 2)))
                    availability = f'available after {minutes} minutes'
                    break

        return availability


class BookingListSeializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "id",
            "slot",
            "start_time",
            "end_time",
        )


class RoomDetailSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    bookings = BookingListSeializer(many=True, read_only=True)
    daywise_bookings = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'seat_capacity', 'tags', 'bookings', 'daywise_bookings')

    def get_daywise_bookings(self, obj: Room):
        bookings_dict = defaultdict(list)

        for b in Booking.objects.filter(room=obj):
            d = b.start_time.date().strftime('%Y-%m-%d')
            bookings_dict[d].append(b.slot)

        bookings = []
        for d in bookings_dict:
            bookings.append({"slots": bookings_dict[d], "date": d})

        return bookings


class AddBookingSerializer(serializers.Serializer):

    room_id = serializers.IntegerField()
    date = serializers.DateField()
    timezone = serializers.CharField()
    slots = serializers.ListField(child=serializers.ChoiceField(choices=timeslots, required=True), required=True)

    def validate(self, attrs):
        r = super().validate(attrs)
        tz = r["timezone"]

        if not len(r['slots']):
            raise ValidationError(detail="At least single slot is required")

        try:
            pytz.timezone(tz)
            r["room"] = Room.objects.get(id=r['room_id'])
        except pytz.exceptions.UnknownTimeZoneError as _:
            raise ValidationError(detail="invalid timezone")
        except Room.DoesNotExist as _:
            raise NotFound(detail="Room not found with given room_id")

        return r

    def create(self, validated_data):
        room = validated_data["room"]
        booking_date: datetime = validated_data["date"]
        timezone = pytz.timezone(validated_data['timezone'])

        with atomic():
            for s in validated_data["slots"]:
                stime_str, etime_str = s.split("~")
                stime: time = datetime.strptime(stime_str, "%H:%M").time()
                etime: time = datetime.strptime(etime_str, "%H:%M").time()
                start_time: datetime = datetime.combine(booking_date, stime).replace(tzinfo=timezone)
                end_time: datetime = datetime.combine(booking_date, etime).replace(tzinfo=timezone)

                booking_exists = Booking.objects.filter(
                    room=room,
                    start_time=start_time,
                    end_time=end_time,
                    slot=s
                ).exists()
                if booking_exists:
                    raise NotAcceptable(detail=f"Booking already exists for slot: {s}")

                Booking.objects.create(
                    room=room,
                    start_time=start_time.astimezone(pytz.UTC),
                    end_time=end_time.astimezone(pytz.UTC),
                    slot=s
                )

        return validated_data
