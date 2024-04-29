from django.db import models

# Create your models here.
class Month(models.Model):
    number = models.PositiveIntegerField()
    slug = models.CharField(max_length = 100)
     
    def __str__(self):
        return self.slug
    

class Day(models.Model):
    number = models.PositiveIntegerField()
    name = models.ForeignKey('WeekDay', on_delete = models.DO_NOTHING)
    month = models.ForeignKey('Month', on_delete = models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.month.number} / {self.number}'
    


class WeekDay(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name