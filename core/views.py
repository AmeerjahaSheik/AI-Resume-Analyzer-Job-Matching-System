from django.shortcuts import render

def landing_view(request):
    return render(request, 'landing.html')

def how_it_works(request):
    return render(request, 'how_it_works.html')
