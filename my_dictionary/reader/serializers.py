from rest_framework import serializers

from reader.models import ForeignBookPage, PDFBook


class ForeignBookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignBookPage
        fields = ["pk", "page_text", "foreign_book"]


class PDFBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFBook
        fields = ["title", "current_page_number", "book_file"]


class PDFBookSetPageNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFBook
        fields = ["current_page_number"]
