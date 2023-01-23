from book_a_room.models import Room
from datetime import datetime
from django.shortcuts import render
def rooms_processor(request):
    rooms = Room.objects.all().order_by('id')
    rooms.capacity_max = Room.objects.all().order_by('-capacity')[0].capacity

    return {
        'crooms': rooms,
        'today': datetime.today().strftime("%Y-%m-%d"),
    }


