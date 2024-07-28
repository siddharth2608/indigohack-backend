from config import Config


class AuthController:

	def __init__(self):
		self.db_conn = Config.POSTGRESSQL_CONN

	def save_registration_form(self, register_data):
		query = '''insert into usermaster (username, firstname, lastname, email, phone ,password) 
					values ('{username}', '{firstname}', '{lastname}', '{email}','{phone}', '{password}')'''.format(**register_data)

		self.db_conn.write_db(query)

	def get_user_data(self, login_data):
		query = '''select * from usermaster where email = '{email}' and password = '{password}' '''.format(**login_data)
		result = self.db_conn.query_db_one(query)
		return result