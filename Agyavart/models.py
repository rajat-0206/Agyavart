from django.db import models

# from fcm_django.models import FCMDevice

# device = FCMDevice.objects.all().first()

# device.send_message(title="Agyavart", body="You have recieved a new message", icon="/static/images/rmailLogoCOncept.png")

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

