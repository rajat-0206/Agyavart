from django.db import models

# Create your models here.

class Rmail(models.Model):
	pic = models.ImageField(upload_to = "images")

	def delete(self, *args, **kwargs):
		self.pic.delete()
		super().delete(*args, **kwargs)

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

class users:
	photo: str
	name: str
	username: str

class chatmsg:
	message: str
	sender: str
	name : str
	time : str

class threads:
	uesrname: str
	name : str
	photo : str
	isread: bool



