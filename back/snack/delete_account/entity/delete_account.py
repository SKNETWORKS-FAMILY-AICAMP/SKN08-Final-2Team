from django.db import models

class DeletedAccount(models.Model):
    account_id = models.IntegerField(unique=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'delete_account'
        app_label = 'delete_account'

    def __str__(self):
        return f"DeletedAccount(account_id={self.account_id}, deleted_at={self.deleted_at})"