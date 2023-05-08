from django.shortcuts import render
from django.http import HttpResponse
from http import HTTPStatus
from .models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.core.serializers.json import Serializer, DjangoJSONEncoder

from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def get_attractions(request):
    if request.method == 'GET':
        location = request.GET.get('location')
        category = request.GET.get('category')
        min_price = int(request.GET.get('min_price')) if request.GET.get('min_price') is not None else None
        max_price = int(request.GET.get('max_price')) if request.GET.get('max_price') is not None else None

        # getting all attractions from the database
        attractions = Attraction.objects.all()

        # filtering
        if location is not None:
            attractions = attractions.filter(country=Country.objects.get(name=location).id)
        if category is not None:
            attractions = attractions.filter(category=Category.objects.get(name=category).id)
        if min_price is not None:
            attractions = attractions.filter(price__gte=int(min_price))
        if max_price is not None:
            attractions = attractions.filter(price__lte=int(max_price))

        # Serialize the records to JSON
        attractions_json = serializers.serialize('json',
                                                 attractions,
                                                 use_natural_foreign_keys=True,
                                                 use_natural_primary_keys=True)

        # remove the pk and model keys
        data = json.loads(attractions_json)
        for d in data:
            del d['pk']
            del d['model']

        attractions_json = json.dumps(data)

        return HttpResponse(attractions_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_tours(request):
    if request.method == 'GET':
        location = request.GET.get('location')
        min_price = int(request.GET.get('min_price')) if request.GET.get('min_price') is not None else None
        max_price = int(request.GET.get('max_price')) if request.GET.get('max_price') is not None else None
        duration_max = int(request.GET.get('duration_max')) if request.GET.get('duration_max') is not None else None
        attractions_no_max = int(request.GET.get('attractions_no_max')) if request.GET.get(
            'attractions_no_max') is not None else None

        # getting all attractions from the database
        tours = Tour.objects.all()

        # filtering
        if location is not None:
            tours = tours.filter(country=Country.objects.get(name=location).id)
        if duration_max is not None:
            tours = tours.filter(duration__lte=duration_max)
        if min_price is not None:
            tours = tours.filter(price__gte=min_price)
        if max_price is not None:
            tours = tours.filter(price__lte=max_price)
        if attractions_no_max is not None:
            tours = tours.filter(price__lte=attractions_no_max)

        # Serialize the records to JSON
        tours_json = serializers.serialize('json',
                                           tours,
                                           use_natural_foreign_keys=True,
                                           use_natural_primary_keys=True)

        # remove the pk and model keys
        data = json.loads(tours_json)
        for d in data:
            del d['pk']
            del d['model']

        tours_json = json.dumps(data)

        return HttpResponse(tours_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_categories(request):
    if request.method == 'GET':

        categories = Category.objects.all()

        # Serialize the records to JSON
        categories_json = serializers.serialize('json',
                                                categories,
                                                use_natural_foreign_keys=True,
                                                use_natural_primary_keys=True)

        # remove the pk and model keys
        data = json.loads(categories_json)
        for d in data:
            del d['model']

        categories_json = json.dumps(data)

        return HttpResponse(categories_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_discounts(request):
    if request.method == 'GET':

        discounts = Discount.objects.all()

        # Serialize the records to JSON
        discounts_json = serializers.serialize('json',
                                               discounts,
                                               use_natural_foreign_keys=True,
                                               use_natural_primary_keys=True)

        # remove the pk and model keys
        data = json.loads(discounts_json)
        for d in data:
            del d['model']

        discounts_json = json.dumps(data)

        return HttpResponse(discounts_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_countries(request):
    if request.method == 'GET':

        countries = Country.objects.all()

        # Serialize the records to JSON
        countries_json = serializers.serialize('json',
                                               countries,
                                               use_natural_foreign_keys=True,
                                               use_natural_primary_keys=True)

        # remove the pk and model keys
        data = json.loads(countries_json)
        for d in data:
            del d['model']

        countries_json = json.dumps(data)

        return HttpResponse(countries_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def book(request):
    if request.method == 'POST':
        tour_attraction_id = request.GET.get('tour_attraction_id')
        psp_id = request.GET.get('psp_id')
        psp_checkout_id = request.GET.get('psp_checkout_id')
        start_date = request.GET.get('start_date')
        adults_no = request.GET.get('adults_no')
        kids_no = request.GET.get('kids_no')
        seniors_no = request.GET.get('seniors_no')

        # checking if any of the required parameters is NoneType
        # if len([x for x in [tour_attraction_id, psp_id, psp_checkout_id, start_date] if x is None]) > 0:
        #     return HttpResponse(status=400)

        # parsing tour_attraction_id (if starts then 'T'-tour, if 'A' then single attraction)
        if tour_attraction_id.startswith('T'):
            tour_id = int(tour_attraction_id[1:])

            # check if there is such a tour
            try:
                tour = Tour.objects.get(pk=tour_id)
            except ObjectDoesNotExist:
                return HttpResponse(('There is no tour with id: ' + str(tour_id)), status=400)

        elif tour_attraction_id.startswith('A'):
            attraction_id = int(tour_attraction_id[1:])

            # check if there is such a tour
            try:
                attraction = Attraction.objects.get(pk=attraction_id)
            except ObjectDoesNotExist:
                return HttpResponse(('There is no tour with id: ' + str(attraction_id)), status=400)
        else:
            return HttpResponse("Incorrect attraction/tour ID", status=400)

        # sending request to PSP
        # parsing date
        # checking number of guests (if not 0)
        if len([x for x in [kids_no, seniors_no, adults_no] if x is None]) == 4:
            print('all zeros')

    else:
        return HttpResponse(status=405)


@csrf_exempt
def make_tour(request):
    if request.method == 'POST':
        tour_name = request.POST['tour_name']
        attractions_list_str = request.POST['attractions']
        attractions = attractions_list_str[1:-1].split(',')
        tour = {
            'name': tour_name,
            'duration': len(attractions),
            'price': 0,
            'country': None
        }  # name, duration, price, country, attractions
        tour_attractions = []

        # iterating through the list and checking if the IDs are correct
        for counter, a in enumerate(attractions):
            try:

                attraction = Attraction.objects.get(pk=int(a))  # get the attraction of ID a
                tour_attractions.append(attraction)             # tour's attractions
                tour['price'] += attraction.price               # add attraction's price to tour's price

                if counter == 0:
                    tour['country'] = attraction.country        # set the tour's country

            except ObjectDoesNotExist as e:
                return HttpResponse(("There is no attraction with ID: " + str(a)), status=400)

        # adding tour to the database
        new_tour = Tour.objects.create(name=tour['name'],
                                       duration=tour['duration'],
                                       price=tour['price'],
                                       country=tour['country'])

        # adding attractions of the tour to database
        for a in tour_attractions:
            new_tour.attractions.add(a)

        # save in the database
        new_tour.save()

        return HttpResponse(("New tour's ID: " + new_tour.id), status=200)
    else:
        return HttpResponse(status=405)
