from django.db import models
from account_profile.entity.account_profile import AccountProfile
from restaurants.entity.restaurants import Restaurant


class AccountScrap(models.Model):
    id = models.AutoField(primary_key=True)  # 즐겨 찾기 번호
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # 식당 정보
    author = models.ForeignKey(AccountProfile, on_delete=models.CASCADE)  # 저장한 사람
    created_at = models.DateTimeField(auto_now_add=True)  # 즐겨 찾기 등록 시간
    is_deleted = models.BooleanField(default=False)
    
    
    class Meta:
        db_table = 'account_scrap'
        app_label = 'account_scrap'
        unique_together = ('restaurant', 'author')  # 식당과 작성자 조합이 유일해야 함