from django.db import models


# Create your models here.

class Country(models.Model):
    name = models.CharField('Country name', max_length=150)

    def natural_key(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class Discount(models.Model):
    name = models.CharField('Discount name', max_length=150)
    value = models.IntegerField('Discount value in %')
    description = models.CharField('Discount description', max_length=200)

    def natural_key(self):
        return f"{self.description}"

    def __str__(self):
        return f"{self.name} {self.value} {self.description}"


class Category(models.Model):
    name = models.CharField('Category name', max_length=150)

    def natural_key(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class Attraction(models.Model):
    name = models.CharField('Attraction name', max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField('Attraction price')
    description = models.CharField('Attraction description', max_length=250, null=True, blank=True)
    address = models.TextField('Attraction localization address')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    discounts = models.ManyToManyField(Discount)

    def __str__(self):
        return f"{self.name} {self.category} {self.price} {self.description} {self.address} {self.country}"


class Tour(models.Model):
    name = models.CharField('Tour name', max_length=250)
    duration = models.IntegerField('Tour Duration (days)')
    price = models.IntegerField('Tour price')
    attractions = models.ManyToManyField(Attraction)

    def __str__(self):
        return f"{self.name} {self.duration} {self.price} {self.attractions}"


class Booking(models.Model):
    tour_or_attraction_id = models.CharField('Tour(T) or attraction(A) id', max_length=100, null=True, blank=True)
    price = models.IntegerField('Booking price')
    start_date = models.DateTimeField('Booking start data')
    adults_no = models.IntegerField('Number of adults', null=True, blank=True)
    kids_no = models.IntegerField('Number of kids', null=True, blank=True)
    seniors_no = models.IntegerField('Number of seniors', null=True, blank=True)

    def __str__(self):
        return f"{self.attraction_id} {self.tour_id} {self.price} {self.start_date} {self.adults_no} {self.kids_no} {self.seniors_no}"