from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime

import hashlib, binascii, os

from .models import Rmail

from django.contrib.sessions.models import Session

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
	if(request.session.has_key('is_logged') and request.session['is_logged']==True):
		return redirect('profile')
	else:
		return render(request,'rmail.html')

def register(request):
	return render(request,'signup.html')


def setting(request):
	return render(request,'setting.html')

def profile(request):
	if(request.session.has_key('is_logged') and request.session['is_logged']==True):
		username = request.session['username']
		result = firebase.get('/users',username)
		return render(request,'profile.html',{'title':result['Name'],'Name':result['Name'],'username':username,'Email':result['Email'],'DOB':result['Birtdate'],'Gender':result['Gender'],'durl':result['DP'],'curl':['Cover']})
	else:
		return redirect('login')


	return render(request,'profile.html')

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
	dp = "/media/images/user.png"
	cover = "/media/images/cover.jpeg"

	errormsg = []
	if(username==""):
		errormsg.append("Username cannot be empty.")
		username = ""
	elif(len(username)<4):
		errormsg.append("Username must be atleast 4 character long.")
		username = ""
	elif(username.isalnum()==False):
		errormsg.append("Invalid Username.")
		username = ""
	if(password==""):
		errormsg.append("Password cannot be empty.")
	elif(len(password)<8):
		errormsg.append("Password should be atleast 8 character long.")
	if(email==""):
		errormsg.append("Email id cannot be empty.")
		email = ""
	elif('@' not in email):
		errormsg.append("Invalid Email.")
		email = ""
	if(len(mob)!=10 or mob.isnumeric()==False):
		errormsg.append("Invalid Mobile Number.")
		mob = ""
	else:
		mobchk = firebase.get('/mobile',mob)
		if(mobchk):
			errormsg.append("This mobile number is in use. Please choose another one.")
	if(day=="0" or month=="0" or year=="0"):
		errormsg.append("Please provide correct birthdate.")
	if(gender=="Gender"):
		errormsg.append("Please select a Gender.")
	if(len(errormsg)>0):
		return render(request,'signup.html',{"warning":errormsg,"USERNAME":username,"NAME":name,"EMAIL":email,"MOBILE":mob,"GENDER":gender})
	else:
		result  = firebase.get("/users",username)
		if(result):
			errormsg.append("This username already taken. Please choose another one.")
			username =""
			return render(request,'signup.html',{"warning":errormsg,"USERNAME":username,"NAME":name,"EMAIL":email,"MOBILE":mob,"GENDER":gender})
		else:
			has_pass = hash_password(password)
			result = firebase.put('/users',username,{'Name':name,'Password':has_pass,'Email':email,'Mobile':mob,'Birtdate':bday,"Gender":gender,"DP":dp,"Cover":cover})
			mobres =	firebase.put('/mobile',mob,{"username":username})
			if(result):
				request.session['is_logged'] = True
				request.session['username'] = username
				return redirect('profile')
			else:
				errormsg =['Some Unknown Error Happened. Please Try again later.']
				return render(request,'signup.html',{'warning':errormsg})



def login(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		errormsg = []
		if(username==""):
			errormsg.append("Username cannot be empty.")
		elif(len(username)<4):
			errormsg.append("Username must be atleast 4 character long.")
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
			    	request.session['is_logged'] = True
			    	request.session['username'] = username
			    	return redirect('profile')
			    else:
			    	errormsg.append("Wrong Password.")
			    	return render(request,'login.html',{'warning':errormsg,"title":"Login Error"})
			else:
				errormsg.append("Username not in our records!! Please Signup.")
				return render(request,'login.html',{'warning':errormsg,"title":"Login Error"})
	else:
		if(request.session.has_key('is_logged') and request.session['is_logged']==True):
			print("yes")
			print(request.session['username'])
			return redirect('profile')
		else:
			return render(request,'Login.html')

def logout(request):
	request.session['is_logged'] = False
	request.session['username'] == None
	print(request.session['is_logged'])
	print(request.session['username'])
	return render(request,'Login.html')


def forgotpass(request):
	fuser = request.POST["fuser"]
	fmob = request.POST["fmob"]
	fpas = request.POST["newpwd"]
	errormsg = []
	if(fuser==""):
		errormsg.append("Username cannot be empty.")
	elif(len(fuser)<4):
		errormsg.append("Username must be atleast 4 character long.")
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
				res = firebase.put('/users',fuser,{'Name':result['Name'],'Password':hash_pass,'Email':result['Email'],'Mobile':result['Mobile'],'Birtdate':result['Birtdate'],"Gender":result['Gender'],"DP":result['DP'],"Cover":result['Cover']})
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


def imgcng(request):
		changedp = request.FILES['dp']
		usernaam = request.POST["username"]
		print(changedp.name)
		result = firebase.get("/users",usernaam)
		if(result["DP"]=="/media/images/user.png"):
			changedp.name = usernaam+"1"+".jpg"
		else:
			i = int(result["DP"][-5])
			changedp.name = usernaam+str(i+1)+".jpg"
		print(changedp.name)
		dpurl = "/media/images/"+changedp.name 
		user = Rmail(pic = changedp)
		user.save()
		firebase.delete("/users",usernaam)
		res = firebase.put('/users',usernaam,{'Name':result['Name'],'Password':result['Password'],'Email':result['Email'],'Mobile':result['Mobile'],'Birtdate':result['Birtdate'],"Gender":result['Gender'],"DP":dpurl,"Cover":result['Cover']})

		return redirect('profile')
		# result = firebase.update("users",username,{'DP':dpurl})
		# return render(request,'profile.html',{'title':result['Name'],'Name':result['Name'],'username':username,'Email':result['Email'],'DOB':result['Birtdate'],'Gender':result['Gender'],'durl':durl})

def newmsg(request):
	if(request.session.has_key('is_logged') and request.session['is_logged']==True):
		if request.method == "POST":
			username = request.session['username']
			recipient = request.POST['recipient']
			msg = request.POST['message']
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
			timestamp = dt_string
			sender = username

			#for sender side message 

			data = firebase.get('/sentmessage',sender)
			res = {'message': msg,'recipient':recipient,'time':timestamp}
			if(data is None):
			    data =[]
			    data.append(res)
			else:
			    data.append(res)
			firebase.put('/sentmessage',sender,data)

			#for reciever side message
			sen = {'message': msg,'time': timestamp}
			another = firebase.get('/recieved',recipient)
			if(another is None):
			    another = []
			    another.append(sen)
			else:
			    another.append(sen)
			firebase.put('/recieved',recipient,another)
			return render(request,'welcome.html')
		else:
			return redirect('profile')
	else:
		return redirect('login')

