from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Consumption, Bmi
from django.contrib.auth.decorators import login_required
# from .forms import BmiForm, BmiMeasurementForm
from django.urls import reverse
from math import pi
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import Legend
from bokeh.embed import components
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource



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


def home(request):
    context = {}
    if request.method=="POST":
        weight_metric = request.POST.get("weight-metric")
        weight_imperial = request.POST.get("weight-imperial")

        if weight_metric:
            weight = float(request.POST.get("weight-metric"))
            height = float(request.POST.get("height-metric"))
        elif weight_imperial:
            weight = float(request.POST.get("weight-imperial"))/2.205
            height = (float(request.POST.get("feet"))*30.48 + float(request.POST.get("inches"))*2.54)/100

        bmi = (weight/(height**2))
        save = request.POST.get("save")
        if save == "on":
            Bmi.objects.create(weight=weight, height=height, bmi=round(bmi))
        if bmi < 16:
            state = "Severe Thinness"
        elif bmi > 16 and bmi < 17:
            state = "Moderate Thinness"
        elif bmi > 17 and bmi < 18:
            state = "Mild Thinness"
        elif bmi > 18 and bmi < 25:
            state = "Normal"
        elif bmi > 25 and bmi < 30:
            state = "Overweight"
        elif bmi > 30 and bmi < 35:
            state = "Obese Class I"
        elif bmi > 35 and bmi < 40:
            state = "Obese Class II"
        elif bmi > 40:
            state = "Obese Class III"
        # print (state)

        context["bmi"] = round(bmi)
        context["state"] = state



    return render(request, "indexbmi.html", context)
