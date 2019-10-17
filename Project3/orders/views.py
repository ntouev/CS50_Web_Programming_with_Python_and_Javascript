from django.http import HttpResponse
from django.shortcuts import render

from .models import Regular, Sicilian, Topping, Sub, Addon, Dinner_platter, Salad, Pasta
# Create your views here.
def home(request):
    context = {
        "regulars": Regular.objects.all(),
        "sicilians": Sicilian.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinner_platters": Dinner_platter.objects.all(),
        "subs": Sub.objects.all(),
        "addons": Addon.objects.all(),
        "toppings": Topping.objects.all(),
    }

    return render(request, 'orders/home.html', context)
