from apps.room.serializers import RoomSerializer, RoomDetailSerializer, AddBookingSerializer
from apps.room.models import Room
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


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


class AddBookingView(CreateAPIView):

    serializer_class = AddBookingSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

