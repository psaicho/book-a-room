from django.urls import path, re_path
from book_a_room import views


urlpatterns = [
    path('room/<int:id>/', views.RoomDetails.as_view(), name='room_details'),
    path('room/new/', views.AddRoom.as_view(), name='add_room'),
    path('rooms/', views.AllRooms.as_view(), name='rooms'),
    path('room/delete/<int:id>/', views.DeleteRoom.as_view(), name='delete_room'),
    re_path(r'room/modify/(?P<id>[0-9]+)/', views.ModifyRoom.as_view(), name='modify_room'),
    path('room/reserve/<int:id>/', views.ReserveRomm.as_view(), name='reserve_room'),
    path('room/search-results/', views.SearchResults.as_view(), name='search_results'),


]