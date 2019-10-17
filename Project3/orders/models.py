from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# Inherting models.model just establishes this class as a Django model.
class Pasta(models.Model):
    name = models.CharField(max_length=64)
    value = models.FloatField()

    def __str__(self):
        return f"{self.name} {self.value}"

class Salad(models.Model):
    name = models.CharField(max_length=64)
    value = models.FloatField()

    def __str__(self):
        return f"{self.name} {self.value}"

class Dinner_platter(models.Model):
    type = models.CharField(max_length=64)
    small_value = models.FloatField()
    large_value = models.FloatField()

    def __str__(self):
        return f"{self.type} {self.small_value} {self.large_value}"

class Regular(models.Model):
    type = models.CharField(max_length=64)
    small_value = models.FloatField()
    large_value = models.FloatField()

    def __str__(self):
        return f"{self.type} {self.small_value} {self.large_value}"

class Sicilian(models.Model):
    type = models.CharField(max_length=64)
    small_value = models.FloatField()
    large_value = models.FloatField()

    def __str__(self):
        return f"{self.type} {self.small_value} {self.large_value}"

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Sub(models.Model):
    type = models.CharField(max_length=64)
    small_value = models.FloatField()
    large_value = models.FloatField()

    def __str__(self):
        return f"{self.type} {self.small_value} {self.large_value}"

class Addon(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
