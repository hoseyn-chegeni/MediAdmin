from django.db import models

# Create your models here.
PRIORITIES_CHOICES = [
    ("پایین", "پایین"),
    ("متوسط", "متوسط"),
    ("بالا", "بالا"),
]


STATUS_CHOICES = [
    ("در انتظار بررسی", "در انتظار بررسی"),
    ("در حال انجام", "در حال انجام"),
    ("انجام شده", "انجام شده"),
    ("لغو شده", "لغو شده"),
]


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    priority = models.CharField(
        max_length=100, choices=PRIORITIES_CHOICES, blank=True, null=True
    )
    assign_to = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="Assigner",
    )
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.title
