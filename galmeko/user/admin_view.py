from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from setting.models import Vehicle
from vendor.models import Driver
from booking.models import Booking,BookingFeature,BookingStop
from django.contrib import messages
from django.core import serializers
from .models import User
import json,requests

# Get Vehicle list for vendor DataTable
def get_vehicle_list(request):
    vendor_id = request.POST.get('vendor_id')
    draw = int(request.GET.get("draw", 0))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 7))

    all_objects = Vehicle.objects.filter(vendor_id=vendor_id)
    filtered_count = all_objects.count()
    total_count = Vehicle.objects.count()
    data = serializers.serialize('json', all_objects)

    json_objects = json.loads(data)
    list_objects = []
    for index in range(len(json_objects)):
        json_objects[index]['fields']['id'] = all_objects[index].id
        json_objects[index]['fields']['status_id'] = all_objects[index].status
        result = json_objects[index]['fields']['status']
        if(result == 1):
            json_objects[index]['fields']['status'] = 'Active'
        elif(result == 0):
            json_objects[index]['fields']['status'] = 'Inactive'
        elif(result == 2):
            json_objects[index]['fields']['status'] = 'Booked'
        else:
            json_objects[index]['fields']['status'] = 'Deleted'
        list_objects.append(json_objects[index]['fields'])

    return HttpResponse(json.dumps(list_objects), content_type='application/json;charset=utf-8')

# Delete Functionality for vehicle Listing on vendor
def delete_vehicle(request):
    result = {}
    if request.method == 'POST' and request.is_ajax():
        try:
            vehicleId = request.POST.get('id', '')
            response = Vehicle.objects.filter(pk=vehicleId).update(status=3)
            if (response == True):
                result['status'] = True
                result['msg'] = 'Vehicle Deleted Successfully successfully!'
                return JsonResponse(result)
            else:
                result['status'] = False
                result['msg'] = 'Something went wrong!'
                return JsonResponse(result)
        except Http404:
            return HttpResponseRedirect("/vendor/vendor/view/")
    else:
        return HttpResponse('Invalid request passed')

# Driver Listing for Vendor Section
def get_driver_list(request):
    vendor_id = request.POST.get('vendor_id')
    print(vendor_id)
    draw = int(request.GET.get("draw", 0))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 7))

    all_objects = Driver.objects.filter(vendor_id=vendor_id)
    filtered_count = all_objects.count()
    total_count = Driver.objects.count()
    data = serializers.serialize('json', all_objects)

    json_objects = json.loads(data)
    list_objects = []
    for index in range(len(json_objects)):
        json_objects[index]['fields']['id'] = all_objects[index].id
        json_objects[index]['fields']['status_id'] = all_objects[index].status
        result = json_objects[index]['fields']['status']
        if(result == 1):
            json_objects[index]['fields']['status'] = 'Active'
        elif(result == 0):
            json_objects[index]['fields']['status'] = 'Inactive'
        elif(result == 2):
            json_objects[index]['fields']['status'] = 'Booked'
        else:
            json_objects[index]['fields']['status'] = 'Deleted'
        list_objects.append(json_objects[index]['fields'])

    return HttpResponse(json.dumps(list_objects), content_type='application/json;charset=utf-8')

def GetUserDataByType(request):
    userData = User.objects.filter(type=request.POST.get('user_type')).filter(status = 1).values('id','first_name','last_name','email')
    result = {}
    if not userData:
        result['status'] = False
        result['data'] = 'Data Not Found'
    else:
        result['status'] = True
        result['data'] = list(userData)
   
    return JsonResponse(result)

