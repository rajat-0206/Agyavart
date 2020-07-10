from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from datetime import datetime

from .models import sentmessage,recievedmessage,users,chatmsg
import os

from win10toast import ToastNotifier

from django.core.mail import EmailMultiAlternatives,send_mail

import random

import requests
import json

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
def rajat(request):
	return render(request,'rajat.html')

def privacy(request):
	return render(request,'privacy.html')

def offline(request):
    return render(request,"offline.html")

def manifest(request):
	return render(request,'manifest.json')
def temp(request):
	return render(request,'signup1.html')

def about(request):
	return render(request,"about.html")

def handle404(request,exception):
    return render(request,"404.html")
def alluser(request):
	result = firebase.get("/users",None)
	data =[]
	for i in result:
		obj = users()
		obj.username = i
		obj.name = result[i]['Name']
		obj.photo = result[i]['DP']
		data.append(obj)
	return render(request,'alluser.html',{'data':data})

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
			return redirect('profile.html')
		else:
			return render(request,'rmail.html')

def about(request):
	return render(request,'about.html')

def register(request):
	return render(request,'signup.html')

def loader(request):
	return render(request,'loader.html')


def setting(request):
	if(request.session.has_key('is_logged') and request.session['is_logged']==True):
		username = request.session['username']
		result = firebase.get('/users',username)
		return render(request,'setting.html',{'Name':result['Name'],'username':username,'Mobile':result["Mobile"],'Email':result['Email'],'DOB':result['Birtdate'],'Gender':result['Gender'],"school":result['School'],"college":result["College"],"higher":result["Higher"],"fb":result['FB'],"insta":result["Insta"],"twitter":result["Twitter"],"tok":result["Tok"]})
	else:
		return redirect('login')

def profile(request):
	if(request.session.has_key('is_logged') and request.session['is_logged']==True):
		username = request.session['username']
		result = firebase.get('/users',username)
		return render(request,'profile.html',{'title':result['Name'],'Name':result['Name'],'username':username,'Email':result['Email'],'Mobile':result["Mobile"],'DOB':result['Birtdate'],'Gender':result['Gender'],"school":result['School'],"college":result["College"],"higher":result["Higher"],"fb":result['FB'],"insta":result["Insta"],"twitter":result["Twitter"],"tok":result["Tok"],'durl':result['DP'],'curl':result['Cover']})
	else:
		return redirect('login.html')

def user(request,username):
		usernaam = username
		if(request.session.has_key('is_logged') and request.session['is_logged']==True):
			if(usernaam==request.session['username']):
				print("yes")
				return redirect('profile')
			else:
				result = firebase.get('/users',usernaam)
				if(result is None):
					return render(request,'user.html',{"is_loged":'True','warning':"No such user found"})
				else:
					return render(request,'user.html',{"is_loged":'True','title':result['Name'],'Name':result['Name'],'username':username,'Email':result['Email'],'Mobile':result["Mobile"],'DOB':result['Birtdate'],'Gender':result['Gender'],"school":result['School'],"college":result["College"],"higher":result["Higher"],"fb":result['FB'],"insta":result["Insta"],"twitter":result["Twitter"],"tok":result["Tok"],'durl':result['DP'],'curl':result['Cover']})
		else:
			result = firebase.get('/users',usernaam)
			if(result is None):
				return render(request,'user.html',{'warning':"No such user found"})
			else:
				return render(request,'user.html',{'title':result['Name'],'Name':result['Name'],'username':username,'Email':result['Email'],'Mobile':result["Mobile"],'DOB':result['Birtdate'],'Gender':result['Gender'],"school":result['School'],"college":result["College"],"higher":result["Higher"],"fb":result['FB'],"insta":result["Insta"],"twitter":result["Twitter"],"tok":result["Tok"],'durl':result['DP'],'curl':result['Cover']})


