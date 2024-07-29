from config import Config


class FlightController:

	def __init__(self):
		self.db_conn = Config.POSTGRESSQL_CONN


	def fetch_airlines_name(self):
		query='''select DISTINCT (airline) from flightdata'''
		result = self.db_conn.query_db(query)
		return result


	def get_flight_data(self,flight_search_filter):
		if(flight_search_filter["departure_airport"] and flight_search_filter["arrival_airport"] and flight_search_filter["departure_date"]):

			query = '''select * from flightdata fd full join subscriptions subs on fd.airline=subs.sub_airline
			 and fd.flightnumber=subs.sub_flightnumber where fd.departure='{departure_airport}' and fd.arrival='{arrival_airport}'
			and DATE_TRUNC('day', fd.departuredate) ='{departure_date}'  '''.format(**flight_search_filter)

		elif (flight_search_filter["airline_name"] and flight_search_filter["flight_number"]):
			query = '''select * from flightdata fd full join subscriptions subs on fd.airline=subs.sub_airline and 
			fd.flightnumber=subs.sub_flightnumber where fd.airline='{airline_name}' and fd.flightnumber='{flight_number}'  '''.format(**flight_search_filter)

		result = self.db_conn.query_db(query)
		return result


	def subscribeToNotify(self,flight_detail):
		if(flight_detail["sub_status"]=='1'):
			query = '''insert into subscriptions (user_id,sub_airline,sub_flightnumber,subscribe_status) values ('{userid}','{airline_name}','{flight_number}','1') '''.format(**flight_detail)

		elif (flight_detail["sub_status"]=='0'):
			query = '''delete from subscriptions where sub_airline='{airline_name}' and sub_flightnumber='{flight_number}' '''.format(**flight_detail)

		self.db_conn.write_db(query)


	def fetch_flight_data(self):

		query = '''select * from flightdata WHERE departuredate > CURRENT_TIMESTAMP'''
		result = self.db_conn.query_db(query)
		return result