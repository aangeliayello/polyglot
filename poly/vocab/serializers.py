from rest_framework import serializers

class WordContextSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=100)
    context = serializers.CharField(max_length=1000)
