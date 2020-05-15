from django.shortcuts import render
from django.http import HttpResponse

from firebase import firebase
firebase = firebase.FirebaseApplication('https://agyavart-27f8b.firebaseio.com/', None)

# config = {
# 	'apiKey': "AIzaSyBp17YUm4uju7nqT5syTdGIUc_mJ253PH0",
#   'authDomain': "agyavart-27f8b.firebaseapp.com",
#   'databaseURL': "https://agyavart-27f8b.firebaseio.com",
#   'projectId': "agyavart-27f8b",
#   'storageBucket': "agyavart-27f8b.appspot.com",
#   'messagingSenderId': "223304863434",
#   'appId': "1:223304863434:web:585b9e9ace6b42ad51ee33",
#   'measurementId': "G-7KW9B9M084"
# }

# firebase = pyrebase.initialize_app(config)

# auth = firebase.auth()

# Create your views here.

def home(request):

	#result = firebase.put('/users','rajathandsom',{'username':'rajathandsom','password':'rajat'})


	return render(request,'rmail.html')

def login(request):
	return render(request,'Login.html')

def register(request):
	return render(request,'signup.html')

def banao(request):
	username = request.POST["USERNAME"]
	password = request.POST["password"]
	name = request.POST["NAME"]
	email = request.POST["EMAIL"]
	mob = request.POST["MOBILE"]
	day = request.POST["birthday_day"]
	month = request.POST["birthday_month"]
	year = request.POST["birthday_year"]
	gender = request.POST["GENDER"]
	bday = str(day)+'/'+str(month)+'/'+str(year)


	errormsg = []
	if(username==""):
		errormsg.append("Username cannot be empty.")
	elif(len(username)<8):
		errormsg.append("Username must be atleast 8 character long.")
	elif(username.isalnum()==False):
		errormsg.append("Invalid Username.")
	if(password==""):
		errormsg.append("Password cannot be empty.")
	elif(len(password)<8):
		errormsg.append("Password should be atleast 8 character long.")
	if(email==""):
		errormsg.append("Email id cannot be empty.")
	elif('@' not in email):
		errormsg.append("Invalid Email.")
	if(len(mob)!=10):
		errormsg.append("Invalid Mobile Number.")
	if(day=="0" or month=="0" or year=="0"):
		errormsg.append("Please provide correct birthdate.")
	if(gender=="Gender"):
		errormsg.append("Please select a Gender.")
	if(len(errormsg)>0):
		return render(request,'signup.html',{"warning":errormsg})
	else:
		result  = firebase.get("/users",username)
		if(result):
			errormsg.append("This username already taken. Please choose another one.")
			return render(request,'signup.html',{warning:errormsg})
		else:

			result = firebase.put('/users',username,{'Name':name,'Password':password,'Email':email,'Mobile':mob,'Birtdate':bday,"Gender":gender})
			mobres =	firebase.put('/mobile',mob,{"username":username})
			if(result):
				return render(request,'Login.html')
			else:
				errormsg =['Some Unknown Error Happened. Please Try again later.']
				return render(request,'signup.html',{'warning':errormsg})



def checkkaro(request):
	username = request.POST["username"]
	password = request.POST["password"]
	errormsg = []
	if(username==""):
		errormsg.append("Username cannot be empty.")
	elif(len(username)<8):
		errormsg.append("Username must be atleast 8 character long.")
	elif(username.isalnum()==False):
		errormsg.append("Invalid Username.")
	if(password==""):
		errormsg.append("Password cannot be empty.")
	elif(len(password)<8):
		errormsg.append("Password should be atleast 8 character long.")

	if(len(errormsg)>0):
		return render(request,'login.html',{"warning":errormsg})
	else:
		result=firebase.get("/users",username)
		if(result):
		    text=result["Password"]
		    if(text==password):
		    	return render(request,'welcome.html',{'msg':'login success.'})
		    else:
		    	errormsg.append("Wrong Password.")
		    	return render(request,'login.html',{'warning':errormsg})
		else:
			errormsg.append("Username not in our records!! Please Signup.")
			return render(request,'login.html',{'warning':errormsg})

