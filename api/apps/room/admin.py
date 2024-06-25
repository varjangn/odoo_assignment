from django.contrib import admin
from apps.room.models import Room, Tag, Booking


class TagAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = ('name',)


class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "seat_capacity"
    )
    search_fields = ('name',)


class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "room",
        "slot",
        "start_time",
        "end_time",
    )


admin.site.register(Room, RoomAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Booking, BookingAdmin)
