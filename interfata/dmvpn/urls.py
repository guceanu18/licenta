from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # dmvpn/bucuresti/
    path('bucuresti', views.bucuresti, name='bucuresti'),
    path('bucuresti/bw', views.calcul_bw_buc, name='calcul_bw_buc'),
    path('bucuresti/bw/phase3', views.phase3, name='phase3'),
    path('bucuresti/bw/phase1', views.phase1, name='phase1'),
    path('brasov', views.brasov, name='brasov'),
    path('brasov/bw', views.calcul_bw_bv, name='calcul_bw_bv'),

]

urlpatterns += staticfiles_urlpatterns()