def banao(request):
	if request.method=="POST":
		username = request.POST["USERNAME"]
		username = username.lower()
		password = request.POST["password"]
		name = request.POST["NAME"]
		email = request.POST["EMAIL"]
		mob = request.POST["MOBILE"]
		gender = request.POST["GENDER"]
		bday = request.POST["DOB"]
		dp = "/media/images/user.png"
		cover = "/media/images/cover.jpeg"
		fb = "UA"
		insta = "UA"
		twiiter ="UA"
		tok ="UA"
		school="UA"
		college="UA"
		higher="UA"

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

		naam = name.split(" ")
		for i in naam:
			if(i.isalpha()==False):
				name =""
				errormsg.append("Invalid Name")
				break

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
		if(gender=="Gender"):
			errormsg.append("Please select a Gender.")
		if(len(errormsg)>0):
			return render(request,'signup.html',{"warning":errormsg,"USERNAME":username,"NAME":name,"EMAIL":email,"MOBILE":mob,"GENDER":gender,})
		else:
			result  = firebase.get("/users",username)
			if(result):
				errormsg.append("This username already taken. Please choose another one.")
				username =""
				return render(request,'signup.html',{"warning":errormsg,"USERNAME":username,"NAME":name,"EMAIL":email,"MOBILE":mob,"GENDER":gender})
			else:
				has_pass = hash_password(password)
				result = firebase.put('/users',username,{'Name':name,'Password':has_pass,'Email':email,'Mobile':mob,'Birtdate':bday,"Gender":gender,"DP":dp,"Cover":cover,"School":school,"College":college,"Higher":higher,"FB":fb,"Insta":insta,"Twitter":twiiter,"Tok":tok})
				mobres =	firebase.put('/mobile',mob,{"username":username})
				if(result):
					request.session['is_logged'] = True
					request.session['username'] = username
					return redirect('profile')
				else:
					errormsg =['Some Unknown Error Happened. Please Try again later.']
					return render(request,'signup.html',{'warning':errormsg})
	else:
		redirect('signup')



def login(request):
	if request.method == "POST":
		username = request.POST["username"]
		username = username.lower()
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
			return render(request,'Login.html',{"warning":errormsg,"title":"Login Error","username":username})
		else:
			result=firebase.get("/users",username)
			if(result):
			    text=result["Password"]
			    if(verify_password(result['Password'],password)):
			    	request.session['is_logged'] = True
			    	request.session['username'] = username
			    	return redirect('profile.html')
			    else:
			    	errormsg.append("Wrong Password.")
			    	return render(request,'Login.html',{'warning':errormsg,"title":"Login Error","username":username})
			else:
				errormsg.append("Username not in our records!! Please Signup.")
				return render(request,'Login.html',{'warning':errormsg,"title":"Login Error"})
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



