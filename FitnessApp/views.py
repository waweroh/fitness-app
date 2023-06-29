from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Consumption, Bmi
from django.contrib.auth.decorators import login_required
from .forms import BmiForm, BmiMeasurementForm
from django.urls import reverse


# Create your views here.
def index(request):
    if request.method =="POST":
        food_consumed = request.POST.get('food_consumed') #get data/food submitted by user in text not object
        consume = Food.objects.get(name=food_consumed ) #get the food object
        # user = request.user.id #get the user selecting the food
        consume = Consumption(user=request.user, food_consumed=consume)# the actual object
        consume.save()
        foods = Food.objects.all()  

    else: 
        foods = Food.objects.all()
    consumed_foods = Consumption.objects.filter(user=request.user.id)  # List of consumed food objects to be displayed on template
    return render(request, 'index.html', {'foods':foods, 'consumed_foods':consumed_foods})

def delete_food(request,id):
    consumed_food = Consumption.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'delete.html', {'consumed_food': consumed_food})

# 

def greeting_view(request):
    return render(request, "user.html")

def measurements(request):
    measurements = Bmi.objects.all().order_by("date_measured")
    return render(request, "measurements.html", {"measurements": measurements})

def measurement(request, id):
    if request.method == "POST":
        get_object_or_404(Bmi, pk=id).delete()
        # BmiMeasurement.objects.get(id="id").delete()
        return redirect(reverse("all_measurements"))


def bmi(request):
    if request.method == "POST":
        form = BmiForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data["height"]
            weight = form.cleaned_data["weight"]
            bmi = weight/(height**2)
            return render(request, "bmi.html", {"form": form, "bmi": bmi})
    else:
        form = BmiForm()
    return render(request, "bmi.html", {"form": form})

def bmi_measurement(request):
    if request.method == "POST":
        form = BmiMeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save()
            measurements = Bmi.objects.order_by("date_measured").all()
            return render(request, "measurement_recorded.html", {"measurements": measurements})
    else:
        measurements = Bmi.objects.order_by("date_measured").all()
        form = BmiMeasurementForm()
    return render(request, "measurement.html", {"form": form, "measurements": measurements})

