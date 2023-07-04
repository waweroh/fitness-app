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

# 

# def greeting_view(request):
#     return render(request, "user.html")

# def measurements(request):
#     measurements = Bmi.objects.all().order_by("date_measured")
#     return render(request, "measurements.html", {"measurements": measurements})

# def measurement(request, id):
#     if request.method == "POST":
#         get_object_or_404(Bmi, pk=id).delete()
#         # BmiMeasurement.objects.get(id="id").delete()
#         return redirect(reverse("all_measurements"))


# def bmi(request):
#     if request.method == "POST":
#         form = BmiForm(request.POST)
#         if form.is_valid():
#             height = form.cleaned_data["height"]
#             weight = form.cleaned_data["weight"]
#             bmi = weight/(height**2)
#             return render(request, "bmi.html", {"form": form, "bmi": bmi})
#     else:
#         form = BmiForm()
#     return render(request, "bmi.html", {"form": form})

# def bmi_measurement(request):
#     if request.method == "POST":
#         form = BmiMeasurementForm(request.POST)
#         if form.is_valid():
#             measurement = form.save()
#             measurements = Bmi.objects.order_by("date_measured").all()
#             return render(request, "measurement_recorded.html", {"measurements": measurements})
#     else:
#         measurements = Bmi.objects.order_by("date_measured").all()
#         form = BmiMeasurementForm()
#     return render(request, "measurement.html", {"form": form, "measurements": measurements})

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

        context["bmi"] = round(bmi)
        context["state"] = state

    if request:
        dates = []
        bmis = []
        num = 1
        dates_queryset = Bmi.objects.all().filter()
        for qr in dates_queryset:
            dates.append(str(qr.date)+"("+str(num)+")")
            bmi = qr.bmi
            if bmi is not None:
                bmis.append(int(bmi))
            num += 1

#         plot = figure(x_range=dates, height=600, width=600, title="Bmi Statistics",
#                     toolbar_location="right", tools="pan, wheel_zoom, box_zoom, reset, hover, tap, crosshair")
#         plot.title.text_font_size = "20pt"
#         plot.xaxis.major_label_text_font_size = "14pt"

#         # Add a step renderer
#         plot.step(dates, bmis, line_width=2)

#         # Customize legend
#         legend = Legend(items=[("BMI", [plot])], location="top_right", label_text_font_size="14pt")
#         plot.add_layout(legend, 'right')

#         plot.xaxis.major_label_orientation = pi/4

# # Generate components for embedding the plot
#         script, div = components(plot)
#         context["script"] = script
#         context["div"] = div

    return render(request, "indexbmi.html", context)
