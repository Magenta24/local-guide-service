from django.db import models


# Create your models here.

class Country(models.Model):
    name = models.CharField('Country name', max_length=150, unique=True)

    def natural_key(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class Discount(models.Model):
    name = models.CharField('Discount name', max_length=150,unique=True)
    value = models.IntegerField('Discount value in %')
    description = models.CharField('Discount description', max_length=200)

    def natural_key(self):
        return f"{self.description}"

    def __str__(self):
        return f"{self.name} {self.value} {self.description}"


class Category(models.Model):
    name = models.CharField('Category name', max_length=150, unique=True)

    def natural_key(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class Attraction(models.Model):
    name = models.CharField('Attraction name', max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField('Attraction price (one adult person)')
    description = models.CharField('Attraction description', max_length=250, null=True, blank=True)
    address = models.TextField('Attraction localization address')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    discounts = models.ManyToManyField(Discount)

    def natural_key(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name} {self.category} {self.price} {self.description} {self.address} {self.country}"


class Tour(models.Model):
    name = models.CharField('Tour name', max_length=250, unique=True)
    duration = models.IntegerField('Tour Duration (days)')
    price = models.IntegerField('Tour price (one adult person)')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    attractions_no = models.IntegerField('Number of attractions in the tour', null=True)
    attractions = models.ManyToManyField(Attraction)

    def __str__(self):
        return f"{self.name} {self.country} {self.duration} {self.price} {self.attractions}"


class Booking(models.Model):
    tour_or_attraction_id = models.CharField('Tour(T) or attraction(A) id', max_length=100, null=True, blank=True)
    price = models.IntegerField('Booking price')
    psp_checkout_id = models.IntegerField('Transaction ID',null=True)
    psp_id = models.IntegerField('PSP ID',null=True)
    start_date = models.DateTimeField('Booking start data')
    adults_no = models.IntegerField('Number of adults', null=True, blank=True)
    kids_no = models.IntegerField('Number of kids', null=True, blank=True)
    seniors_no = models.IntegerField('Number of seniors', null=True, blank=True)

    def __str__(self):
        return f"{self.attraction_id} {self.tour_id} {self.price} {self.start_date} {self.adults_no} {self.kids_no} {self.seniors_no}"