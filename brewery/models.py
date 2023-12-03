# brewery/models.py
from django.db import models
import uuid

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class Brewery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    website = models.URLField()
    current_rating = models.FloatField(default=0)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    @staticmethod
    def create_brewery_from_api_data(api_data):
        return Brewery.objects.create(
            id=uuid.UUID(api_data.get('id')),
            name=api_data.get('name'),
            address = api_data('address'),
            phone = api_data('phone'),
            website = api_data('website'),
            current_rating = api_data('current_rating'),
            state  = api_data('state'),
            city = api_data('city')
        )

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)  # Assuming Brewery model is defined
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField()
