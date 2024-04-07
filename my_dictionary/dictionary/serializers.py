from rest_framework import serializers

from .models import Words


class WordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = ["russian_word", "foreign_word", "context", "asking_date"]


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = ["id", "russian_word", "foreign_word", "context"]


class WordAnswerSerializer(serializers.Serializer):
    word_id = serializers.IntegerField()
    is_correct = serializers.BooleanField()
