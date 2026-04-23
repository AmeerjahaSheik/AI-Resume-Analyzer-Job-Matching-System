from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    return redirect('analyzer:landing')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL redirects to analyzer landing
    path('', root_redirect),

    # Analyzer app
    path('analyzer/', include('analyzer.urls')),
]