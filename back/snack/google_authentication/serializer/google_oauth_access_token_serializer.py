from rest_framework import serializers

class googleOauthAccessTokenSerializer(serializers.Serializer):
    code = serializers.CharField()
