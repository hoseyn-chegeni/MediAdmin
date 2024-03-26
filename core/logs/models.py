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
