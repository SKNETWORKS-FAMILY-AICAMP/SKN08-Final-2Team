from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    reviewCount = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    closed = models.CharField(max_length=255, null = True, default=False)
    keyword = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'restaurants'
        app_label = 'restaurants'

    def __str__(self):
        return self.name
