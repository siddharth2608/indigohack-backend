from django.shortcuts import render,redirect
from .controllers import FlightController
from django.http import JsonResponse


def FlightSearch(request):

	if request.method=="GET":
		context={
			"title":"Flight Search - Home"
		}
		return render(request,'flight/search.html',context)


def GetAirLinesList(request):

	if request.method=="GET":
		airlinesList = FlightController().fetch_airlines_name()
		if airlinesList is not None:
			return JsonResponse({"airlines": airlinesList})


def FlightSearchResult(request):

	print("inside")

	if request.method=="GET":
		departure_airport = request.GET.get('departure_airport', None)
		arrival_airport = request.GET.get('arrival_airport', None)
		departure_date = request.GET.get('departure_date', None)
		airline_name = request.GET.get('airline_name', None)
		flight_number = request.GET.get('flight_number', None)

		search_param_data = {

			"departure_airport": departure_airport,
			"arrival_airport": arrival_airport,
			"departure_date": departure_date,
			"airline_name": airline_name,
			"flight_number":flight_number

		}

		
		flight_data = FlightController().get_flight_data(search_param_data)

		return JsonResponse(flight_data, safe=False)
		
