from rest_framework.serializers import ModelSerializer, ReadOnlyField

from text_books.models import Exercise, TextBook


class ExerciseSerializer(ModelSerializer):
    miniature = ReadOnlyField()

    class Meta:
        model = Exercise
        fields = "__all__"


class TextBookSerializer(ModelSerializer):

    class Meta:
        model = TextBook
        fields = "__all__"
