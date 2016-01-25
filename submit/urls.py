from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.submitTask, name='submitTask'),
    url(r'^submitCasDat/$', views.submitCasDat, name='submitCasDat'),
    url(r'^setPara/$', views.setPara, name='setPara'),
]
