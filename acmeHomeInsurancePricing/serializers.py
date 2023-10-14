from rest_framework import serializers
from .models import Quotes


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotes
        fields = ['id', 'monthly_subtotal', 'monthly_taxes']