def sendotp(request):
	if(request.method=="POST"):
		username = request.POST['username']
		result = firebase.get("/users",username)
		if(result is None):
			return HttpResponse('No account associated with this username')
		else:
			lis=[1,2,3,4,5,6,7,8,9,0,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
			code=str(random.choice(lis))+str(random.choice(lis))+str(random.choice(lis))+str(random.choice(lis))+str(random.choice(lis))+str(random.choice(lis))
			htmlgen = '<p>Your OTP is <strong>'+code+'</strong></p>'
			send_mail('OTP request for Agyavart Login','123456','noreply.jumblejuggle@gmail.com',[result['Email']],fail_silently=False,html_message=htmlgen)
			query = "otp/"+username
			firebase.patch_async(query,{"current":code})
			return HttpResponse("OTP sent on register Email")
	else:
		return redirect('login')

def sendmail(request):
	if(request.method=="POST"):
		email = request.POST['email']
		lis=[1,2,3,4,5,6,7,8,9,0,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		code=str(random.choice(lis))+str(random.choice(lis))+str(random.choice(lis))+str(random.choice(lis))+str(random.choice(lis))+str(random.choice(lis))
		htmlgen = '<p>Your OTP for completing registration is <strong>'+code+'</strong></p>'
		send_mail('OTP request for new Agyavart account','123456','noreply.jumblejuggle@gmail.com',[email],fail_silently=False,html_message=htmlgen)
		return HttpResponse(code)
	else:
		return redirect('signup')



def forgotpass(request):
	if request.method == "POST":
		fuser = request.POST["username"]
		fuser = fuser.lower()
		otp = request.POST["otp"]
		fpas = request.POST["password"]
		conpass = request.POST["conpass"]
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
		elif(fpas!=conpass):
			errormsg.append("Confirm Password not matched.")
		if(len(otp)!=6 ):
			errormsg.append("Please enter 6 character for OTP")
		if(len(errormsg)>0):
			return HttpResponse(errormsg)
		else:
			res = firebase.get('/otp',fuser)
			if(otp==str(res['current'])):
					hash_pass = hash_password(fpas)
					result = firebase.get("/users",fuser)
					print(result)
					firebase.put('/users',fuser,{'Name':result['Name'],"Password":hash_pass,'Email':result['Email'],'Mobile':result['Mobile'],'Birtdate':result['Birtdate'],'Gender':result['Gender'],"School":result['School'],"College":result["College"],"Higher":result["Higher"],"FB":result['FB'],"Insta":result["Insta"],"Twitter":result["Twitter"],"Tok":result["Tok"],"DP":result["DP"],"Cover":result['Cover']})
					return HttpResponse("Password changed successfully. Now you can login")
			else:
				return HttpResponse('OTP did not match. Try Again!!')
	else:
		redirect('login')


def forgotusername(request):
	if request.method == "POST":
		gmob = request.POST["mobile"]
		if(len(gmob)!=10 or gmob.isnumeric()==False):
			errormsg = ['Invalid Mobile Number.']
			return render(request,'Login.html',{"warning":errormsg,"title":"Forgot Username"})
		else:

			result = firebase.get("/mobile",gmob)
			if(result):
				msg = 'Your username is ' + result['username']+'. You can use it to login.'
				return render(request,'Login.html',{'info':msg,'title':'Forgot Username'})
			else:
				errormsg = ['No username associated with this number.']
				return render(request,'Login.html',{"warning":errormsg,"title":"Forgot Username"})
	else:
		redirect('login')





def handle_uploaded_file(f):
    with open('/static/rajat.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def imgcng(request):
	if request.method == "POST":
		try:
			changedp = request.FILES['dp']
		except:
			return redirect('profile')
		usernaam = request.session['username']
		result = firebase.get("/users",usernaam)
		if(result["DP"]=="/media/images/user.png"):
			changedp.name = usernaam+"dp"+".jpg"
		else:
			temp = "media/images/"+usernaam+"dp"+".jpg"
			os.remove(temp)
			changedp.name = usernaam+"dp"+".jpg"
			# i = int(result["DP"][-5])
			# changedp.name = usernaam+str(i+1)+".jpg"
		print(changedp.name)
		dpurl = "/media/images/"+changedp.name
		user = Rmail(pic = changedp)
		user.save()
		firebase.delete("/users",usernaam)
		firebase.put('/users',usernaam,{'Name':result['Name'],"Password":result['Password'],'Email':result['Email'],'Mobile':result['Mobile'],'Birtdate':result['Birtdate'],'Gender':result['Gender'],"School":result['School'],"College":result["College"],"Higher":result["Higher"],"FB":result['FB'],"Insta":result["Insta"],"Twitter":result["Twitter"],"Tok":result["Tok"],"DP":dpurl,"Cover":result['Cover']})
		return redirect('profile.html')
	else:
		return redirect('profile.html')

def deldp(request):
		usernaam = request.session['username']
		result = firebase.get("/users",usernaam)
		newdp="/media/images/user.png"
		firebase.put('/users',usernaam,{'Name':result['Name'],"Password":result['Password'],'Email':result['Email'],'Mobile':result['Mobile'],'Birtdate':result['Birtdate'],'Gender':result['Gender'],"School":result['School'],"College":result["College"],"Higher":result["Higher"],"FB":result['FB'],"Insta":result["Insta"],"Twitter":result["Twitter"],"Tok":result["Tok"],"DP":newdp,"Cover":result['Cover']})
		return redirect('/profile')

def delcover(request):
		usernaam = request.session['username']
		result = firebase.get("/users",usernaam)
		newcover="/media/images/cover.jpeg"
		firebase.put('/users',usernaam,{'Name':result['Name'],"Password":result['Password'],'Email':result['Email'],'Mobile':result['Mobile'],'Birtdate':result['Birtdate'],'Gender':result['Gender'],"School":result['School'],"College":result["College"],"Higher":result["Higher"],"FB":result['FB'],"Insta":result["Insta"],"Twitter":result["Twitter"],"Tok":result["Tok"],"DP":result["DP"],"Cover":newcover})
		return redirect('/profile')

def covercng(request):
	if request.method == "POST":
		try:
			changecover = request.FILES['cover']
		except:
			return redirect('profile')
		usernaam = request.session['username']
		result = firebase.get("/users",usernaam)
		if(result["Cover"]=="/media/images/cover.jpeg"):
			changecover.name = usernaam+"cover1"+".jpg"
		else:
			i = int(result["Cover"][-5])
			changecover.name = usernaam+"cover"+str(i+1)+".jpg"
		curl = "/media/images/"+changecover.name
		user = Rmail(pic = changecover)
		user.save()
		firebase.delete("/users",usernaam)
		firebase.put('/users',usernaam,{'Name':result['Name'],"Password":result['Password'],'Email':result['Email'],'Mobile':result['Mobile'],'Birtdate':result['Birtdate'],'Gender':result['Gender'],"School":result['School'],"College":result["College"],"Higher":result["Higher"],"FB":result['FB'],"Insta":result["Insta"],"Twitter":result["Twitter"],"Tok":result["Tok"],"DP":result['DP'],"Cover":curl})
		return redirect('profile')
	else:
		return redirect('profile')


def detupt(request):
	if request.method == "POST":
		username = request.session['username']
		result = firebase.get("/users",username)
		password = result['Password']
		try:
			name = request.POST["newNAME"]
		except:
			name = result['Name']
		try:
			email = request.POST["newEMAIL"]
		except:
			email = result['Email']
		try:
			mob = request.POST["newMOBILE"]
		except:
			mob = str(result['Mobile'])
		try:
			fb = request.POST["newFB"]
		except:
			fb = result['FB']
		try:
			insta = request.POST["newINSTA"]
		except:
			insta = result['Insta']
		try:
			twiiter =request.POST["newTWITTER"]
		except:
			twiiter = result['Twitter']
		try:
			tok =request.POST["newTOK"]
		except:
			tok = result['Tok']
		try:
			school=request.POST["newSCHOOL"]
		except:
			school = result['School']
		try:
			college=request.POST["newCOLLEGE"]
		except:
			college = result['College']
		try:
			higher=request.POST["newHIGHER"]
		except:
			higher = result['Higher']
		errormsg = []
		naam = name.split(" ")
		for i in naam:
			if(i.isalpha()==False):
				name =""
				errormsg.append("Invalid Name")
				break
		if(email=="" or name=="" or mob=="" or fb=="" or insta=="" or twiiter=="" or tok =="" or school=="" or college=="" or higher==""):
			errormsg.append("Field entry cannot be blank.")
		if('@' not in email):
			errormsg.append("Invalid Email.")
			email = ""
		if(len(mob)!=10 or mob.isnumeric()==False):
			errormsg.append("Invalid Mobile Number.")
			mob = ""
		else:
			mobchk = firebase.get('/mobile',mob)
			if(mobchk is not None and mobchk['username'] == username):
				pass
			elif(mobchk is None):
				pass
			else:
				errormsg.append("This mobile number is in use. Please choose another one.")
		if(len(errormsg)>0):
			return render(request,'setting.html',{"warning":errormsg,'Name':name,'Mobile':mob,'Email':email,"school":school,"college":college,"higher":higher,"fb":fb,"insta":insta,"twiiter":insta,"tok":tok})
		else:
			firebase.delete("/users",username)
			firebase.delete("/mobile",result['Mobile'])
			result = firebase.put('/users',username,{'Name':name,'Password':result['Password'],'Email':email,'Mobile':mob,'Birtdate':result['Birtdate'],"Gender":result['Gender'],"DP":result['DP'],"Cover":result['Cover'],"School":school,"College":college,"Higher":higher,"FB":fb,"Insta":insta,"Twitter":twiiter,"Tok":tok})
			mobres =	firebase.put('/mobile',mob,{"username":username})
			if(result):
				return redirect('profile')
			else:
					errormsg =['Some Unknown Error Happened. Please Try again later.']
					return render(request,'signup.html',{'warning':errormsg})
	else:
		return redirect('settings')


def changepass(request):
	if request.method =="GET":
		password = request.GET['curpassword']
		newpass = request.GET['newpassword']
		conpass = request.GET['conpassword']
		username = request.session['username']
		result = firebase.get("/users",username)
		errormsg = []
		if(password=="" or newpass=="" or conpass==""):
			errormsg.append("Please fill all the fields.")
		elif(len(newpass)<8):
			errormsg.append("New password should be 8 character long.")
		else:
			# hash_pass = hash_password(password);
			hash_newpass = hash_password(newpass);
			# hash_conpass = hash_password(conpass);
			if(verify_password(result['Password'],password)):
				if(verify_password(hash_newpass,conpass)):
					firebase.delete("/users",username)
					firebase.put("/users",username,{'Password':hash_newpass,'Name':result['Name'],'Mobile':result['Mobile'],'Email':result['Email'],'Birtdate':result['Birtdate'],'Gender':result['Gender'],"School":result['School'],"College":result["College"],"Higher":result["Higher"],"FB":result['FB'],"Insta":result["Insta"],"Twitter":result["Twitter"],"Tok":result["Tok"],'DP':result['DP'],'Cover':result['Cover']})
					return HttpResponse('Password changed successfully.')
				else:
					errormsg.append('Confirm password does not match.')
			else:
				print("currne")
				errormsg.append('Current password does not match.')

		if(len(errormsg)>0):
			return HttpResponse(errormsg)
	else:
		redirect('settings')
			# return 	render(request,'settings.html',{"warning":errormsg,'Name':result['Name'],'Mobile':result['Mobile'] ,'Email':result['Email'],"school":result['School'],"college":result['College'],"higher":result['Higher'],"fb":result['FB'],"insta":result['Insta'],"twiiter":result['Twitter'],"tok":result['Tok']})

def delacc(request):
	if request.method == "POST":
		password = request.POST['delpass']
		username = request.session['username']
		result = firebase.get("/users",username)
		if(verify_password(result['Password'],password)):
			firebase.delete("/users",username)
			firebase.delete("/mobile",result["Mobile"])
			firebase.delete("/sentmessage",username)
			firebase.delete("/recieved",username)
			request.session['is_logged'] = False;
			request.session['username'] = "";
			return HttpResponse("done")
		else:
			return HttpResponse("Password don't match.!! Account deletion failed.")
	else:
		redirect('settings')


### Message section

def newmsg(request):
	if(request.session.has_key('is_logged') and request.session['is_logged']==True):
		if request.method == "POST":
			username = request.session['username']
			recipient = request.POST['recipient']
			recipient = recipient.lower()
			if(recipient==username):
				return HttpResponse("You cannot send message to yourself.")
			valid = firebase.get("users/",recipient)
			if(valid is not None):
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
				query = recipient+"/NewMsg"
				result = firebase.get("otp",query)
				if result is None:
					result = 0
				query1 ="otp/"+recipient
				firebase.patch_async(query1,{"NewMsg":result+1})
				return HttpResponse("Message sent successfull.")
			else:
				return HttpResponse("Recipient not valid.")
		else:
			return redirect('message')
	else:
		return redirect('login')

def recieve(request):
	if(request.session.has_key('is_logged') and request.session['is_logged']==True):
		username = request.session['username']
		result = firebase.get('/recieved',username)
		if(result is not None):
			data = []
			for i in range((len(result)-1),-1,-1):
				name = 'obj'+str(i)
				name = recievedmessage()
				name.message = result[i]['message']
				name.time = result[i]['time']
				name.photo = "/media/images/user.png"
				data.append(name)
			query = "otp/" + username
			firebase.patch_async(query,{"NewMsg":0})
			return render(request,'recieve.html',{'data':data})
		else:
			return render(request,'recieve.html',{'warning':"No message sent yet."})
	else:
		return render(request,'rmail.html')


def message(request):
	if(request.session.has_key('is_logged') and request.session['is_logged']==True):
		username = request.session['username']
		result = firebase.get('/sentmessage',username)
		usersdet = firebase.get('/users',None)
		if(result is not None):
			data = []
			for i in range((len(result)-1),-1,-1):
				name = 'obj'+str(i)
				name = sentmessage()
				name.recipient = result[i]['recipient']
				name.message = result[i]['message']
				name.time = result[i]['time']
				try:
					name.name = usersdet[name.recipient]["Name"]
				except:
					name.name = "Agyavart User"
				try:
					name.photo = usersdet[name.recipient]["DP"]
				except:
					name.photo = "/media/images/user.png"
				data.append(name)
			return render(request,'msg.html',{'data':data})
		else:
			return render(request,'msg.html',{'warning':"No message recieved Yet"})

	else:
		return render(request,'rmail.html')

def viewsent(request):
	if request.method == "POST":
		try:
			user = request.POST['user']
		except:
			user = None;
		msg = request.POST['msg']
		time = request.POST['time']
		try:
			name = request.POST['name']
		except:
			name = None;
		photo = request.POST['photo']
		return render(request,"viewsent.html",{"user":user,"msg":msg,"time":time,"name":name,"photo":photo})
	else:
		redirect('message')

def chkfornew(request):
	username = request.session['username']
	query = username+"/NewMsg"
	result = firebase.get("otp/",query)
	if(result is not None or result>0):
		return HttpResponse(result)
	else:
		return HttpResponse("0")

def displaymsg(request):
	if(request.method=="POST"):
		username = request.session['username']
		result = firebase.get('/recieved',username)
		if(result is not None):
			data = []
			for i in range((len(result)-1),-1,-1):
				name = 'obj'+str(i)
				name = recievedmessage()
				name.message = result[i]['message']
				name.time = result[i]['time']
				name.photo = "/media/images/user.png"
				data.append(name)
			query = "otp/" + username
			firebase.patch_async(query,{"NewMsg":0})
			return render(request,'displaymsg.html',{'data':data})
		else:
			return render(request,'displaymsg.html',{'warning':"No message sent yet."})
	else:
		return redirect('recieve')


#IMPLEMENTING  CHAT

def chatroom(request):
	username = request.session['username']
	recipient  = request.GET['recipient']
	result = firebase.get('users/',username)
	rec = firebase.get('users/',recipient)
	roomcode = firebase.get('chat/',username+"/"+recipient+"/roomcode")
	if(roomcode==None):
		roomcode = hash_password(username+recipient)
		firebase.patch('chat/'+username+"/"+recipient,{"roomcode":roomcode})
		firebase.patch('chat/'+recipient+"/"+username,{"roomcode":roomcode})
	chatlog = firebase.get("chatlog/",roomcode)
	pastmsg = []
	if(chatlog is not None):
		for i in chatlog:
			obj = chatmsg()
			obj.message = i["message"]
			obj.sender = i["sender"]
			obj.name = i["name"]
			if("time" in i.keys()):
				obj.time = i["time"]
			pastmsg.append(obj)
	return render(request,'rajat.html',{"chatlog":pastmsg,"roomcode":roomcode,"recipient":recipient,"username":username,"recName":rec["Name"],"photo":result['DP']})

def save_message(request):
	roomcode = request.POST["roomcode"]
	message = request.POST['message']
	sender = request.session['username']
	time = request.POST['time']
	result = firebase.get('users/',sender)
	chatlog = firebase.get('chatlog/',roomcode)
	if(chatlog==None):
		chatlog = []
		chatlog.append({"message":message,"sender":sender,"name":result['Name'],"time":time})
	else:
		chatlog.append({"message":message,"sender":sender,"name":result['Name'],"time":time})
	#time = request.POST["time"]
	firebase.put_async('chatlog/',roomcode,chatlog)
	return HttpResponse("done")

def temp(request):
	return render(request,'chat_template.html')


