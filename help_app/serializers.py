from rest_framework import serializers
from .models import Donacion, Contacto


class DonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donacion
        fields = "__all__"


class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = "__all__"
