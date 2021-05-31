from django.db import models
from django.utils import timezone
import datetime

class Dist(models.Model):
    dist_name = models.CharField(max_length=50)
    dist_code = models.SmallIntegerField(primary_key=True)
    def __str__(self):
        return str(self.dist_code)

class Dist_new(models.Model):
    dist_name = models.CharField(max_length=50)
    dist_numb = models.SmallIntegerField()
    def __str__(self):
        return str(self.dist_name)

class Pin(models.Model):
    dist = models.ForeignKey(Dist, on_delete=models.CASCADE)
    pin_code = models.CharField(max_length=6, primary_key=True)
    def __str__(self):
        return self.pin_code

class User(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    email = models.EmailField(primary_key=True)
    d1 = models.BooleanField(default=True)
    d2 = models.BooleanField(default=True)
    notify = models.BooleanField()
    eight = models.BooleanField()
    five = models.BooleanField()
    cvsh = models.BooleanField()
    covax = models.BooleanField()
    sptk = models.BooleanField()
    free = models.BooleanField()
    paid = models.BooleanField()
    not_times = models.SmallIntegerField(default=0)
    time = models.DateTimeField(default = (timezone.now()-datetime.timedelta(hours = 6)))
    def __str__(self):
        return self.email


class Day(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    notify = models.BooleanField()
    day_numb = models.SmallIntegerField()
    def __str__(self):
        return str(self.day_numb)

class Time(models.Model):
    time = models.DateField(default = datetime.date.today())

    def change(self):
        days = Day.objects.all()
        for day in days:
            if day.day_numb > 1:
                day.day_numb -= 1
                day.save()
            else:
                day.day_numb = 5
                day.save()
                cents = Cent.objects.filter(day = day)
                for cent in cents:
                    cent.delete()


class Cent(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    cent_id = models.IntegerField()
    def __str__(self):
        return str(self.cent_id)

class Slice(models.Model):
    j = models.SmallIntegerField()
    k = models.SmallIntegerField()
    
    def get(self):
        dist = Dist.objects.order_by('dist_name')
        leng = len(dist)
        if self.k == leng:
            self.j = 0
            self.k = 0
        self.j = self.k
        self.k = self.k + 20
        if self.k>leng:
            self.k = leng
        return  (self.j, self.k)