from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=255)  # 식당 이름
    latitude = models.FloatField(null=True, blank=True)           # 위도
    longitude = models.FloatField(null=True, blank=True)          # 경도
    address = models.TextField()             # 주소

    class Meta:
        db_table = 'restaurants'
        app_label = 'restaurants'

    def __str__(self):
        return self.name
