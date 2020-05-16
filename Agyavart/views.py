from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
import hashlib, binascii, os

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

#Hasing Functions

def temp(request):
	return render(request,'signup1.html')

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

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
	if(len(mob)!=10 or mob.isnumeric()==False):
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
			has_pass = hash_password(password)
			result = firebase.put('/users',username,{'Name':name,'Password':has_pass,'Email':email,'Mobile':mob,'Birtdate':bday,"Gender":gender})
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
		return render(request,'login.html',{"warning":errormsg,"title":"Login Error"})
	else:
		result=firebase.get("/users",username)
		if(result):
		    text=result["Password"]

		    if(verify_password(result['Password'],password)):
		    	return render(request,'profile.html',{'title':result['Name'],'Name':result['Name'],'username':username,'Email':result['Email'],'DOB':result['Birtdate'],'Gender':result['Gender']})
		    else:
		    	errormsg.append("Wrong Password.")
		    	return render(request,'login.html',{'warning':errormsg,"title":"Login Error"})
		else:
			errormsg.append("Username not in our records!! Please Signup.")
			return render(request,'login.html',{'warning':errormsg,"title":"Login Error"})


def forgotpass(request):
	fuser = request.POST["fuser"]
	fmob = request.POST["fmob"]
	fpas = request.POST["newpwd"]
	errormsg = []
	if(fuser==""):
		errormsg.append("Username cannot be empty.")
	elif(len(fuser)<8):
		errormsg.append("Username must be atleast 8 character long.")
	elif(fuser.isalnum()==False):
		errormsg.append("Invalid Username.")
	if(fpas==""):
		errormsg.append("Password cannot be empty.")
	elif(len(fpas)<8):
		errormsg.append("Password should be atleast 8 character long.")
	if(len(fmob)!=10 or fmob.isnumeric()==False):
		errormsg.append("Invalid Mobile Number.")
	if(len(errormsg)>0):
		return render(request,'login.html',{"warning":errormsg,"title":"Forgot Password"})
	else:
		result = firebase.get('/users',fuser)
		if(result):
			if(fmob==result["Mobile"]):
				hash_pass = hash_password(fpas);
				firebase.delete("/users",fuser)
				res = firebase.put('/users',fuser,{'Name':result['Name'],'Password':hash_pass,'Email':result['Email'],'Mobile':result['Mobile'],'Birtdate':result['Birtdate'],"Gender":result['Gender']})
				return render(request,'login.html',{'info':'Password changed successfully. Now you can login.'})
			else:
				errormsg = ['Mobile Number did not match. Try Again!!']
				return render(request,'login.html',{"warning":errormsg,"title":"Forgot Password"})
		else:
			errormsg = ['Invalid Username. Please try again!!']
			return render(request,'login.html',{"warning":errormsg,"title":"Forgot Password"})
	

def forgotusername(request):
	gmob = request.POST["mobile"]
	if(len(gmob)!=10 or gmob.isnumeric()==False):
		errormsg = ['Invalid Mobile Number.']
		return render(request,'login.html',{"warning":errormsg,"title":"Forgot Username"})
	else:

		result = firebase.get("/mobile",gmob)
		if(result):
			msg = 'Your username is ' + result['username']+'. You can use it to login.'
			return render(request,'login.html',{'info':msg,'title':'Forgot Username'})
		else:
			errormsg = ['No username associated with this number.']
			return render(request,'login.html',{"warning":errormsg,"title":"Forgot Username"})

def handle_uploaded_file(f):
    with open('/static/rajat.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
# def imgcng(request):
# 	upload = request.FILES['dp']
# 	return render(request,'welcome.html',{'user':upload})

def imgcng(request):
    if request.method == 'POST':
        uploadFileForm(request.POST, request.FILES)
        handle_uploaded_file(request.FILES['file'])
        return render(request,'welcome.html')