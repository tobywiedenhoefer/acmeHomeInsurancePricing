from rest_framework import serializers
from .models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ["id", "monthly_subtotal", "monthly_taxes"]
