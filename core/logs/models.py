from django.db import models


# Create your models here.
class ClientSMSLog(models.Model):
    client = models.ForeignKey("client.Client", on_delete=models.CASCADE)
    sender_number = models.CharField(max_length=20)
    receiver_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message_body = models.TextField()
    status = models.CharField(max_length=20)
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"پیامک {self.subject} به {self.client}"


class UserSMSLog(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    sender_number = models.CharField(max_length=20)
    receiver_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message_body = models.TextField()
    status = models.CharField(max_length=20)
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پیامک {self.subject} به {self.user}"
    

class UserActionLog(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    record_id = models.PositiveIntegerField()
    additional_info = models.TextField(blank=True, null=True)
    is_success = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.event_type} on {self.table_name} at {self.timestamp}"
