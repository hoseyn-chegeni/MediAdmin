from django.db import models
from datetime import date
from django_jalali.db import models as jmodels


# Create your models here.
HIGH_RISK_CHOICES = (
    ("دیابت", "دیابت"),
    ("پسوریازیس", "پسوریازیس"),
    ("سرطان", "سرطان"),
    ("هپاتیت", "هپاتیت"),
    ("ایدز", "ایدز"),
    ("تبخال", "تبخال"),
    ("آسم و تنگی نفس", "آسم و تنگی نفس"),
    ("آلرژی و حساسیت", "آلرژی و حساسیت"),
    ("سینوزیت", "سینوزیت"),
    ("سکته (مغزی / قلبی)", "سکته (مغزی / قلبی)"),
    ("سرع", "سرع"),
    ("سل", "سل"),
    ("مشکلات تیرویید", "مشکلات تیرویید"),
    ("فشار خون", "فشار خون"),
    ("سردرد و میگرن", "سردرد و میگرن"),
    ("بیماری های کبدی", "بیماری های کبدی"),
    ("بیماری های کلیوی", "بیماری های کلیوی"),
    ("بیماری های قلبی", "بیماری های قلبی"),
    ("بیماری های پوستی", "بیماری های پوستی"),
    ("مشکلات مغز و اعصاب", "مشکلات مغز و اعصاب"),
)


class Client(models.Model):
    case_id = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fathers_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=255)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    MARITAL_STATUS_CHOICES = (
        ("S", "Single"),
        ("M", "Married"),
    )
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)

    # Health history and treatment
    surgeries = models.CharField(max_length=255, blank=True, null=True)
    allergies = models.CharField(max_length=255, blank=True, null=True)
    medical_history = models.CharField(max_length=255, blank=True, null=True)
    medications = models.CharField(max_length=255, blank=True, null=True)
    smoker = models.CharField(max_length=255, blank=True, null=True)
    disease = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    insurance = models.ForeignKey(
        "insurance.Insurance", on_delete=models.CASCADE, blank=True, null=True
    )
    is_vip = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to="images", default="images/default.png", blank=True, null=True
    )  # Image field for the client
    number_of_receptions = models.PositiveIntegerField(blank=True, null=True, default=0)
    last_reception_date = models.DateField(blank=True, null=True)
    last_reception_reason = models.CharField(blank=True, null=True, max_length=255)
    initial_session = models.ForeignKey(
        "planner.Session",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="initial_session",
    )
    high_risk = models.CharField(
        max_length=255, choices=HIGH_RISK_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class ClientGallery(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.client} : {self.title}"


class ClientAttachment(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    attachments = models.FileField(upload_to="attachments/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.client} : {self.title}"
