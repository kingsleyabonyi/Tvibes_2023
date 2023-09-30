from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Music


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'


    # def create(self, validated_data):
    #      return super().create(validated_data)

    