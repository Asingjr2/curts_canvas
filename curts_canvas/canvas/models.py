from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from base.models import BaseModel


class Picture(BaseModel): 
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, default=50)

    def __str__(self): 
        return "Picture name is {}".format(self.name)
