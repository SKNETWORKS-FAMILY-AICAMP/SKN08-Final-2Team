from django.db import models

# Create your models here.
from django.db import models
from account.entity.account import Account  # account_id 외래키 연결 시 사용

class AccountPrefer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)

    Q_1 = models.TextField(null=True, blank=True)
    Q_2 = models.TextField(null=True, blank=True)
    Q_3 = models.TextField(null=True, blank=True)
    Q_4 = models.TextField(null=True, blank=True)
    Q_5 = models.TextField(null=True, blank=True)
    Q_6 = models.TextField(null=True, blank=True)
    Q_7 = models.TextField(null=True, blank=True)
    Q_8 = models.TextField(null=True, blank=True)
    Q_9 = models.TextField(null=True, blank=True)
    Q_10 = models.TextField(null=True, blank=True)
    Q_11 = models.TextField(null=True, blank=True)
    Q_12 = models.TextField(null=True, blank=True)
    Q_13 = models.TextField(null=True, blank=True)
    Q_14 = models.TextField(null=True, blank=True)
    Q_15 = models.TextField(null=True, blank=True)
    Q_16 = models.TextField(null=True, blank=True)
    Q_17 = models.TextField(null=True, blank=True)
    Q_18 = models.TextField(null=True, blank=True)
    Q_19 = models.TextField(null=True, blank=True)
    Q_20 = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'account_prefer'
        app_label = 'account_prefer'

    def __str__(self):
        return f"선호도 조사 - Account {self.account.id}"
