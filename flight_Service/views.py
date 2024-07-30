from django.shortcuts import render,redirect
from .controllers import FlightController
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def FlightSearch(request):

	if request.method=="GET":
		context={
			"title":"Flight Search - Home",
			"userid": request.COOKIES.get('userid')
		}
		return render(request,'flight/search.html',context)


def GetAirLinesList(request):

	if request.method=="GET":
		airlinesList = FlightController().fetch_airlines_name()
		if airlinesList is not None:
			return JsonResponse({"airlines": airlinesList})


def FlightSearchResult(request):

	if request.method=="GET":
		departure_airport = request.GET.get('departure_airport', None)
		arrival_airport = request.GET.get('arrival_airport', None)
		departure_date = request.GET.get('departure_date', None)
		airline_name = request.GET.get('airline_name', None)
		flight_number = request.GET.get('flight_number', None)
		user_id = request.COOKIES.get('userid')

		search_param_data = {

			"departure_airport": departure_airport,
			"arrival_airport": arrival_airport,
			"departure_date": departure_date,
			"airline_name": airline_name,
			"flight_number":flight_number,
			"userid" : user_id

		}

		
		flight_data = FlightController().get_flight_data(search_param_data)
		for flight in flight_data:
			flight['userid'] = user_id
		print(flight_data)
		return JsonResponse(flight_data, safe=False)
		
@csrf_exempt
def SubscribeToNotification(request):

	if request.method=="POST":
		user_id = request.COOKIES.get('userid')
		if user_id:
			
			data = json.loads(request.body)
			print(data)
			flight_number = data.get('flight_number')
			airline_name = data.get('airline_name')
			sub_status = data.get('action')
			flight_detail = {
				"flight_number": flight_number,
				"airline_name": airline_name,
				"sub_status": sub_status,
				"userid" : user_id
			}
			if flight_number is None or  airline_name is None:
				return JsonResponse({"error": "Flight number or Airline Name is missing"}, status=400)

			FlightController().subscribeToNotify(flight_detail)
			return JsonResponse({"success": "Subscription successful"}, status=200)
		else:
			return JsonResponse({"error": "Please Login First"}, status=401)
	else:
		 return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def GetAllFlighstData(request):

	if request.method=="GET":

		flight_data = FlightController().fetch_flight_data()

		return JsonResponse(list(flight_data), safe=False)