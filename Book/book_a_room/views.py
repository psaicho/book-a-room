from book_a_room.models import Room, RoomReservation
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, reverse
from django import views
from django.shortcuts import get_object_or_404
from django.urls import reverse
from datetime import date, datetime



# Create your views here.
class AddRoom(views.View):
    def get(self, request):
        return render(
            request,
            'add_room.html'
        )

    def post(self, request):
        # get value from form
        name = str(request.POST.get('name'))
        capacity = request.POST.get('capacity')
        projector_a = True if request.POST.get('projector_a') == 'on' else False

        #change the letter size in name variable
        print(type(name))

        #validation
        if name != '' and capacity.isnumeric():
            info = 'Romm has been added to the dataBase'
            name = name.title()
            # Add room to the DataBase
            Room.objects.update_or_create(
                name=name,
                defaults={'name': name, 'capacity': capacity, 'projector_availability':projector_a},
            )
            return HttpResponseRedirect(reverse('rooms'))
        else:
            info = 'Fill in the name of the room, the capacity of the room must be greater than 0!'

            return render(
                request,
                'add_room.html',
                context={'info': info}
            )

class AllRooms(views.View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(
            request,
            'rooms.html',
            context={'rooms': rooms}
        )

class DeleteRoom(views.View):

    def get(self, request, id):
        room = Room.objects.get(id=id)
        room.delete()
        return render(
            request,
            'rooms.html',

        )

class ModifyRoom(views.View):
    def get(self, request, id):
        room = get_object_or_404(Room, id=id)
        return render(
            request,
            'modify_room.html',
            context={'room': room}
        )
    def post(self, request, id):
        # get value from form
        name = str(request.POST.get('name'))
        capacity = request.POST.get('capacity')
        projector_a = True if request.POST.get('projector_a') == 'on' else False

        # validation
        if name != '' and capacity.isnumeric():
            # Add room to the DataBase
            room = Room.objects.filter(id=id).update(name=name.title(),
                                                     capacity=capacity,
                                                     projector_availability=projector_a)
        else:
            info = 'Fill in the name of the room, the capacity of the room must be greater than 0!'

        return HttpResponseRedirect(reverse('rooms'))

class ReserveRomm(views.View):

    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(
            request,
            'reserve_room.html',
            context={'room': room}
        )

    def post(self, request, id):
        date_r = request.POST.get('date')
        comment = request.POST.get('comment')
        room = Room.objects.get(id=id)
        if RoomReservation.objects.filter(date=date_r, room_id=room).exists() or \
                date.today().strftime("%Y-%m-%d") > datetime.strptime(date_r, '%Y-%m-%d').strftime("%Y-%m-%d"):
            info = "Sorry, this Conference Room is busy at that date or You entered date from past "
            return render(
                request,
                'reserve_room.html',
                context={'info': info}
            )
        else:
            RoomReservation.objects.create(date=date_r, room_id=room, comment=comment)
            return HttpResponseRedirect(reverse('rooms'))





