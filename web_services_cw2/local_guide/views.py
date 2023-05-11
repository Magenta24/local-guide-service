from django.shortcuts import render
from django.http import HttpResponse
from http import HTTPStatus
from .models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from datetime import datetime
from django.core.serializers.json import Serializer, DjangoJSONEncoder

from django.core.exceptions import ObjectDoesNotExist


def calculate_total_price(base_price, adults_no, kids_no, seniors_no):
    attraction_price_total = adults_no * base_price + \
                             kids_no * (Discount.objects.get(name='Children').value / 100) * base_price + \
                             seniors_no * (Discount.objects.get(name='Seniors').value / 100) * base_price

    return attraction_price_total

def create_json_error_msg(msg):
    msg_dict = {'message': msg}
    return json.dumps(msg_dict)

@csrf_exempt
def get_attractions(request):
    if request.method == 'GET':
        location = request.GET.get('location')
        category = request.GET.get('category')
        min_price = int(request.GET.get('min_price')) if request.GET.get('min_price') is not None else None
        max_price = int(request.GET.get('max_price')) if request.GET.get('max_price') is not None else None
        adults_no = int(request.GET.get('adults_no')) if request.GET.get('adults_no') not in [None, ''] else 0
        kids_no = int(request.GET.get('kids_no')) if request.GET.get('kids_no') not in [None, ''] else 0
        seniors_no = int(request.GET.get('seniors_no')) if request.GET.get('seniors_no') not in [None, ''] else 0

        # getting all attractions from the database
        attractions = Attraction.objects.all()
        attractions_dict = {'attractions': []}

        # filtering
        try:
            if location is not None:
                attractions = attractions.filter(country=Country.objects.get(name=location).id)
            if category is not None:
                attractions = attractions.filter(category=Category.objects.get(name=category).id)
            if min_price is not None:
                attractions = attractions.filter(price__gte=int(min_price))
            if max_price is not None:
                attractions = attractions.filter(price__lte=int(max_price))

        except ObjectDoesNotExist:
            return HttpResponse(('There is no attraction with parameters: ' + str({
                'location': location,
                'category': category,
                'min_price': min_price,
                'max_price': max_price})), status=400)

        # Serialize the records to JSON
        for a in attractions:
            # calculating price (all adults_no, seniors_no and kids_no are 0 then return base price which is per one, adult person)
            attraction_price_total = 0
            if len([x for x in [adults_no, seniors_no, kids_no] if x == 0]) == 3:
                attraction_price_total = a.price
            else:
                attraction_price_total = calculate_total_price(a.price, adults_no, kids_no, seniors_no)

            attractions_dict['attractions'].append({
                'id': a.id,
                'name': a.name,
                'base_price': a.price,
                'price_for_all_guests': attraction_price_total,
                'address': a.address,
                'category': a.category.name,
                'country': a.country.name,
                'description': a.description
            })

        attractions_json = json.dumps(attractions_dict)

        return HttpResponse(attractions_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_tours(request):
    if request.method == 'GET':
        location = request.GET.get('location') if request.GET.get('location') not in [None, ''] else None
        min_price = int(request.GET.get('min_price')) if request.GET.get('min_price') not in [None, ''] else None
        max_price = int(request.GET.get('max_price')) if request.GET.get('max_price') not in [None, ''] else None
        duration_max = int(request.GET.get('duration_max')) if request.GET.get('duration_max') not in [None,''] else None
        attractions_no_max = int(request.GET.get('attractions_no_max')) if request.GET.get('attractions_no_max') not in [None, ''] else None
        adults_no = int(request.GET.get('adults_no')) if request.GET.get('adults_no') not in [None, ''] else 0
        kids_no = int(request.GET.get('kids_no')) if request.GET.get('kids_no') not in [None, ''] else 0
        seniors_no = int(request.GET.get('seniors_no')) if request.GET.get('seniors_no') not in [None, ''] else 0

        # getting all attractions from the database
        tours = Tour.objects.all()
        tours_dict = {'tours': []}

        # filtering
        try:
            if location is not None:
                tours = tours.filter(country=Country.objects.get(name=location).id)
            if duration_max is not None:
                tours = tours.filter(duration__lte=duration_max)
            if min_price is not None:
                tours = tours.filter(price__gte=min_price)
            if max_price is not None:
                tours = tours.filter(price__lte=max_price)
            if attractions_no_max is not None:
                tours = tours.filter(attractions_no__lte=attractions_no_max)

        except ObjectDoesNotExist:
            return HttpResponse(('There is no attraction with parameters: ' + str({
                'location': location,
                'duration_max': duration_max,
                'min_price': min_price,
                'max_price': max_price,
                'attractions_no_max': attractions_no_max})), status=400)

        # Serialize the records to JSON
        for t in tours:
            attractions = []

            # calculating price (all adults_no, seniors_no and kids_no are 0 then return base price which is per one, adult person)
            tour_price_total = 0
            if len([x for x in [adults_no, seniors_no, kids_no] if x == 0]) == 3:
                tour_price_total = t.price
            else:
                tour_price_total = calculate_total_price(t.price, adults_no, kids_no, seniors_no)

            # adding all attractions of particular tour
            for a in t.attractions.all():
                attractions.append(a.name)

            tours_dict['tours'].append({
                'id': t.id,
                'name': t.name,
                'duration': t.duration,
                'base_price': t.price,
                'price_for_all_guests': tour_price_total,
                'country': t.country.name,
                'attractions': attractions
            })

        tours_json = json.dumps(tours_dict)

        return HttpResponse(tours_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_categories(request):
    if request.method == 'GET':

        categories = Category.objects.all()

        # serialization to JSON
        categories_dict = {'categories': []}
        for c in categories:
            categories_dict['categories'].append(c.name)

        categories_json = json.dumps(categories_dict)

        return HttpResponse(categories_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_discounts(request):
    if request.method == 'GET':

        discounts = Discount.objects.all()

        # serialization to JSON
        discounts_dict = {'discounts': []}
        for d in discounts:
            discounts_dict['discounts'].append({'name': d.name, 'value': d.value, 'description': d.description})

        discounts_json = json.dumps(discounts_dict)

        return HttpResponse(discounts_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_countries(request):
    if request.method == 'GET':

        countries = Country.objects.all()

        # serialization to JSON
        countries_dict = {'countries': []}
        for c in countries:
            countries_dict['countries'].append(c.name)

        countries_json = json.dumps(countries_dict)

        return HttpResponse(countries_json, content_type='application/json')
    else:
        return HttpResponse(status=405)


@csrf_exempt
def book(request):
    if request.method == 'POST':
        # print(json.loads(request.body))
        incoming_booking_json = json.loads(request.body)
        tour_attraction_id = incoming_booking_json['tour_attraction_id']
        psp_id = incoming_booking_json['psp_id']
        psp_checkout_id = incoming_booking_json['psp_checkout_id']
        start_date = incoming_booking_json['start_date']
        adults_no = incoming_booking_json['adults_no'] if 'adults_no' in incoming_booking_json else 0
        kids_no = incoming_booking_json['kids_no'] if 'kids_no' in incoming_booking_json else 0
        seniors_no = incoming_booking_json['seniors_no'] if 'seniors_no' in incoming_booking_json else 0

        # checking if any of the required parameters is NoneType
        if len([x for x in [tour_attraction_id, psp_id, psp_checkout_id, start_date] if x is None]) > 0:
            error_msg = create_json_error_msg('tour_attraction_id, psp_id, psp_checkout_id, start_date are required')
            return HttpResponse(error_msg, status=400)

        # creating booking object
        booking_dict = {'tour_attraction_id': None,
                        'psp_id': None,
                        'psp_checkout_id': None,
                        'start_date': None,
                        'adults_no': None,
                        'kids_no': None,
                        'seniors_no': None
                        }

        # parsing tour_attraction_id (if starts then 'T'-tour, if 'A' then single attraction)
        if tour_attraction_id.startswith('T'):

            tour_id = int(tour_attraction_id[1:])

            # check if there is such a tour
            try:
                tour = Tour.objects.get(pk=tour_id)
                booking_dict['tour_attraction_id'] = tour_attraction_id

                # calculating price (all adults_no, seniors_no and kids_no are 0 then return base price which is per one, adult person)
                booking_dict['price'] = 0
                if len([x for x in [adults_no, seniors_no, kids_no] if x == 0]) == 3:
                    booking_dict['price'] = tour.price
                else:
                    booking_dict['price'] = calculate_total_price(tour.price, adults_no, kids_no, seniors_no)

            except ObjectDoesNotExist:
                error_msg = create_json_error_msg(('There is no tour with id: ' + str(tour_id)))
                return HttpResponse(error_msg, status=400)

        elif tour_attraction_id.startswith('A'):
            attraction_id = int(tour_attraction_id[1:])

            # check if there is such a tour
            try:
                attraction = Attraction.objects.get(pk=attraction_id)
                booking_dict['tour_attraction_id'] = tour_attraction_id

                # calculating price (all adults_no, seniors_no and kids_no are 0 then return base price which is per one, adult person)
                booking_dict['price'] = 0
                if len([x for x in [adults_no, seniors_no, kids_no] if x == 0]) == 3:
                    booking_dict['price'] = attraction.price
                else:
                    booking_dict['price'] = calculate_total_price(attraction.price, adults_no, kids_no, seniors_no)

            except ObjectDoesNotExist:
                error_msg = create_json_error_msg(('There is no tour with id: ' + str(attraction_id)))
                return HttpResponse(error_msg, status=400)
        else:
            error_msg = create_json_error_msg("Incorrect attraction/tour ID")
            return HttpResponse(error_msg, status=400)

        # sending request to PSP to confirm the psp_checkout_id
        psp_checkout_status_code = None
        if int(psp_id) == 1:
            psp_checkout_status_code = requests.get(
                "http://sc20cah.pythonanywhere.com/api/checkout/" + str(psp_checkout_id) + '/status').status_code
        elif int(psp_id) == 2:
            psp_checkout_status_code = requests.get(
                "http://sc20ap.pythonanywhere.com/api/checkout/" + str(psp_checkout_id) + '/status').status_code
        elif int(psp_id) == 3:
            psp_checkout_status_code = requests.get(
                "http://sc20sh.pythonanywhere.com/api/checkout/" + str(psp_checkout_id) + '/status').status_code
        else:
            error_msg = create_json_error_msg("Incorrect psp ID")
            return HttpResponse(error_msg, status=400)

        # if status code is not equal 200
        print('STATUS CODE FROM PSP: ', str(psp_checkout_status_code))
        if psp_checkout_status_code != 200:
            return HttpResponse(("Incorrect psp_checkout_id: " + str(psp_checkout_id)), status=400)
        else:
            booking_dict['psp_id'] = psp_id
            booking_dict['psp_checkout_id'] = psp_checkout_id

        # parsing date
        try:
            booking_start_date = datetime.fromisoformat(start_date)
            booking_dict['start_date'] = booking_start_date.isoformat()
        except Exception as e:
            print(e)
            error_msg = create_json_error_msg('Incorrect datetime format. It should be ISO format %Y-%m-%dT%H:%M:%S%f')
            return HttpResponse(error_msg, status=400)

        # checking number of guests (if not 0)
        if len([x for x in [kids_no, seniors_no, adults_no] if x in [None, '']]) == 4:
            error_msg = create_json_error_msg('The total number of guests cannot be 0!')
            return HttpResponse(error_msg, status=400)
        else:
            booking_dict['adults_no'] = int(adults_no) if adults_no not in [None, ''] else 0
            booking_dict['kids_no'] = int(kids_no) if kids_no not in [None, ''] else 0
            booking_dict['seniors_no'] = int(seniors_no) if seniors_no not in [None, ''] else 0


        # adding booking to the database
        new_booking = Booking.objects.create(
            price=booking_dict['price'],
            start_date=booking_dict['start_date'],
            adults_no=booking_dict['adults_no'],
            kids_no=booking_dict['kids_no'],
            seniors_no=booking_dict['seniors_no'],
            tour_or_attraction_id=booking_dict['tour_attraction_id'],
            psp_id=booking_dict['psp_id'],
            psp_checkout_id=booking_dict['psp_checkout_id']
        )

        booking_dict['msg'] = 'Booked successfully'
        booking_json = json.dumps(booking_dict)
        return HttpResponse(booking_json, status=200)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def make_tour(request):
    if request.method == 'POST':

        # getting parameters
        incoming_new_tour_json = json.loads(request.body)
        tour_name = incoming_new_tour_json['tour_name']
        attractions_list_str = incoming_new_tour_json['attractions']

        # parsing the attraction list
        attractions = attractions_list_str[1:-1].split(',')
        tour = {
            'id': None,
            'name': tour_name,
            'duration': len(attractions),
            'price': 0,
            'country': None,
            'attractions_no': len(attractions),
            'attractions': []
        }

        tour_attractions = []  # attraction objects that are part of the tour

        # iterating through the list and checking if the IDs are correct
        for counter, a in enumerate(attractions):
            try:

                attraction = Attraction.objects.get(pk=int(a))  # get the attraction of ID a
                tour_attractions.append(attraction)  # tour's attractions
                tour['price'] += attraction.price  # add attraction's price to tour's price
                tour['attractions'].append(attraction.name)

                if counter == 0:
                    tour['country'] = attraction.country  # set the tour's country

            except ObjectDoesNotExist as e:
                return HttpResponse(("There is no attraction with ID: " + str(a)), status=400)

        # adding tour to the database
        try:
            new_tour = Tour.objects.create(name=tour['name'],
                                           duration=tour['duration'],
                                           price=tour['price'],
                                           country=tour['country'],
                                           attractions_no=tour['attractions_no'])
        except Exception as e:
            error_msg = create_json_error_msg(('There is a tour with name: ' + tour['name']))
            return HttpResponse(error_msg, status=400)

        # adding attractions of the tour to database
        for a in tour_attractions:
            new_tour.attractions.add(a)

        # save in the database
        new_tour.save()

        # return JSON
        tour['id'] = new_tour.id
        tour['country'] = tour['country'].name
        new_tour_json = json.dumps(tour)

        return HttpResponse(new_tour_json, content_type='application/json')
    else:
        return HttpResponse(status=405)
