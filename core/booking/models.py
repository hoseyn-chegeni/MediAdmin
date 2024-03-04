from django.db import models

# Create your models here.
class Appointment(models.Model):
    service = models.ForeignKey('services.Service', on_delete = models.CASCADE)
    client = models.ForeignKey("client.Client", on_delete = models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.service}, {self.client}, {self.date}'