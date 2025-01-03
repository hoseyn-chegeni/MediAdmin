from django.db import models
from django_jalali.db import models as jmodels
from django import forms

# Create your models here.
STATUS = (
    ("در انتظار", "در انتظار"),
    ("پذیرش شده", "پذیرش شده"),
    ("عدم مراجعه", "عدم مراجعه"),
)


class Month(models.Model):
    objects = jmodels.jManager()
    number = models.PositiveIntegerField()
    slug = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class Day(models.Model):
    number = models.PositiveIntegerField()
    name = models.ForeignKey("WeekDay", on_delete=models.DO_NOTHING)
    month = models.ForeignKey("Month", on_delete=models.CASCADE)
    date = jmodels.jDateField()
    mock_date = models.CharField(max_length=255, blank=True, null=True)
    christ_date = models.DateField()
    is_holiday = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.month.number} / {self.number}"


class WeekDay(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    day = models.ForeignKey("Day", on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    client = models.ForeignKey(
        "client.Client", on_delete=models.CASCADE, blank=True, null=True
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, blank=True, null=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class DeletedSession(models.Model):
    day = models.ForeignKey("Day", on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    client = models.ForeignKey(
        "client.Client", on_delete=models.CASCADE, blank=True, null=True
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    reason = models.TextField()
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class JalaliDateHandler(models.Model):
    date = models.DateField()
    jalali_date = jmodels.jDateField()
