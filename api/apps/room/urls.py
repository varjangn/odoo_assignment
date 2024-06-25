
from django.urls import path
from apps.room.views import RoomListView, RoomDetailView, AddBookingView


urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('add-booking/', AddBookingView.as_view(), name='add-booking'),
]