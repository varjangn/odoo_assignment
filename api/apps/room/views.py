from apps.room.serializers import RoomSerializer, RoomDetailSerializer, AddBookingSerializer, TagIdsSerializer
from apps.room.models import Room, Tag
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound


class RoomListView(ListAPIView):
    queryset = Room.objects.all().order_by()
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter]
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    search_fields = ['name', 'tags__name']


class RoomDetailView(RetrieveAPIView):

    queryset = Room.objects.all().order_by()
    serializer_class = RoomDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


class RoomRemoveTagsView(CreateAPIView):

    serializer_class = TagIdsSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag_ids = serializer.data.get("tag_ids")

        room_id = kwargs['pk']
        room: Room = Room.objects.filter(id=room_id).first()
        if room is None:
            raise NotFound(detail="Room not found with given room id")

        for tag in Tag.objects.filter(id__in=tag_ids):
            room.tags.remove(tag)

        return Response({"success": True})


class AddBookingView(CreateAPIView):

    serializer_class = AddBookingSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

