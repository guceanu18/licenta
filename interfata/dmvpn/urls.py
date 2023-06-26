from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    # dmvpn/bucuresti/
    path('bucuresti', views.bucuresti, name='bucuresti'),
    path('bucuresti/bw', views.calcul_bw_buc, name='calcul_bw_buc'),
    path('bucuresti/bw/phase3', views.phase3, name='phase3'),
    path('bucuresti/bw/phase1', views.phase1, name='phase1'),
    path('bucuresti/bw/esp', views.ipsec_esp, name='ipsec_esp'),
    path('bucuresti/bw/ah', views.ipsec_ah, name='ipsec_ah'),
    path('bucuresti/bw/test_delay_buc', views.test_delay_buc, name='test_delay_buc'),
    path('brasov/bw/test_delay_bv', views.test_delay_bv, name='test_delay_bv'),
    path('cluj/bw/test_delay_cj', views.test_delay_cj, name='test_delay_cj'),
    path('constanta/bw/test_delay_ct', views.test_delay_ct, name='test_delay_ct'),
    path('brasov', views.brasov, name='brasov'),
    path('brasov/bw', views.calcul_bw_bv, name='calcul_bw_bv'),
    path('cluj', views.cluj, name='cluj'),
    path('cluj/bw', views.calcul_bw_cj, name='calcul_bw_cj'),
    path('constanta', views.constanta, name='constanta'),
    path('constanta/bw', views.calcul_bw_ct, name='calcul_bw_ct'),

]

urlpatterns += staticfiles_urlpatterns()
