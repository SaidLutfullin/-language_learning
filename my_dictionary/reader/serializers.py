from rest_framework import serializers

from reader.models import ForeignBookPage


class ForeignBookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignBookPage
        fields = ["pk", "page_text", "foreign_book"]
