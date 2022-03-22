from django.db import models
from django.contrib import auth

from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Country(models.Model):
    name = models.CharField(help_text = 'Name of the country', max_length = 50)
    code = models.CharField(help_text = 'alpha2_code', max_length = 2)
    code_2 = models.CharField(help_text = 'alpha2_code', max_length = 3)

class ProxyServer(models.Model):


    host = models.CharField(help_text = 'Name of the host', max_length = 30)
    port = models.IntegerField(help_text = 'Port to conenct to', validators=[MaxValueValidator(65535), MinValueValidator(1)])
    #country = models.CharField(help_text = 'Country Name')
    
    #choices=Country.objects.values_list('name', flat=True),
    country = models.ForeignKey(Country,  on_delete = models.DO_NOTHING)

class Airport(models.Model):
    name = models.CharField(help_text = 'Name of the country', max_length = 50)
    
    country = models.ForeignKey(Country, on_delete = models.DO_NOTHING)

#python manage.py makemigrations Fligts
#python manage.py migrate Fligts