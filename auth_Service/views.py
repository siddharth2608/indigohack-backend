from django.shortcuts import render,redirect
from .controllers import AuthController

def RegisterUser(request):

	if request.method=="GET":
		context={
			"title":"Register"
		}
		return render(request,'auth/register.html',context)


	if request.method=="POST":

		firstname = request.POST["firstname"]
		lastname = request.POST["lastname"]
		username = request.POST["username"]
		email = request.POST["email"]
		phone = request.POST["phone"]
		password = request.POST["password"]

		register_data = {

			"firstname":firstname,
			"lastname":lastname,
			"username":username,
			"email":email,
			"phone":phone,
			"password": password
		}

		AuthController().save_registration_form(register_data)
		
		return redirect('authapp:register_user')


def LoginUser(request):

	if request.method=="GET":
		context = {
			"title":"Login"
		}
		return render(request,'auth/login.html',context)

	if request.method=="POST":

		login_data = {"email":request.POST["email"],"password":request.POST["password"]}
		user_data = AuthController().get_user_data(login_data)
		if user_data:
			user_id = user_data.get('id')
			response = redirect('flightapp:homepage')
			response.set_cookie('userid', str(user_id))
			return response
		else:
			return render(request,'auth/login.html')


def LogoutUser(request):
	if request.method=="GET":
		response = redirect('flightapp:homepage')
		response.delete_cookie('userid')
		return response