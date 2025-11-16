from django.shortcuts import render
# Create your views here.
#Muestra la template home.html

def home(request):
 return render(request, "home.html", {"title": "Hola Django!"})