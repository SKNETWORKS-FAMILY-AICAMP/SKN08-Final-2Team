from rest_framework import serializers

class MetaOauthAccessTokenSerializer(serializers.Serializer):
    code = serializers.CharField()
