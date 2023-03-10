from datetime import date, datetime

from book_a_room.models import Room, RoomReservation
from django import views
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
class AddRoom(views.View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(
            request,
            'add_room.html',
            context={'room': room}
        )

    def post(self, request):
        # get value from form
        name = str(request.POST.get('name'))
        capacity = request.POST.get('capacity')
        projector_a = True if request.POST.get('projector_a') == 'on' else False

        # change the letter size in name variable
        print(type(name))

        # validation
        if name != '' and capacity.isnumeric():
            info = 'Romm has been added to the dataBase'
            name = name.title()
            # Add room to the DataBase
            Room.objects.update_or_create(
                name=name,
                defaults={'name': name, 'capacity': capacity, 'projector_availability': projector_a},
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
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = date.today() in reservation_dates
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


def room_by_id(id: int):
    room = Room.objects.get(id=id)
    room.reservation_gt_today \
        = [reservation.date for reservation in
           room.roomreservation_set.filter(date__gt=date.today()).order_by('date')]
    return room


class RoomDetails(views.View):
    def get(self, request, id):
        # room = Room.objects.get(id=id)
        # room.reservation_gt_today \
        #     = [reservation.date for reservation in
        #        room.roomreservation_set.filter(date__gt=date.today())]
        return render(
            request,
            'room.html',
            context={'room': room_by_id(id)}
        )


class ReserveRomm(views.View):
    def get(self, request, id):
        return render(
            request,
            'reserve_room.html',
            context={'room': room_by_id(id)}
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


class SearchResults(views.View):
    def get(self, request):
        date = request.GET.get('search_date')
        print(date)

        projector = True if request.GET.get('search_projector') == 'on' else False
        id = request.GET.get('search_id')
        capacity = request.GET.get('search_capacity')
        print(RoomReservation.objects.filter(date=date).values_list('id'))
        rooms = Room.objects.filter(
                                    (Q(capacity__gt=capacity)
                                     and Q(projector_availability=projector))
                                    ).exclude(id__in=RoomReservation.objects.filter(date=date).values_list('room_id'))
        return render(
            request,
            'search_result.html',
            context={'rooms': rooms}
        )
