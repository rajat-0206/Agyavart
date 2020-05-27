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

