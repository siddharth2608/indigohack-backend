from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'flightapp'

urlpatterns = [
	
	path('search',views.FlightSearch, name='homepage'),
	path('airlinesList',views.GetAirLinesList, name='airlinesList'),
	path('searchflightdata/', views.FlightSearchResult, name='flightsearchdata')
]