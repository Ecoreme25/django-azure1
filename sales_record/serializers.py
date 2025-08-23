
from rest_framework import serializers
from .models import Sales

# Convert from Python object into JSON

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'




