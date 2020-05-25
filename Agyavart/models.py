from django.db import models

# Create your models here.

class Rmail(models.Model):
	pic = models.ImageField(upload_to = "images")