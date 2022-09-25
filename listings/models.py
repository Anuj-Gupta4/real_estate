from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Listing(models.Model):
    Title = models.CharField(max_length=30, default='House on Sale')
    Location = models.CharField(max_length=30, default='Kalanki')
    City = models.CharField(max_length=30, default='Kathmandu')
    Price = models.IntegerField(default=9999999)
    Bedroom = models.IntegerField(default=0)
    Bathroom = models.IntegerField(default=0)
    Floors = models.IntegerField(default=1)
    Parking = models.IntegerField(default=0)
    Face = models.CharField(max_length=30)
    Area = models.IntegerField(default=100)
    Road_Width = models.IntegerField(default=0)
    Road_Type = models.CharField(max_length=30)
    Build_Area = models.IntegerField(default=0)
    Amenities = models.CharField(max_length=30)
    Contact_number = models.IntegerField(default=9845654321)
    Contact_mail = models.CharField(max_length=30, default='admin@gmail.com')
    Image = models.ImageField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.Title