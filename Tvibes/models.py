from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=200)
    origin = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dob = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Music(models.Model):
    title = models.CharField(max_length=200)
    genere = models.CharField(max_length=100)
    date_released = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(Artist,  on_delete=models.CASCADE)
    co_artist = models.ManyToManyField(Artist, through='FeatureArtist', related_name='co_artists')
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)


    def __str__(self):
        return self.title




class FeatureArtist(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


