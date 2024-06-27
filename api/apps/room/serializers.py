import pytz
import math
from django.db.transaction import atomic
from datetime import time, datetime, timedelta
from rest_framework import serializers
from collections import defaultdict
from apps.room.models import Tag, Room, Booking, generate_time_slots
from rest_framework.exceptions import ValidationError, NotAcceptable, NotFound


TIMESLOTS = generate_time_slots(
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

        if total_bookings == 0:
            return 'currently available'
        elif total_bookings == len(TIMESLOTS):
            # total bookings are equals to all slots in
            return 'available at tomorrow'

        curr_time = datetime.combine(
            today, datetime.now(timezone).time()
        ).replace(tzinfo=timezone)

        minutes = 0
        prev_end_time = None
        for b in bookings:
            etime: time = b.end_time.astimezone(timezone)
            if etime < curr_time:
                continue

            if prev_end_time is not None:
                max_diff: timedelta = (etime - prev_end_time)
                max_diff_mins = int(math.ceil(round(max_diff.seconds / 60, 2)))
                if max_diff_mins <= 30:
                    minutes += max_diff_mins
                else:
                    break
            else:
                diff: timedelta = (etime - curr_time)
                diff_mins = int(math.ceil(round(diff.seconds / 60, 2)))
                minutes += diff_mins

            prev_end_time = etime

        if minutes <= 0:
            return 'currently available'
        elif minutes > 60:
            day_end_time = TIMESLOTS[-1][0].split("~")[-1]

            end_time_dt = datetime.combine(
                today, datetime.strptime(day_end_time, '%H:%M'
            ).time()).replace(tzinfo=timezone)

            day_diff:timedelta = (end_time_dt - curr_time)
            day_diff_mins = int(math.ceil(round(day_diff.seconds / 60, 2)))
            if minutes >= day_diff_mins:
                # all remaining slots are booked
                return 'available at tomorrow'
            else:
                hours = minutes // 60
                minutes = minutes % 60
                return f'available after {hours} hour and {minutes} minutes'
        else:
            return f'available after {minutes} minutes'




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
    # bookings = BookingListSeializer(many=True, read_only=True)
    daywise_bookings = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            'id',
            'name',
            'seat_capacity',
            'tags',
            'daywise_bookings',
            # 'bookings',
        )

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
    slots = serializers.ListField(child=serializers.ChoiceField(choices=TIMESLOTS, required=True), required=True)

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

                stime_utc = start_time.astimezone(pytz.UTC)
                etime_utc = end_time.astimezone(pytz.UTC)
                Booking.objects.create(
                    room=room,
                    start_time=stime_utc,
                    end_time=etime_utc,
                    slot=s
                )

        return validated_data


class TagIdsSerializer(serializers.Serializer):

    tag_ids = serializers.ListField(child=serializers.IntegerField())
