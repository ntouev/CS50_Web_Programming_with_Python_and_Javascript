from django.contrib import admin

from . models import Regular, Sicilian, Topping, Sub, Addon, Dinner_platter, Salad, Pasta
# Register your models here.
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Regular)
admin.site.register(Sicilian)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Addon)
