from rest_framework import serializers

from example.models import Car, Manufacturer


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'manufacturer',
            'model',
            'manufactured',
            'classification',
            'retail_price',
            'is_bullet_proof',
        )


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('name', )