def GetLatLongByAddress(request):
    api_key = "AIzaSyAjRK7OqmoYM-KJki3hji4vZo6SiMl_nWA"
    origin_address=request.POST.get('origin')
    destination_address=request.POST.get('destination')
    origin_api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(origin_address, api_key))
    destination_api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(destination_address, api_key))
    origin_api_response_dict = origin_api_response.json()
    destination_api_response_dict = destination_api_response.json()
    response = {}
    if origin_api_response_dict['results'] and destination_api_response_dict['results']:
        origin_geocode = origin_api_response_dict['results'][0]['geometry']['location']['lat'] + ',' + origin_api_response_dict['results'][0]['geometry']['location']['lng']
        destination_geocode = destination_api_response_dict['results'][0]['geometry']['location']['lat'] + ',' + destination_api_response_dict['results'][0]['geometry']['location']['lng']
        response = {
            'status' : True,
            'origin' : origin_geocode,
            'destination': destination_geocode
        }
    else:
        response = {
            'status' : False,
            'origin' : '28.5052605,77.0827607',
            'destination' : '28.4616027,77.036577'
        }
        
    return JsonResponse(response, safe=False)

def add_booking(request):
    result = {}
    if request.method == 'POST': 
        try:
            booking = save_booking(request)
            if booking['status'] == 200:
                booking_id = booking['booking_id']
                stopAndFeature = save_stop_feature(request,booking_id)
                if (stopAndFeature['status'] == 200):
                    messages.success(request, 'Booking Added successfully!')
                else:
                   messages.success(request, 'Something Went Wrong!') 
            else:
                messages.success(request, 'Something went wrong!')
            return HttpResponseRedirect("/admin/booking/booking/")
           
        except Http404:
            return HttpResponseRedirect("/admin/booking/booking/")
    else:
        return HttpResponse('Invalid request passed')

def save_stop_feature(request,booking_id):
    result = {}
    feature_len = len(request.POST.getlist('features'))
    features = request.POST.getlist('features')
    stop_name = request.POST.getlist('stop_name')
    stop_phone = request.POST.getlist('stop_phone')
    stop_address = request.POST.getlist('stop_address')
    stop_len = min([len(stop_name), len(stop_phone), len(stop_address)])
    length = min([len(features)])
    if length > 0:
        for i in range(0,length,1):
            feature = BookingFeature(booking_id= booking_id,feature_id= features[i]
            )
            feature.save()
            if feature.id:
                result['feature_status'] = 200
            else:
                result['feature_status'] = 400
    if length > 0:
        for i in range(0,stop_len,1):
            stops = BookingStop(booking_id= booking_id,name= stop_name[i],phone= stop_phone[i],address= stop_address[i]
                )
            stops.save()
            if stops.id:
                result['stops_status'] = 200
            else:
                result['stops_status'] = 400
    if( result['stops_status'] == 200 and result['feature_status'] == 200):
        result['status'] = 200
        return result
    else:
        result['status'] = 200
        return result

def save_booking(request):
    result = {}
    booking_type    = request.POST.get('booking_type')
    origin_name     = request.POST.get('origin_name')
    origin_phone    = request.POST.get('origin_phone')
    origin_address  = request.POST.get('origin_address')
    origin_geocode  = request.POST.get('origin_geocode')
    destination_name     = request.POST.get('destination_name')
    destination_phone    = request.POST.get('destination_phone')
    destination_address  = request.POST.get('destination_address')
    destination_geocode  = request.POST.get('destination_geocode')
    booking_msg  = request.POST.get('notes')
    if request.POST.get('trip') is None:
        round_trip  = 0
    else:
        round_trip  = request.POST.get('trip')
    fare  = request.POST.get('fare')
    category_id = request.POST.get('category')
    user_id = request.POST.get('id_user')
    status = 1

    booking = Booking(booking_type = booking_type,origin_name = origin_name,origin_phone = origin_phone,origin_address = origin_address, origin_geocode = origin_geocode,destination_name = destination_name,destination_phone = destination_phone,destination_address = destination_address,destination_geocode = destination_geocode,booking_msg = booking_msg,round_trip = round_trip,fare = fare,category_id = category_id,user_id = user_id,status = status)
    booking.save()
    if(booking.id):
        result['status'] = 200
        result['booking_id'] = booking.id
    else:
        result['status'] = 400

    return result 

    