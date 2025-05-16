from rest_framework import serializers
from account_prefer.entity.account_prefer import AccountPrefer

class AccountPreferSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPrefer
        fields = '__all__'
