from django.shortcuts import render, redirect
from .models import Food, Consumption
from django.contrib.auth.decorators import login_required

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

