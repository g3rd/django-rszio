from django.conf.urls import url

from .views import image_view


urlpatterns = [
    url(r'^(?P<options>[\w\.\,\;-]+)/(?P<path>.+)$', image_view, name='rszio_image'),
]
