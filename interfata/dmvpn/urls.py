from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #dmvpn/bucuresti/
    path('bucuresti', views.bucuresti, name='bucuresti'),
    path('bucuresti/bw', views.calcul_bw, name='calcul_bw')
]

urlpatterns += staticfiles_urlpatterns()