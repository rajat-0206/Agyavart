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

	result = firebase.put('/users',username,{'Name':name,'Password':password,'Email':email,'Mobile':mob,'Birtdate':bday,"Gender":gender})

	if(result):
		return render(request,'Login.html')

	else:
		return render(request,'signup.html')



def checkkaro(request):
	username = request.POST["username"]
	password = request.POST["password"]
	result=firebase.get("/users",username)
	if(result):
	    text=result["Password"]
	    if(text==password):
	    	return render(request,'welcome.html',{'msg':'login success'})
	    else:
	    	return render(request,'welcome.html',{'msg':'wrong password','user':username,'pass':password})
	else:
		return render(request,'welcome.html',{'msg':'wrong username','error':result,'user':username,'pass':password})

