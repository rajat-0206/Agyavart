from django.db import models

# Create your models here.

class Rmail(models.Model):
	pic = models.ImageField(upload_to = "images")

class sentmessage:
	recipient: str
	message: str
	time : str
	name: str
	photo : str

class recievedmessage:
	message: str
	time : str
	photo : str
